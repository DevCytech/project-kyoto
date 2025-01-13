import os
import discord
from discord import app_commands
from discord.ext import commands

class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} has loaded and is ready')

    # Command allows bot to sync all of its slash commands to discord
    # Sync may take a few hours to completely sync, even after bot response
    @commands.command()
    async def sync(self, ctx: discord.Message):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        try:
            sync_commands = await self.bot.tree.sync()
            sync_embed = discord.Embed(description=f'✔️ I have synced **{len(sync_commands)}** commands!', color=discord.Color.green())
            await ctx.send(embed=sync_embed)

        except Exception as e:
            print(f'Error syncing commands: {e}')
            error_embed = discord.Embed(description=f'❌ I ran into an issue syncing the commands. \n\n```{e}```', color=discord.Color.red())
            await ctx.send(embed=error_embed)

async def setup(bot):
    await bot.add_cog(DevCommands(bot))
    