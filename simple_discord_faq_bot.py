"""

Diego Melgara, FEB 2025
"""
import discord
from faq_bot_Diego import understand, generate, load_FAQ_data
import nest_asyncio

intents, responses, regex_patterns = load_FAQ_data()

## MYClient Class Definition

class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self):
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

        channel_id = 1340501083637682261
        channel = self.get_channel(channel_id)

        if channel:
            await channel.send("👋 Hey, I'm Diego's Bot! Remember to include `@Diegos_Bot` whenever you want to talk to me!")

        print("Welcome message sent!")


    async def on_message(self, message):
        """Handles Discord messages."""
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            utterance = message.content.replace(f'<@{self.user.id}>', '').strip()
            intent = understand(utterance)
            response = generate(intent, utterance)

            await message.channel.send(response)



## Set up and log in

nest_asyncio.apply()

client = MyClient()
with open("bot_token.txt") as file:
    token = file.read().strip()
client.run(token)