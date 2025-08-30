import os
import logging
import hashlib
from datetime import datetime
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ConversationHandler, ContextTypes, filters
)
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
QUESTIONNAIRE = 1

# Predefined questions
QUESTIONS = [
    "How would you rate the company culture? (1-5)",
    "What do you think about the work environment?",
    "Do you have any suggestions for improvement?",
    "How satisfied are you with your team collaboration? (1-5)",
    "Any additional comments?"
]

def anonymize_user_id(user_id, salt=None):
    """Anonymize user ID using hashing with salt."""
    if salt is None:
        salt = os.getenv('SALT', 'default_salt')
    
    # Convert to string and encode
    user_str = str(user_id).encode('utf-8')
    salt_bytes = salt.encode('utf-8')
    
    # Create hash
    hash_object = hashlib.sha256(salt_bytes + user_str)
    return hash_object.hexdigest()

class MongoDB:
    def __init__(self):
        self.uri = os.getenv('MONGO_URI')
        self.client = MongoClient(self.uri)
        self.db = self.client.feedback_bot
        self.collection = self.db.feedback

    def insert_feedback(self, feedback_data):
        """Insert feedback into database."""
        try:
            result = self.collection.insert_one(feedback_data)
            return result.inserted_id
        except Exception as e:
            print(f"Error inserting feedback: {e}")
            return None

    def get_all_feedback(self):
        """Retrieve all feedback from database."""
        try:
            return list(self.collection.find().sort('timestamp', -1))
        except Exception as e:
            print(f"Error retrieving feedback: {e}")
            return []

class FeedbackBot:
    def __init__(self):
        self.token = os.getenv('BOT_TOKEN')
        self.owner_chat_id = os.getenv('OWNER_CHAT_ID')
        self.db = MongoDB()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the conversation and ask the first question."""
        user = update.message.from_user
        logger.info("User %s started the conversation.", user.first_name)
        
        await update.message.reply_text(
            "Welcome to the Anonymous Feedback Bot! 🤖\n\n"
            "This bot allows you to provide completely anonymous feedback. "
            "Your identity will not be stored or shared.\n\n"
            "We'll ask you a series of questions. You can answer at your own pace.\n\n"
            "Type /cancel at any time to stop providing feedback.\n\n"
            "Let's start with the first question:",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Ask first question
        await update.message.reply_text(QUESTIONS[0])
        
        # Initialize user data
        context.user_data['answers'] = []
        context.user_data['current_question'] = 0
        
        return QUESTIONNAIRE

    async def handle_answer(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store answer and ask next question."""
        user_answer = update.message.text
        current_question = context.user_data['current_question']
        
        # Store answer
        context.user_data['answers'].append(user_answer)
        
        # Check if we have more questions
        if current_question + 1 < len(QUESTIONS):
            context.user_data['current_question'] += 1
            next_question = QUESTIONS[current_question + 1]
            await update.message.reply_text(next_question)
            return QUESTIONNAIRE
        else:
            # All questions answered
            return await self.finish_questionnaire(update, context)

    async def finish_questionnaire(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Save all answers and finish conversation."""
        user = update.message.from_user
        answers = context.user_data['answers']
        
        # Anonymize user ID
        anonymous_id = anonymize_user_id(user.id, os.getenv('SALT'))
        
        # Save to database
        feedback_data = {
            'anonymous_id': anonymous_id,
            'answers': answers,
            'timestamp': update.message.date
        }
        self.db.insert_feedback(feedback_data)
        
        # Notify owner
        await self.notify_owner(answers)
        
        await update.message.reply_text(
            "Thank you for your feedback! 🙏\n\n"
            "Your responses have been recorded anonymously. "
            "Your honest input helps us improve.",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Clear user data
        context.user_data.clear()
        
        return ConversationHandler.END

    async def notify_owner(self, answers: list):
        """Notify bot owner about new feedback."""
        message = "📋 New anonymous feedback received:\n\n"
        for i, (question, answer) in enumerate(zip(QUESTIONS, answers)):
            message += f"{i+1}. {question}\nAnswer: {answer}\n\n"
        
        try:
            await self.application.bot.send_message(
                chat_id=self.owner_chat_id,
                text=message
            )
        except Exception as e:
            logger.error("Failed to notify owner: %s", e)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel the conversation."""
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        
        await update.message.reply_text(
            "Feedback session cancelled. Your responses were not saved.",
            reply_markup=ReplyKeyboardRemove()
        )
        
        context.user_data.clear()
        return ConversationHandler.END

    async def retrieve_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Retrieve feedback (owner only)."""
        user = update.message.from_user
        
        if str(user.id) != self.owner_chat_id:
            await update.message.reply_text("Unauthorized access.")
            return
        
        # Get all feedback from database
        all_feedback = self.db.get_all_feedback()
        
        if not all_feedback:
            await update.message.reply_text("No feedback available yet.")
            return
        
        # Format feedback for display
        message = "📊 Feedback Summary:\n\n"
        for i, feedback in enumerate(all_feedback, 1):
            message += f"Feedback #{i}:\n"
            for j, (question, answer) in enumerate(zip(QUESTIONS, feedback['answers'])):
                message += f"  Q{j+1}: {answer}\n"
            message += f"  Date: {feedback['timestamp'].strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Split message if too long (Telegram has message length limits)
        if len(message) > 4096:
            for x in range(0, len(message), 4096):
                await update.message.reply_text(message[x:x+4096])
        else:
            await update.message.reply_text(message)

    def setup_handlers(self, application):
        """Setup conversation and command handlers."""
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                QUESTIONNAIRE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_answer)
                ],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        
        application.add_handler(conv_handler)
        application.add_handler(CommandHandler('retrieve', self.retrieve_feedback))
        
        # Store application reference for notifications
        self.application = application

    def run(self):
        """Run the bot."""
        application = Application.builder().token(self.token).build()
        self.setup_handlers(application)
        
        logger.info("Bot is running...")
        application.run_polling()

if __name__ == '__main__':
    bot = FeedbackBot()
    bot.run()