import discord
from discord import app_commands
from discord.ext import commands
import database
import random
import time

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="balance", description="Check your current wallet and bank balance.")
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        target = member or interaction.user
        user_data = database.get_user(target.id)
        
        wallet = user_data["wallet"]
        bank = user_data["bank"]
        total = wallet + bank

        embed = discord.Embed(title=f"💰 {target.display_name}'s Balance", color=discord.Color.green())
        embed.add_field(name="Wallet", value=f"${wallet:,}", inline=True)
        embed.add_field(name="Bank", value=f"${bank:,}", inline=True)
        embed.add_field(name="Total Net Worth", value=f"${total:,}", inline=False)
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="daily", description="Claim your daily reward of $2,500.")
    async def daily(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data = database.get_user(user_id)
        
        # Initialize a daily cooldown tracker if it doesn't exist
        current_time = int(time.time())
        last_daily = user_data.get("last_daily", 0)
        cooldown = 86400 # 24 hours in seconds
        
        if current_time - last_daily < cooldown:
            remaining = cooldown - (current_time - last_daily)
            hours, remainder = divmod(remaining, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            await interaction.response.send_message(
                f"⏳ You already claimed your daily reward! Come back in **{hours}h {minutes}m {seconds}s**.", 
                ephemeral=True
            )
            return

        # Reward the user
        database.update_user(user_id, "wallet", 2500)
        database.set_user_money(user_id, "last_daily", current_time)
        
        embed = discord.Embed(
            title="📆 Daily Reward",
            description=f"You successfully claimed your daily **$2,500**! It has been added to your wallet.",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="work", description="Shift hours to earn a steady wage.")
    async def work(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user_data = database.get_user(user_id)
        
        current_time = int(time.time())
        last_work = user_data.get("work_cooldown", 0)
        cooldown = 3600 # 1 hour in seconds
        
        if current_time - last_work < cooldown:
            remaining = cooldown - (current_time - last_work)
            minutes, seconds = divmod(remaining, 60)
            
            await interaction.response.send_message(
                f"💼 You are tired from your last shift. Rest for another **{minutes}m {seconds}s**.", 
                ephemeral=True
            )
            return

        # Generate a random payout and scenario
        earnings = random.randint(300, 800)
        scenarios = [
            f"You worked as a software developer and earned **${earnings:,}**.",
            f"You cleaned up the local server rooms and made **${earnings:,}**.",
            f"You streamed some video games and received **${earnings:,}** in viewer donations.",
            f"You helped moderate a massive server and got paid **${earnings:,}**."
        ]
        
        database.update_user(user_id, "wallet", earnings)
        database.set_user_money(user_id, "work_cooldown", current_time)
        
        await interaction.response.send_message(f"💼 {random.choice(scenarios)}")

    @app_commands.command(name="leaderboard", description="View the top 10 richest players globally.")
    async def leaderboard(self, interaction: discord.Interaction):
        data = database.load_data()
        
        # Filter and sort data by total money (wallet + bank)
        sorted_users = sorted(
            [item for item in data.items() if "wallet" in item[1]], 
            key=lambda item: item[1].get("wallet", 0) + item[1].get("bank", 0), 
            reverse=True
        )

        embed = discord.Embed(title="🏆 Global Economy Leaderboard", color=discord.Color.gold())
        
        top_10 = sorted_users[:10]
        description = ""
        
        for index, (user_id, stats) in enumerate(top_10, start=1):
            total_money = stats.get("wallet", 0) + stats.get("bank", 0)
            user = self.bot.get_user(int(user_id))
            username = user.name if user else f"User {user_id}"
            
            description += f"**{index}. {username}** — ${total_money:,}\n"
            
        if not description:
            description = "No global accounts discovered yet!"
            
        embed.description = description
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Economy(bot))
