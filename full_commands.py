import os
import random
import discord
from discord.ext import commands
from main import make_embed, fgen_files, pgen_files, user_invites

@commands.command()
async def fgen(ctx, category=None):
    if category == "stock":
        report = ""
        for k, v in fgen_files.items():
            if os.path.exists(v):
                with open(v, 'r') as f:
                    report += f"🎁 **{k.capitalize()}**: `{len([l for l in f if l.strip()])}`\n"
        await ctx.send(embed=make_embed(title="🎁 fgen Stock", description=report or "No stock available."))
        return

    if category not in fgen_files:
        await ctx.send(embed=make_embed(title="❌ Invalid Category", description="Use a valid category or `stock`"))
        return

    filepath = fgen_files[category]
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        await ctx.send(embed=make_embed(title="⚠️ Empty Stock", description="No accounts available."))
        return

    selected = random.choice(lines)
    lines.remove(selected)

    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    try:
        await ctx.author.send(embed=make_embed(title=f"🎁 {category.capitalize()} Account", description=f"```{selected}```"))
        await ctx.send(embed=make_embed(title="📩 Sent", description="Check your DMs!"))
    except:
        await ctx.send(embed=make_embed(title="❌ DM Error", description="Enable DMs to receive the account."))

@commands.command()
async def pgen(ctx, category=None):
    if category == "stock":
        report = ""
        for k, v in pgen_files.items():
            if os.path.exists(v):
                with open(v, 'r') as f:
                    report += f"📝 **{k.capitalize()}**: `{len([l for l in f if l.strip()])}`\n"
        await ctx.send(embed=make_embed(title="📝 pgen Stock", description=report or "No stock available."))
        return

    if category not in pgen_files:
        await ctx.send(embed=make_embed(title="❌ Invalid Category", description="Use a valid category or `stock`"))
        return

    filepath = pgen_files[category]
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        await ctx.send(embed=make_embed(title="⚠️ Empty Stock", description="No accounts available."))
        return

    selected = random.choice(lines)
    lines.remove(selected)

    with open(filepath, 'w') as f:
        f.write('\n'.join(lines) + '\n')

    try:
        await ctx.author.send(embed=make_embed(title=f"📝 {category.capitalize()} Name", description=f"```{selected}```"))
        await ctx.send(embed=make_embed(title="📩 Sent", description="Check your DMs!"))
    except:
        await ctx.send(embed=make_embed(title="❌ DM Error", description="Enable DMs to receive the name."))

@commands.command()
async def stock(ctx):
    fstock = ""
    pstock = ""
    for k, v in fgen_files.items():
        if os.path.exists(v):
            with open(v, 'r') as f:
                fstock += f"🎁 **{k.capitalize()}**: `{len([l for l in f if l.strip()])}`\n"
    for k, v in pgen_files.items():
        if os.path.exists(v):
            with open(v, 'r') as f:
                pstock += f"📝 **{k.capitalize()}**: `{len([l for l in f if l.strip()])}`\n"
    embed = make_embed(title="📦 Stock Overview")
    embed.add_field(name="🎁 fgen Stock", value=fstock or "None", inline=False)
    embed.add_field(name="📝 pgen Stock", value=pstock or "None", inline=False)
    await ctx.send(embed=embed)

@commands.command()
async def help(ctx):
    embed = make_embed(title="📘 Help Menu", description="Here are the available commands:")
    embed.add_field(name="!fgen <category>", value="Generate free account", inline=False)
    embed.add_field(name="!pgen <category>", value="Generate premium name", inline=False)
    embed.add_field(name="!stock", value="View stock of all categories", inline=False)
    embed.add_field(name="!drop", value="Drop a random item from stock", inline=False)
    embed.add_field(name="!payout <user_id> <service>", value="Send an account to a user", inline=False)
    embed.add_field(name="!close", value="Close a ticket", inline=False)
    embed.add_field(name="!i [@user]", value="See invite count for a user", inline=False)
    embed.add_field(name="!topinvites", value="Leaderboard of top inviters", inline=False)
    await ctx.send(embed=embed)

@commands.command(name="i")
async def invites(ctx, member: discord.Member = None):
    member = member or ctx.author
    guild_id = ctx.guild.id
    count = user_invites.get(guild_id, {}).get(member.id, 0)
    await ctx.send(embed=make_embed(
        title="📨 Invite Stats",
        description=f"{member.mention} has **{count} invite(s)**."
    ))

@commands.command(name="topinvites")
async def top_invites(ctx):
    guild_id = ctx.guild.id
    invites = user_invites.get(guild_id, {})
    if not invites:
        await ctx.send(embed=make_embed(title="📉 Top Inviters", description="No invite data available."))
        return

    sorted_invites = sorted(invites.items(), key=lambda x: x[1], reverse=True)[:10]
    description = ""
    for i, (user_id, count) in enumerate(sorted_invites, start=1):
        user = ctx.guild.get_member(user_id)
        if user:
            description += f"**{i}.** {user.mention} - `{count}` invites\n"
    await ctx.send(embed=make_embed(title="🏆 Top Inviters", description=description or "No invite data."))

def setup(bot):
    bot.add_command(fgen)
    bot.add_command(pgen)
    bot.add_command(stock)
    bot.add_command(help)
    bot.add_command(invites)
    bot.add_command(top_invites)
