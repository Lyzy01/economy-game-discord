import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

class EconomyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Dynamically load modules from the cogs folder
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename}')
                print(f'Loaded module: {filename}')
        
        # Sync your slash commands globally across Discord
        await self.tree.sync()

bot = EconomyBot()

@bot.event
async def on_ready():
    print(f'🤖 {bot.user.name} is online and operational!')
    print('------')

bot.run(os.getenv('DISCORD_TOKEN'))
