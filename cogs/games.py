import discord
from discord import app_commands
from discord.ext import commands
import random
import time
import database

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_money(self, user_data, amount):
        return user_data["wallet"] >= amount

    # ==========================
    # COINFLIP
    # ==========================

    @app_commands.command(name="coinflip", description="Bet money on a coin flip.")
    async def coinflip(self, interaction: discord.Interaction, amount: int, choice: str):

        user_id = interaction.user.id
        user_data = database.get_user(user_id)

        if amount <= 0:
            return await interaction.response.send_message(
                "❌ Bet must be greater than $0.",
                ephemeral=True
            )

        if not self.has_money(user_data, amount):
            return await interaction.response.send_message(
                "❌ Not enough money in your wallet.",
                ephemeral=True
            )

        choice = choice.lower()

        if choice not in ["heads", "tails"]:
            return await interaction.response.send_message(
                "Choose `heads` or `tails`.",
                ephemeral=True
            )

        result = random.choice(["heads", "tails"])

        if result == choice:
            database.update_user(user_id, "wallet", amount)
            color = discord.Color.green()
            text = f"You won **${amount:,}**!"
        else:
            database.update_user(user_id, "wallet", -amount)
            color = discord.Color.red()
            text = f"You lost **${amount:,}**!"

        embed = discord.Embed(
            title="🪙 Coin Flip",
            description=f"Result: **{result}**\n{text}",
            color=color
        )

        await interaction.response.send_message(embed=embed)

    # ==========================
    # SLOTS
    # ==========================

    @app_commands.command(name="slots", description="Try your luck on the slot machine.")
    async def slots(self, interaction: discord.Interaction, amount: int):

        user_id = interaction.user.id
        user_data = database.get_user(user_id)

        if amount <= 0:
            return await interaction.response.send_message("❌ Invalid amount.", ephemeral=True)

        if not self.has_money(user_data, amount):
            return await interaction.response.send_message("❌ Not enough money.", ephemeral=True)

        symbols = ["🍒", "🍋", "🍇", "💎", "7️⃣"]

        roll = [random.choice(symbols) for _ in range(3)]

        if len(set(roll)) == 1:
            winnings = amount * 5
            database.update_user(user_id, "wallet", winnings)

            result = f"🎉 JACKPOT!\nWon **${winnings:,}**"
            color = discord.Color.gold()

        elif len(set(roll)) == 2:
            winnings = amount * 2
            database.update_user(user_id, "wallet", winnings)

            result = f"✨ Two matched!\nWon **${winnings:,}**"
            color = discord.Color.green()

        else:
            database.update_user(user_id, "wallet", -amount)

            result = f"💀 Lost **${amount:,}**"
            color = discord.Color.red()

        embed = discord.Embed(
            title="🎰 Slots",
            description=f"{' '.join(roll)}\n\n{result}",
            color=color
        )

        await interaction.response.send_message(embed=embed)

    # ==========================
    # CRIME
    # ==========================

    @app_commands.command(name="crime", description="Commit a risky crime.")
    async def crime(self, interaction: discord.Interaction):

        user_id = interaction.user.id
        user_data = database.get_user(user_id)

        now = int(time.time())
        cooldown = 1800

        last = user_data.get("crime_cooldown", 0)

        if now - last < cooldown:
            remaining = cooldown - (now - last)
            mins, secs = divmod(remaining, 60)

            return await interaction.response.send_message(
                f"🚔 Wait {mins}m {secs}s.",
                ephemeral=True
            )

        database.set_user_money(user_id, "crime_cooldown", now)

        if random.randint(1, 100) <= 60:

            reward = random.randint(500, 2000)

            database.update_user(user_id, "wallet", reward)

            await interaction.response.send_message(
                f"💰 Crime successful!\nYou stole **${reward:,}**."
            )

        else:

            fine = random.randint(300, 1000)

            database.update_user(user_id, "wallet", -fine)

            await interaction.response.send_message(
                f"🚓 You got caught!\nLost **${fine:,}**."
            )

    # ==========================
    # FISH
    # ==========================

    @app_commands.command(name="fish", description="Go fishing.")
    async def fish(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        catches = [
            ("🐟 Common Fish", 150),
            ("🐠 Tropical Fish", 300),
            ("🦈 Shark", 1200),
            ("🐡 Pufferfish", 500),
            ("👢 Old Boot", 10)
        ]

        fish_name, value = random.choice(catches)

        database.update_user(user_id, "wallet", value)

        await interaction.response.send_message(
            f"{fish_name}\nSold for **${value:,}**."
        )

    # ==========================
    # MINE
    # ==========================

    @app_commands.command(name="mine", description="Mine valuable ores.")
    async def mine(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        ores = [
            ("🪨 Stone", 50),
            ("⛓️ Iron", 200),
            ("🥇 Gold", 500),
            ("💎 Diamond", 1500),
            ("💠 Emerald", 1000)
        ]

        ore, value = random.choice(ores)

        database.update_user(user_id, "wallet", value)

        await interaction.response.send_message(
            f"You mined {ore}\nWorth **${value:,}**."
        )

    # ==========================
    # HUNT
    # ==========================

    @app_commands.command(name="hunt", description="Go hunting.")
    async def hunt(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        animals = [
            ("🐇 Rabbit", 100),
            ("🦌 Deer", 450),
            ("🐗 Boar", 700),
            ("🐻 Bear", 1500)
        ]

        animal, value = random.choice(animals)

        database.update_user(user_id, "wallet", value)

        await interaction.response.send_message(
            f"You hunted a {animal}\nSold for **${value:,}**."
        )

    # ==========================
    # SCRATCH CARD
    # ==========================

    @app_commands.command(name="scratch", description="Scratch a lottery ticket.")
    async def scratch(self, interaction: discord.Interaction):

        user_id = interaction.user.id

        reward = random.randint(0, 5000)

        database.update_user(user_id, "wallet", reward)

        await interaction.response.send_message(
            f"🎟️ Scratch Card\nYou won **${reward:,}**."
        )

    # ==========================
    # HIGH LOW
    # ==========================

    @app_commands.command(name="highlow", description="Guess higher or lower.")
    async def highlow(
        self,
        interaction: discord.Interaction,
        amount: int,
        guess: str
    ):

        user_id = interaction.user.id
        user_data = database.get_user(user_id)

        if amount <= 0:
            return await interaction.response.send_message(
                "❌ Invalid amount.",
                ephemeral=True
            )

        if not self.has_money(user_data, amount):
            return await interaction.response.send_message(
                "❌ Not enough money.",
                ephemeral=True
            )

        first = random.randint(1, 100)
        second = random.randint(1, 100)

        guess = guess.lower()

        win = (
            guess == "higher" and second > first
        ) or (
            guess == "lower" and second < first
        )

        if win:
            winnings = amount * 2
            database.update_user(user_id, "wallet", winnings)

            result = f"🎉 Won **${winnings:,}**"
            color = discord.Color.green()

        else:
            database.update_user(user_id, "wallet", -amount)

            result = f"💀 Lost **${amount:,}**"
            color = discord.Color.red()

        embed = discord.Embed(
            title="📈 High Low",
            description=f"{first} → {second}\n\n{result}",
            color=color
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Games(bot))
