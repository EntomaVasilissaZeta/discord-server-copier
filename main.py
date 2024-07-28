import discord
from discord.ext import commands
import json
import aiohttp

with open('config.json') as f:
    config = json.load(f)

TOKEN = config['token']
SOURCE_GUILD_ID = int(config['source_guild_id'])
TARGET_GUILD_ID = int(config['target_guild_id'])

# Set up Discord bot
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    for guild in bot.guilds:
        print(f'Guild ID: {guild.id}, Guild Name: {guild.name}')

async def delete_all_channels(guild):
    for channel in guild.channels:
        try:
            await channel.delete()
            print(f'Deleted channel: {channel.name}')
        except discord.Forbidden:
            print(f'Failed to delete channel: {channel.name} (Insufficient permissions)')
        except discord.HTTPException as e:
            print(f'Failed to delete channel: {channel.name} (HTTPException: {e})')

async def create_webhook(channel, user):
    avatar_url = user.avatar.url if user.avatar else None
    webhook = await channel.create_webhook(name=user.name, avatar=await user.avatar.read() if avatar_url else None)
    return webhook

async def copy_server(source_guild_id, target_guild_id):
    source_guild = bot.get_guild(source_guild_id)
    target_guild = bot.get_guild(target_guild_id)

    if not source_guild:
        print(f"Source guild with ID {source_guild_id} not found.")
        return
    if not target_guild:
        print(f"Target guild with ID {target_guild_id} not found.")
        return

    await delete_all_channels(target_guild)

    await target_guild.edit(name=source_guild.name)

    for role in reversed(source_guild.roles):
        if role.is_default():
            continue
        await target_guild.create_role(
            name=role.name,
            permissions=role.permissions,
            colour=role.colour,
            hoist=role.hoist,
            mentionable=role.mentionable
        )

    for category in source_guild.categories:
        new_category = await target_guild.create_category(name=category.name)
        for channel in category.channels:
            if isinstance(channel, discord.TextChannel):
                await new_category.create_text_channel(name=channel.name, topic=channel.topic)
            elif isinstance(channel, discord.VoiceChannel):
                await new_category.create_voice_channel(name=channel.name)
            elif isinstance(channel, discord.StageChannel):
                await new_category.create_stage_channel(name=channel.name)

    for channel in source_guild.channels:
        if isinstance(channel, discord.TextChannel) and channel.category is None:
            await target_guild.create_text_channel(name=channel.name, topic=channel.topic)
        elif isinstance(channel, discord.VoiceChannel) and channel.category is None:
            await target_guild.create_voice_channel(name=channel.name)
        elif isinstance(channel, discord.StageChannel) and channel.category is None:
            await target_guild.create_stage_channel(name=channel.name)

    print("Server copied successfully.")

async def copy_messages(source_channel_id, target_channel_id):
    source_channel = bot.get_channel(source_channel_id)
    target_channel = bot.get_channel(target_channel_id)

    if not source_channel:
        print(f"Source channel with ID {source_channel_id} not found.")
        return
    if not target_channel:
        print(f"Target channel with ID {target_channel_id} not found.")
        return

    async for message in source_channel.history(limit=None, oldest_first=True):
        webhook = await create_webhook(target_channel, message.author)
        await webhook.send(content=message.content, username=message.author.name, avatar_url=message.author.avatar.url)
        await webhook.delete()

@bot.command()
async def copy(ctx):
    source_guild = bot.get_guild(SOURCE_GUILD_ID)
    target_guild = bot.get_guild(TARGET_GUILD_ID)

    if not source_guild:
        await ctx.send(f"Source guild with ID {SOURCE_GUILD_ID} not found.")
    if not target_guild:
        await ctx.send(f"Target guild with ID {TARGET_GUILD_ID} not found.")

    if source_guild and target_guild:
        await copy_server(SOURCE_GUILD_ID, TARGET_GUILD_ID)
        await ctx.send("Server copy initiated.")

@bot.command()
async def mcopy(ctx, source_channel_id: int, target_channel_id: int):
    await copy_messages(source_channel_id, target_channel_id)
    await ctx.send("Messages copied successfully.")

bot.run(TOKEN)
