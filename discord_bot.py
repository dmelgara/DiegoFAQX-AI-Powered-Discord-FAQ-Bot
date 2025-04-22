import discord
from faq_bot_Diego import understand, generate


class MyClient(discord.Client):


    def __init__(self):

        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self):
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message):
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):
            utterance = message.content.replace(f'<@{self.user.id}>', '').strip()
            intent = understand(utterance)
            response = generate(intent, utterance)
            await message.channel.send(response)

        # check message content and respond accordingly
        if message.content == 'ping':
            await message.channel.send('pong')

## Set up and log in
client = MyClient()
with open("bot_token.txt") as file:
    token = file.read()

client.run(token)