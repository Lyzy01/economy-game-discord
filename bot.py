import discord
from discord.ext import commands
from dotenv import load_dotenv

from flask import Flask
from threading import Thread

import os

# =========================
# LOAD ENV
# =========================

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

# Put your test server ID here
TEST_GUILD_ID = 1366110873248071801

# =========================
# FLASK SERVER FOR RENDER
# =========================

app = Flask(__name__)

@app.route("/")
def home():
    return "Economy Bot is Online!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port
    )

Thread(target=run_web, daemon=True).start()

# =========================
# DISCORD BOT
# =========================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class EconomyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):

        print("Loading cogs...")

        for filename in os.listdir("./cogs"):

            if filename.endswith(".py"):

                try:
                    await self.load_extension(
                        f"cogs.{filename[:-3]}"
                    )

                    print(
                        f"✅ Loaded {filename}"
                    )

                except Exception as e:

                    print(
                        f"❌ Failed loading {filename}"
                    )

                    print(e)

        print("All cogs loaded.")

bot = EconomyBot()

# =========================
# SYNC GLOBAL
# =========================

@bot.command()
@commands.is_owner()
async def sync(ctx):

    try:

        synced = await bot.tree.sync()

        embed = discord.Embed(
            title="✅ Commands Synced",
            description=f"Synced **{len(synced)}** global commands.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        await ctx.send(
            f"❌ Sync Failed\n```py\n{e}\n```"
        )

# =========================
# SYNC GUILD
# =========================

@bot.command()
@commands.is_owner()
async def syncguild(ctx):

    try:

        guild = discord.Object(
            id=TEST_GUILD_ID
        )

        bot.tree.copy_global_to(
            guild=guild
        )

        synced = await bot.tree.sync(
            guild=guild
        )

        embed = discord.Embed(
            title="⚡ Guild Sync Complete",
            description=f"Synced **{len(synced)}** commands instantly.",
            color=discord.Color.blurple()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        await ctx.send(
            f"❌ Guild Sync Failed\n```py\n{e}\n```"
        )

# =========================
# RELOAD COG
# =========================

@bot.command()
@commands.is_owner()
async def reload(ctx, cog: str):

    try:

        await bot.reload_extension(
            f"cogs.{cog}"
        )

        await ctx.send(
            f"✅ Reloaded `{cog}`"
        )

    except Exception as e:

        await ctx.send(
            f"❌ Reload Failed\n```py\n{e}\n```"
        )

# =========================
# LOAD COG
# =========================

@bot.command()
@commands.is_owner()
async def load(ctx, cog: str):

    try:

        await bot.load_extension(
            f"cogs.{cog}"
        )

        await ctx.send(
            f"✅ Loaded `{cog}`"
        )

    except Exception as e:

        await ctx.send(
            f"❌ Load Failed\n```py\n{e}\n```"
        )

# =========================
# UNLOAD COG
# =========================

@bot.command()
@commands.is_owner()
async def unload(ctx, cog: str):

    try:

        await bot.unload_extension(
            f"cogs.{cog}"
        )

        await ctx.send(
            f"✅ Unloaded `{cog}`"
        )

    except Exception as e:

        await ctx.send(
            f"❌ Unload Failed\n```py\n{e}\n```"
        )

# =========================
# READY EVENT
# =========================

@bot.event
async def on_ready():

    print("\n==========================")
    print(f"Logged in as {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("==========================\n")

    try:

        await bot.change_presence(
            activity=discord.Game(
                name="💰 Economy Simulator"
            )
        )

    except:
        pass

# =========================
# OWNER ERRORS
# =========================

@sync.error
@syncguild.error
@reload.error
@load.error
@unload.error
async def owner_error(ctx, error):

    if isinstance(
        error,
        commands.NotOwner
    ):
        await ctx.send(
            "❌ Only the bot owner can use this command."
        )

# =========================
# START BOT
# =========================

if __name__ == "__main__":
    bot.run(TOKEN)
