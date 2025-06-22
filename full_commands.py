import os
import random
import discord
from discord.ext import commands

# Freegen and Premiumgen file paths
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

def make_embed(**kwargs):
    embed = discord.Embed(color=random.randint(0, 0xFFFFFF), **kwargs)
    embed.set_image(url="https://i.imgur.com/9hVqfby.gif")
    return embed

# --- fgen Command ---
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
        await ctx.send(embed=make_embed(title="❌ Invalid Category", description="Use a valid category or `stock`."))
        return

    filepath = fgen_files[category]
    if not os.path.exists(filepath):
        await ctx.send(embed=make_embed(title="❌ File Missing", description=f"{filepath} not found."))
        return

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

# --- pgen Command ---
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
        await ctx.send(embed=make_embed(title="❌ Invalid Category", description="Use a valid category or `stock`."))
        return

    filepath = pgen_files[category]
    if not os.path.exists(filepath):
        await ctx.send(embed=make_embed(title="❌ File Missing", description=f"{filepath} not found."))
        return

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        await ctx.send(embed=make_embed(title="⚠️ Empty Stock", description="No names available."))
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

# --- drop Command ---
@commands.command()
async def drop(ctx):
    combined = list(fgen_files.values()) + list(pgen_files.values())
    random.shuffle(combined)
    for filepath in combined:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            if lines:
                selected = random.choice(lines)
                lines.remove(selected)
                with open(filepath, 'w') as f:
                    f.write('\n'.join(lines) + '\n')
                await ctx.send(embed=make_embed(title="🎉 Drop", description=f"```{selected}```"))
                return
    await ctx.send(embed=make_embed(title="⚠️ All Stock Empty", description="No available accounts or names."))

# --- stock Command ---
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

# --- help Command ---
@commands.command()
async def help(ctx):
    embed = make_embed(title="📘 Help Menu", description="Here are the available commands:")
    embed.add_field(name="!fgen <category>", value="Generate free account", inline=False)
    embed.add_field(name="!pgen <category>", value="Generate premium name", inline=False)
    embed.add_field(name="!stock", value="View stock of all categories", inline=False)
    embed.add_field(name="!drop", value="Drop a random item from stock", inline=False)
    await ctx.send(embed=embed)

# --- Add Commands to Bot ---
def setup(bot):
    bot.add_command(fgen)
    bot.add_command(pgen)
    bot.add_command(drop)
    bot.add_command(stock)
    bot.add_command(help)
