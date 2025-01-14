import discord
from discord import app_commands
from discord.ext import commands

# TO DO 
# Guild Info --- Scheduled Events, vanity invite, language


class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} has loaded and is ready')

    # Bot Info

    # Help Command

    # Command List

    # User Info

    # Channel Info

    # Guild Info
    @app_commands.command(name='guild-info', description='Get the information and statistics for your current guild!')
    @app_commands.guild_only()
    async def guildinfo(self, interaction: discord.Interaction):
        guild = interaction.guild

        try:
             # Count all bots in the server
            guild.fetch_members()
            bot_count = [m for m in guild.members if m.bot]

            # Set descrption
            if guild.description is not None: description = f'\n\n {guild.description}'
            else: description = ''

            if len(guild.emojis) > 0: emojis = f'\n😀 Emojis: {len(guild.emojis)}'
            else: emojis = ''

            if len(guild.stickers) > 0: stickers = f'\n📃 Stickers: {len(guild.stickers)}' 
            else: stickers = ''


            guild_info_embed = discord.Embed(title=f"{guild.name}'s Information", description=f"{guild.name} was created by **{guild.owner}** on {guild.created_at.strftime('%m-%d-%Y at %H:%M')}. {description}", color=discord.Color.pink())
            guild_info_embed.add_field(name='Members', value=f'Total: {guild.member_count} \n🙋‍♂️ Humans: {guild.member_count - len(bot_count)} \n🤖 Bots: {len(bot_count)} \n💠 Boosters: {guild.premium_subscription_count}', inline=True)
            guild_info_embed.add_field(name='Basic Stats', value=f'👨‍🏫 Roles: {len(guild.roles)} \n 💬 Channels: {len(guild.channels)} {emojis} {stickers}', inline=True)
            guild_info_embed.set_footer(text=f'Guild ID: {guild.id}')

            # Conditional elements
            if guild.icon is not None: guild_info_embed.set_thumbnail(url=guild.icon)
            if guild.banner is not None: guild_info_embed.set_image(url=guild.banner)

            await interaction.response.send_message(embed=guild_info_embed)
        except Exception as e:
            print(e)

    # Emote Info


async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
    