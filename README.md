Anonymous Feedback Telegram Bot
A Telegram bot for collecting anonymous feedback from users. This bot ensures complete anonymity by hashing user IDs before storage and provides a simple interface for both feedback providers and administrators.

Features
Anonymous Feedback Collection: Users can provide feedback without revealing their identity

Predefined Questionnaire: Set of questions that can be easily customized

MongoDB Storage: All feedback is stored securely in a MongoDB database

Owner Notifications: Instant notifications when new feedback is received

Secure User ID Hashing: User identities are protected using SHA256 hashing with salt

Feedback Retrieval: Administrators can easily retrieve all collected feedback

Setup Instructions
Prerequisites
Python 3.7 or higher

MongoDB database (local or cloud-based like MongoDB Atlas)

Telegram account and bot token from BotFather

Installation
Clone or download the project files

bash
mkdir feedback-bot
cd feedback-bot

Create a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Configure environment variables

Copy the .env.example file to .env

Fill in your actual values:

ini
BOT_TOKEN=your_actual_bot_token_from_botfather
MONGO_URI=your_mongodb_connection_string
OWNER_CHAT_ID=your_telegram_chat_id
SALT=a_random_string_for_hashing_security
Set up MongoDB

Create a MongoDB database (local installation or cloud service like MongoDB Atlas)

Update the MONGO_URI in your .env file with your connection string

Getting Your Telegram Chat ID
Start a conversation with @userinfobot on Telegram

Send any message to the bot

The bot will reply with your chat ID

Copy this ID into the OWNER_CHAT_ID field in your .env file

Getting Your Bot Token
Start a conversation with BotFather on Telegram

Use the /newbot command to create a new bot

Follow the instructions to choose a name and username for your bot

After creation, BotFather will provide you with a token

Copy this token into the BOT_TOKEN field in your .env file

Usage
Starting the Bot
bash
python feedback_bot.py
User Commands
/start - Begin the feedback process

/cancel - Cancel the current feedback session

Administrator Commands
/retrieve - Retrieve all collected feedback (owner only)

Customization
Modifying Questions
Edit the QUESTIONS list in the feedback_bot.py file to change the feedback questions:

python
QUESTIONS = [
    "Your first question here?",
    "Your second question here?",
    # Add more questions as needed
]
Database Configuration
The bot uses MongoDB for storage. You can modify the database and collection names by editing the MongoDB class in the code.

Security Considerations
Environment Variables: Never commit your .env file to version control

Salt Value: Use a long, random string for the SALT environment variable

Database Security: Ensure your MongoDB instance is properly secured with authentication

Bot Privacy: Set your bot to private if you want to limit access to specific users

Deployment
Local Deployment
Follow the installation instructions above

Run the bot using python feedback_bot.py

The bot will continue running until you stop the process

Server Deployment
For 24/ operation, consider deploying to a cloud server:

Heroku: Create a Procfile and deploy using Git

DigitalOcean: Set up a droplet and run the bot using a process manager like PM2

AWS EC2: Launch an instance and run the bot in the background

Using Process Managers
For production deployment, use a process manager to keep the bot running:

bash
# Using PM2
pm2 start feedback_bot.py --name feedback-bot

# Using systemd
# Create a service file at /etc/systemd/system/feedback-bot.service
Troubleshooting
Common Issues
Bot not responding: Check your BOT_TOKEN is correct

Database connection errors: Verify your MONGO_URI is correct and MongoDB is running

Permission errors: Ensure the bot has write permissions in its directory

Logs
The bot generates logs that can help with troubleshooting. Check the console output for error messages.

Contributing
Fork the repository

Create a feature branch

Make your changes

Test thoroughly

Submit a pull request

License
This project is open source and available under the MIT License.

Support
If you encounter any issues or have questions:

Check the troubleshooting section above

Ensure all environment variables are properly set

Verify your MongoDB connection is working

Check that your Telegram bot token is valid

For additional help, you can open an issue in the project repository.

Future Enhancements
Potential improvements for future versions:

Web interface for feedback visualization

Advanced analytics and reporting

Multi-language support

Customizable question sets

Feedback categorization and tagging

Export functionality (CSV, PDF)

User authentication for administrators

Rate limiting to prevent spam
