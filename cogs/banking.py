import discord
from discord import app_commands
from discord.ext import commands
import database

class Banking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="deposit", description="Deposit your wallet money safely into the bank.")
    async def deposit(self, interaction: discord.Interaction, amount: str):
        user_id = interaction.user.id
        user_data = database.get_user(user_id)
        wallet = user_data["wallet"]

        if amount.lower() == "all":
            transfer_amount = wallet
        else:
            try:
                transfer_amount = int(amount)
            except ValueError:
                await interaction.response.send_message("❌ Please enter a valid number or type 'all'.", ephemeral=True)
                return

        if transfer_amount <= 0:
            await interaction.response.send_message("❌ You must deposit an amount greater than 0.", ephemeral=True)
            return

        if wallet < transfer_amount:
            await interaction.response.send_message("❌ You do not have that much cash in your wallet.", ephemeral=True)
            return

        database.update_user(user_id, "wallet", -transfer_amount)
        database.update_user(user_id, "bank", transfer_amount)
        
        await interaction.response.send_message(f"🏦 Successfully deposited **${transfer_amount:,}** into your bank account.")

    @app_commands.command(name="withdraw", description="Withdraw money from your bank account to your wallet.")
    async def withdraw(self, interaction: discord.Interaction, amount: str):
        user_id = interaction.user.id
        user_data = database.get_user(user_id)
        bank = user_data["bank"]

        if amount.lower() == "all":
            transfer_amount = bank
        else:
            try:
                transfer_amount = int(amount)
            except ValueError:
                await interaction.response.send_message("❌ Please enter a valid number or type 'all'.", ephemeral=True)
                return

        if transfer_amount <= 0:
            await interaction.response.send_message("❌ You must withdraw an amount greater than 0.", ephemeral=True)
            return

        if bank < transfer_amount:
            await interaction.response.send_message("❌ You do not have that much cash in your bank vault.", ephemeral=True)
            return

        database.update_user(user_id, "bank", -transfer_amount)
        database.update_user(user_id, "wallet", transfer_amount)
        
        await interaction.response.send_message(f"💰 Successfully withdrew **${transfer_amount:,}** into your wallet.")

async def setup(bot):
    await bot.add_cog(Banking(bot))
