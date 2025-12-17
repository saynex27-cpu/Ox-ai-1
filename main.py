import discord
from discord.ext import commands
import os
import aiohttp

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Ox AI is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Example DiscordSRV / Minecraft relay message
    if message.channel.name == "minecraft-chat":
        print(f"[MC] {message.author}: {message.content}")

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong! Ox AI is alive.")

bot.run(TOKEN)
