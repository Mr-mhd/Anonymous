# Anonymous Feedback Telegram Bot

A Telegram bot for collecting anonymous feedback from users.

## Key Features
- Completely anonymous feedback collection
- Secure storage in MongoDB
- Instant notifications to the admin
- Ability to retrieve all feedback

## Quick Setup

1. Prerequisites:
   - Python 3.7 or higher
   - MongoDB account (local or Atlas)

2. Installation:
   ```bash
   git clone <repository-url>
   cd feedback-bot
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

3. Configuration:
   - Create a `.env` file:
   ```ini
   BOT_TOKEN=your_bot_token
   MONGO_URI=your_mongodb_connection_string
   OWNER_CHAT_ID=your_chat_id
   SALT=a_strong_random_string
   ```

4. Run:
   ```bash
   python feedback_bot.py
   ```

## How to Use

- Users: Send `/start` command to begin the feedback process
- Admin: Send `/retrieve` command to view received feedback

## Getting Bot Token

1. Talk to [BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Choose a name and username for your bot
4. Place the received token in the `.env` file
