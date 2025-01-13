import os
import asyncio
import discord
from itertools import cycle
from dotenv import load_dotenv
from discord.ext import commands, tasks

# Setup enviroment
load_dotenv('.env')

# Setup bot client
bot = commands.Bot(command_prefix='k/', intents=discord.Intents.all())

# Setup bot statuses
bot_statuses = cycle(['Am I alive?', 'What am I to do?', 'What are we doing here?'])

@tasks.loop(minutes=1)
async def change_bot_status():
    await bot.change_presence(activity=discord.Game(next(bot_statuses)))

# Alert when the bot is ready
@bot.event
async def on_ready():
    print('I am online and ready? What do I do again?')
    change_bot_status.start()

# Load cog modules
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# Starting the bot
async def run():
    token = os.getenv('token')
    if not token: return print('Please provide a token to login with.')

    async with bot:
        await load()
        await bot.start(os.getenv('token'), reconnect=True)
    
asyncio.run(run())
