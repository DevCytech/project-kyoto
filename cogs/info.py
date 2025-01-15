import discord
import textwrap
from discord import app_commands
from discord.ext import commands


class InfoCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{__name__} has loaded and is ready')

    # Bot Info
    @app_commands.command(name='bot-info', description='Get information about me!')
    async def botinfo(self, interaction: discord.Integration):
        bot_info_embed = discord.Embed(title='About Me', description='Hello I am Project Kyoto, an Discord bot to help make your life easier throughout the day. So far my abilities are a little underwhelming but I am getting there slowly, please bear with me! I was started as a passion project, and will hopefully stay that way. I hope you enjoy the functions I currently have and will enjoy using me as I grow bigger! Thank you so much for the support both from me and the Development team powering this project. If you need any help please read below, as always, have a great day!', color=discord.Color.purple())
        bot_info_embed.add_field(name='Help', value='If you need general help please view my `/help` or visit my website and go to the FAQ page!', inline=False)
        bot_info_embed.add_field(name='Commands', value='To view all of my commands please use `/command-list` or view them in the `/` area!', inline=False)
        bot_info_embed.add_field(name='Website', value='https://disconnectbot.com/project-kyoto', inline=False)
        bot_info_embed.set_thumbnail(url='https://images-ext-1.discordapp.net/external/odub4mNDY9mIiHXLzu12sgohpMWaXxuD5hHvUcZfO2c/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1136826536377458800/fa55e685ee4c99b1356af57be915187a.png?format=webp&quality=lossless&width=636&height=636')

        await interaction.response.send_message(embed=bot_info_embed)

    # Help Command

    # Command List

    # User Info

    # Channel Info
    @app_commands.command(name='channel-info', description='Get information about your current channel or specifed channel')
    @app_commands.guild_only()
    async def channelinfo(self, interaction: discord.Interaction, textchannel: discord.TextChannel = None):
        fallback_channel = interaction.channel
        if textchannel is not None:
            target_channel = textchannel
        else:
            target_channel = fallback_channel

        channel_info_embed = discord.Embed(title=f'{target_channel.name} Information', description=f'{target_channel.topic if not 'None' else 'This channel does not have a topic listed'}', color=discord.Color.pink())
        channel_info_embed.add_field(name='Category', value=f'{target_channel.category if not 'None' else 'Not in a Category'}', inline=True)
        channel_info_embed.add_field(name='Members Allowed', value=f'🙋‍♂️ {len(target_channel.members)}', inline=True)
        channel_info_embed.add_field(name='Thread Count', value=f'💬 {len(target_channel.threads)}', inline=True)

        if target_channel.is_nsfw():
           channel_info_embed.add_field(name='NSFW', value='🔞 This channel is considered an NSFW channel.', inline=True)

        channel_info_embed.add_field(name='Jump Link', value=f'🔗 Jump to this channel: {target_channel.jump_url}', inline=False)
        channel_info_embed.set_footer(text=f'Channel ID: {target_channel.id}')

        await interaction.response.send_message(embed=channel_info_embed)

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

            if guild.vanity_url is not None: guild_info_embed.add_field(name='Vanity URL', value=f'{guild.vanity_url}')

            if len(guild.scheduled_events) > 0:
                i = 0
                events = ''
                for e in guild.scheduled_events:
                    if i == 5: break
                    i += 1
                    if i == 1:
                        events = f'[{e.name}]({e.url}) on {e.start_time.strftime('%m-%d-%Y at %H:%M')}. {textwrap.shorten(e.description, width=75, placeholder='') if not None else ''}..'
                    else:
                        events = f'{events} \n[{e.name}]({e.url}) on {e.start_time.strftime('%m-%d-%Y at %H:%M')}. {textwrap.shorten(e.description, width=75, placeholder='') if not None else ''}..'


                guild_info_embed.add_field(name='Upcoming events:', value=f'{events}', inline=False)

            await interaction.response.send_message(embed=guild_info_embed)
        except Exception as e:
            print(e)

    # Emote Info


async def setup(bot):
    await bot.add_cog(InfoCommands(bot))
    