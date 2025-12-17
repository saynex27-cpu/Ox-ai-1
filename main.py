import os
import discord
from discord.ext import commands
from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ========= ENV =========
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# ========= CONFIG (CHANGE THESE IDS) =========
MOD_CHANNEL_ID = 123456789012345678      # moderator-only channel ID
ANNOUNCE_CHANNEL_ID = 123456789012345678 # announcement channel ID
MOD_ROLE_NAME = "Moderator"              # or Admin

# ========= BOT SETUP =========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

scheduler = AsyncIOScheduler()
scheduler.start()

# ========= READY =========
@bot.event
async def on_ready():
    print(f"🤖 ox ai online as {bot.user}")
    await bot.change_presence(
        activity=discord.Game(name="Deadnex SMP | !help")
    )

# ========= IP MESSAGE =========
IP_MESSAGE = (
    "🌍 **Deadnex SMP**\n"
    "🎮 Address: `play-01.breezecloud.fun`\n"
    "🔌 Port: `19137`\n"
    "🕒 Online 24/7"
)

# ========= COMMANDS =========
@bot.command()
async def ip(ctx):
    await ctx.send(IP_MESSAGE)

@bot.command()
async def help(ctx):
    await ctx.send(
        "**🤖 ox ai Commands**\n"
        "`!ip` → Server IP\n"
        "`!announce YYYY-MM-DD HH:MM message` (mods only)\n"
    )

# ========= ANNOUNCE COMMAND =========
@bot.command()
async def announce(ctx, date: str, time: str, *, message: str):
    # Channel check
    if ctx.channel.id != MOD_CHANNEL_ID:
        return

    # Role check
    if not any(role.name == MOD_ROLE_NAME for role in ctx.author.roles):
        await ctx.send("❌ You are not allowed to do this.")
        return

    try:
        ist = pytz.timezone("Asia/Kolkata")
        run_time = ist.localize(
            datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        )

        async def send_announcement():
            channel = bot.get_channel(ANNOUNCE_CHANNEL_ID)
            await channel.send(f"📢 **Announcement**\n{message}")

        scheduler.add_job(send_announcement, "date", run_date=run_time)
        await ctx.send(f"✅ Announcement scheduled for {date} {time} IST")

    except Exception as e:
        await ctx.send("❌ Format error. Use: YYYY-MM-DD HH:MM message")
        print(e)

# ========= RUN =========
bot.run(DISCORD_TOKEN)
