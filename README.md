# Discord Server Copy Bot
## This bot allows you to copy server structures and messages from one Discord server to another. It handles copying channels, roles, and messages using Discord’s API.

# Features
Server Copy: Replicate the structure of one server (channels, roles, categories) to another.
Message Copy: Transfer messages from one channel to another.
Prerequisites
Python 3.8+: Ensure Python is installed on your system.
Discord Bot Token: Create a bot on Discord Developer Portal and get your token.
Setup
1. Clone the Repository
Start by cloning the repository to your local machine:

bash
Copy code
git clone https://github.com/EntomaVasilissaZeta/discord-server-copy-bot.git
cd discord-server-copy-bot
2. Install Dependencies
Install the required Python packages using pip. This will install discord.py and aiohttp, which are necessary for running the bot:

# bash
Copy code
pip install -r requirements.txt
3. Configure the Bot
Create a config.json file in the project directory with your bot's configuration. This file should include your bot token and the IDs for the source and target guilds:

# config
Copy code
{
  "token": "YOUR_BOT_TOKEN_HERE",
  "source_guild_id": "SOURCE_GUILD_ID_HERE",
  "target_guild_id": "TARGET_GUILD_ID_HERE"
}
YOUR_BOT_TOKEN_HERE: Replace with the token you got from the Discord Developer Portal.
SOURCE_GUILD_ID_HERE: Replace with the ID of the server you want to copy from.
TARGET_GUILD_ID_HERE: Replace with the ID of the server you want to copy to.
4. Run the Bot
Execute the bot script to start the bot:

# bash
Copy code
python bot.py
5. Using the Bot
Once the bot is running, you can use the following commands in any server where the bot is present:

!copy: Initiates the process to copy the entire server structure from the source guild to the target guild. This includes roles, categories, and channels.

!mcopy <source_channel_id> <target_channel_id>: Copies all messages from the specified source channel to the target channel. Replace <source_channel_id> and <target_channel_id> with the actual channel IDs.

Example Usage
Copying Server Structure:

In the Discord chat where the bot is present, type !copy and press Enter.
The bot will start copying the server structure from the source guild to the target guild.
Copying Messages:

To copy messages, type !mcopy <source_channel_id> <target_channel_id>.
Replace <source_channel_id> and <target_channel_id> with the IDs of the channels you want to copy messages between.
Troubleshooting
Bot Not Responding: Ensure the bot has the necessary permissions in both source and target guilds. The bot needs permissions to manage channels, roles, and read/send messages.
Missing Roles or Channels: Double-check the IDs in your config.json file and ensure the bot has proper permissions.
Contributing
Feel free to fork the repository and submit pull requests if you want to contribute improvements or bug fixes.

License
This project is licensed under the MIT License - see the LICENSE file for details.
