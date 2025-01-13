import os
import psutil
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
            print(f'!!! Error syncing commands: {e}')
            error_embed = discord.Embed(description=f'❌ I ran into an issue syncing the commands. \n\n```{e}```', color=discord.Color.red())
            await ctx.send(embed=error_embed)

    # Quick diag command to learn information about how to bot is running
    @commands.command()
    async def diag(self, ctx: discord.Message):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')
        if not ctx.author.id == int(dev_id): return

        mem_info = psutil.virtual_memory().used
        load_info = psutil.getloadavg()
        cpu_info = psutil.cpu_percent(interval=1)

        diag_embed = discord.Embed(title='Diagnostics Open', description='Latency in ms', color=discord.Color.green())
        diag_embed.add_field(name="Latency (ms)", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        diag_embed.add_field(name='CPU Usage (%)', value=f"{cpu_info}%", inline=True)
        diag_embed.add_field(name='Average Loads (%)', value=f"1m {round(load_info[0], 2)}% | 5m {round(load_info[1], 2)}% | 15m {round(load_info[2], 2)}%")
        diag_embed.add_field(name="Memory (mb)", value=f"{mem_info / 1024 **2:n}mb", inline=True)
        await ctx.send(embed=diag_embed)

    # Allows the bot to be restart from a remote location 
    @commands.command()
    async def restart(self, ctx: discord.Message):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        restart_embed = discord.Embed(description=f'⚠️ I am now restarting. . .', color=discord.Color.yellow())
        await ctx.send(embed=restart_embed)

        print('Restarting bot as per command')
        await self.bot.close()
        os.system('python3 index.py')

    # Allows the bot to be shutdown from a remote location 
    @commands.command()
    async def shutdown(self, ctx: discord.Message):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        shutdown_embed = discord.Embed(description=f'⚠️ I am now shutting down. . .', color=discord.Color.yellow())
        await ctx.send(embed=shutdown_embed)

        await self.bot.close()

    # Allows the bot to reload a module from a remote location
    @commands.command()
    async def reload(self, ctx: discord.Message, mod=None):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        if mod is None: 
            error_embed = discord.Embed(description=f'❌ Please provide a module name to reload', color=discord.Color.red())
            await ctx.send(embed=error_embed)
            return
        
        try: 
            await self.bot.reload_extension(f'cogs.{mod}')
            reload_embed = discord.Embed(description=f'✔️ I have successfully reloaded the `{mod}` module!', color=discord.Color.green())
            await ctx.send(embed=reload_embed)
        except Exception as e:
            print(f'!!! Error reloading module: {e}')
            error_embed = discord.Embed(description=f'❌ I ran into an issue reloading a module. \n\n```{e}```', color=discord.Color.red())
            await ctx.send(embed=error_embed)

    # Allows the bot to load a module from a remote location
    @commands.command()
    async def load(self, ctx: discord.Message, mod=None):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        if mod is None: 
            error_embed = discord.Embed(description=f'❌ Please provide a module name to load', color=discord.Color.red())
            await ctx.send(embed=error_embed)
            return
        
        try: 
            await self.bot.load_extension(f'cogs.{mod}')
            load_embed = discord.Embed(description=f'✔️ I have successfully loaded the `{mod}` module!', color=discord.Color.green())
            await ctx.send(embed=load_embed)
        except Exception as e:
            print(f'!!! Error loading module: {e}')
            error_embed = discord.Embed(description=f'❌ I ran into an issue loading a module. \n\n```{e}```', color=discord.Color.red())
            await ctx.send(embed=error_embed)

    # Allows the bot to unload a module from a remote location
    @commands.command()
    async def unload(self, ctx: discord.Message, mod=None):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        if mod is None: 
            error_embed = discord.Embed(description=f'❌ Please provide a module name to unload', color=discord.Color.red())
            await ctx.send(embed=error_embed)
            return
        
        try: 
            await self.bot.unload_extension(f'cogs.{mod}')
            unload_embed = discord.Embed(description=f'✔️ I have successfully unloaded the `{mod}` module!', color=discord.Color.green())
            await ctx.send(embed=unload_embed)
        except Exception as e:
            print(f'!!! Error loading module: {e}')
            error_embed = discord.Embed(description=f'❌ I ran into an issue unloading a module. \n\n```{e}```', color=discord.Color.red())
            await ctx.send(embed=error_embed)

    # Allows the bot to enable or re-enable a command from a remote location
    @commands.command()
    async def togglecommand(self, ctx: discord.Message, cmd=None):
        dev_id = os.getenv('dev_id')
        if dev_id is None: return print('No developer id has been set in enviroment file.')

        if not ctx.author.id == int(dev_id): return

        if cmd is None: 
            error_embed = discord.Embed(description=f'❌ Please provide a command name to toggle', color=discord.Color.red())
            await ctx.send(embed=error_embed)
            return
        
        try: 
            target_command = self.bot.get_command(cmd)

            if target_command is None:
                error_embed = discord.Embed(description=f'❌ Command could not be found, please try again', color=discord.Color.red())
                await ctx.send(embed=error_embed)
                return

            target_command.enabled = not target_command.enabled
            status = 'enabled' if target_command.enabled else 'disabled'
            toggled_embed = discord.Embed(description=f'✔️ I have successfully {status} the `{cmd}` command!', color=discord.Color.green())
            await ctx.send(embed=toggled_embed)
        except Exception as e:
            print(f'!!! Error toggling command: {e}')
            error_embed = discord.Embed(description=f'❌ I ran into an issue toggling the command. \n\n```{e}```', color=discord.Color.red())
            await ctx.send(embed=error_embed)
        

async def setup(bot):
    await bot.add_cog(DevCommands(bot))
    