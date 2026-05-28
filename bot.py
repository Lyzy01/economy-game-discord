import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

# Replace with your Discord Server ID for instant command syncing
TEST_GUILD_ID = 123456789012345678


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
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"✅ Loaded {filename}")

                except Exception as e:
                    print(f"❌ Failed to load {filename}")
                    print(e)

        print("All cogs loaded.")

bot = EconomyBot()


# ==========================
# GLOBAL SYNC
# ==========================

@bot.command(name="sync")
@commands.is_owner()
async def sync(ctx):

    try:
        synced = await bot.tree.sync()

        embed = discord.Embed(
            title="✅ Global Sync Complete",
            description=f"Successfully synced **{len(synced)}** slash commands globally.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ Sync Failed",
            description=f"```py\n{e}\n```",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# ==========================
# TEST SERVER SYNC
# ==========================

@bot.command(name="syncguild")
@commands.is_owner()
async def syncguild(ctx):

    try:

        guild = discord.Object(id=TEST_GUILD_ID)

        bot.tree.copy_global_to(guild=guild)

        synced = await bot.tree.sync(guild=guild)

        embed = discord.Embed(
            title="⚡ Instant Guild Sync",
            description=f"Successfully synced **{len(synced)}** commands to this server.",
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ Guild Sync Failed",
            description=f"```py\n{e}\n```",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# ==========================
# RELOAD COG
# ==========================

@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx, cog: str):

    try:

        await bot.reload_extension(f"cogs.{cog}")

        embed = discord.Embed(
            title="🔄 Cog Reloaded",
            description=f"Successfully reloaded **{cog}**.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ Reload Failed",
            description=f"```py\n{e}\n```",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# ==========================
# LOAD COG
# ==========================

@bot.command(name="load")
@commands.is_owner()
async def load(ctx, cog: str):

    try:

        await bot.load_extension(f"cogs.{cog}")

        embed = discord.Embed(
            title="📥 Cog Loaded",
            description=f"Successfully loaded **{cog}**.",
            color=discord.Color.green()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ Load Failed",
            description=f"```py\n{e}\n```",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# ==========================
# UNLOAD COG
# ==========================

@bot.command(name="unload")
@commands.is_owner()
async def unload(ctx, cog: str):

    try:

        await bot.unload_extension(f"cogs.{cog}")

        embed = discord.Embed(
            title="📤 Cog Unloaded",
            description=f"Successfully unloaded **{cog}**.",
            color=discord.Color.orange()
        )

        await ctx.send(embed=embed)

    except Exception as e:

        embed = discord.Embed(
            title="❌ Unload Failed",
            description=f"```py\n{e}\n```",
            color=discord.Color.red()
        )

        await ctx.send(embed=embed)


# ==========================
# READY EVENT
# ==========================

@bot.event
async def on_ready():

    print("\n==========================")
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print("==========================\n")

    await bot.change_presence(
        activity=discord.Game(
            name="💰 Economy Simulator"
        )
    )


# ==========================
# ERROR HANDLER
# ==========================

@sync.error
@syncguild.error
@reload.error
@load.error
@unload.error
async def owner_error(ctx, error):

    if isinstance(error, commands.NotOwner):
        await ctx.send("❌ Only the bot owner can use this command.")


# ==========================
# START BOT
# ==========================

bot.run(TOKEN)
