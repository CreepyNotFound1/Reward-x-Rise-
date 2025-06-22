import os
import sys
import random
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
from discord import Interaction
from dotenv import load_dotenv
from keep_alive import keep_alive
import asyncio
from datetime import datetime, timedelta

# 🌐 Load token from .env file
load_dotenv("token.env")
keep_alive()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

RGB_LINE = "https://i.imgur.com/9hVqfby.gif"
BOT_OWNER_ID = 1355469919592120340
TICKET_CHANNEL_ID = 1376975625100722236
LOG_CHANNEL_ID = 1383716982083420231

fgen_files = {
    "minecraft": "minecraft_info.txt",
    "netflix": "netflix_info.txt",
    "steam": "steam_info.txt",
    "roblox": "roblox_info.txt",
    "crunchyroll": "crunchyroll_info.txt",
    "nitro": "nitro_info.txt"
}
pgen_files = {
    "minecraft": "p_minecraft_info.txt",
    "netflix": "p_netflix_info.txt",
    "steam": "p_steam_info.txt",
    "roblox": "p_roblox_info.txt",
    "crunchyroll": "p_crunchyroll_info.txt",
    "nitro": "p_nitro_info.txt"
}

invite_tracker = {}
user_invites = {}
giveaway_entries = {}

def make_embed(**kwargs):
    embed = discord.Embed(color=random.randint(0, 0xFFFFFF), **kwargs)
    embed.set_image(url=RGB_LINE)
    return embed

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.wait_until_ready()
    for guild in bot.guilds:
        invites = await guild.invites()
        invite_tracker[guild.id] = {invite.code: invite.uses for invite in invites}
        user_invites[guild.id] = {}

    channel = bot.get_channel(TICKET_CHANNEL_ID)
    if channel:
        async for message in channel.history(limit=10):
            if message.author.id == bot.user.id and message.components:
                await message.delete()
        view = TicketView()
        await channel.send(embed=make_embed(title="🎟️ Create a Ticket", description="Click the button below to open a ticket."), view=view)

@bot.event
async def on_member_join(member):
    guild = member.guild
    after = await guild.invites()
    before = invite_tracker.get(guild.id, {})
    inviter = None

    for invite in after:
        if before.get(invite.code, 0) < invite.uses:
            inviter = invite.inviter
            break

    invite_tracker[guild.id] = {invite.code: invite.uses for invite in after}

    if inviter:
        user_invites[guild.id][inviter.id] = user_invites[guild.id].get(inviter.id, 0) + 1
        count = user_invites[guild.id][inviter.id]
        log_channel = bot.get_channel(LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"👋 Welcome {member.mention} to the server! Invited by {inviter.mention}. They now have **{count} invites**.")

    movement_log = bot.get_channel(LOG_CHANNEL_ID)
    if movement_log:
        await movement_log.send(f"📅 {member} joined the server.")

@bot.event
async def on_member_remove(member):
    movement_log = bot.get_channel(LOG_CHANNEL_ID)
    if movement_log:
        await movement_log.send(f"📄 {member} left the server.")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log:
        await log.send(f"🗑️ Message deleted in {message.channel.mention} by {message.author.mention}: `{message.content}`")

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log and before.content != after.content:
        await log.send(f"✏️ Message edited in {before.channel.mention} by {before.author.mention}:\nBefore: `{before.content}`\nAfter: `{after.content}`")

@bot.event
async def on_voice_state_update(member, before, after):
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log:
        if before.channel is None and after.channel:
            await log.send(f"🎵 {member} joined voice channel {after.channel.name}.")
        elif before.channel and after.channel is None:
            await log.send(f"🔇 {member} left voice channel {before.channel.name}.")
        elif before.channel != after.channel:
            await log.send(f"🔄 {member} switched from {before.channel.name} to {after.channel.name}.")

@bot.event
async def on_member_update(before, after):
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log:
        if before.nick != after.nick:
            await log.send(f"📝 {after.mention} changed nickname from `{before.nick}` to `{after.nick}`")
        if before.roles != after.roles:
            before_roles = set(before.roles)
            after_roles = set(after.roles)
            added = after_roles - before_roles
            removed = before_roles - after_roles
            if added:
                await log.send(f"➕ {after.mention} got roles: {', '.join([r.mention for r in added])}")
            if removed:
                await log.send(f"➖ {after.mention} lost roles: {', '.join([r.mention for r in removed])}")

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log and not message.author.bot:
        await log.send(f"📲 Message sent in {message.channel.mention} by {message.author.mention}: `{message.content}`")

@bot.event
async def on_guild_channel_create(channel):
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log:
        await log.send(f"🚨 **ANTI-NUKE ALERT**: Channel {channel.mention} was created. Deleting...")
    await channel.delete()

@bot.event
async def on_guild_channel_delete(channel):
    log = bot.get_channel(LOG_CHANNEL_ID)
    if log:
        await log.send(f"⚠️ **Channel Deleted:** {channel.name}")

@bot.check
async def global_admin_only(ctx):
    return ctx.author.id == BOT_OWNER_ID

# --- Load Modular Commands ---
from full_commands import setup
setup(bot)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
