import discord
from discord import app_commands
from discord.ext import commands
import database # Import our manual database handler

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- SET YOUR DISCORD ID HERE ---
    # Find this by right-clicking your name in Discord -> Copy User ID
    OWNER_ID =  1366110873248071801 

    # A custom check to make sure ONLY you can run these
    def is_owner():
        def predicate(interaction: discord.Interaction) -> bool:
            return interaction.user.id == Admin.OWNER_ID
        return app_commands.check(predicate)

    @app_commands.command(name="setmoney", description="[OWNER] Manually set a user's wallet balance.")
    @is_owner()
    async def setmoney(self, interaction: discord.Interaction, target: discord.User, amount: int):
        database.set_user_money(target.id, "wallet", amount)
        
        embed = discord.Embed(
            title="💰 Manual Adjustment",
            description=f"Successfully set {target.mention}'s wallet to **${amount:,}**.",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="deletedatauser", description="[OWNER] Completely wipe a user's global data.")
    @is_owner()
    async def deletedatauser(self, interaction: discord.Interaction, target: discord.User):
        data = database.load_data()
        str_id = str(target.id)
        
        if str_id in data:
            del data[str_id]
            database.save_data(data)
            await interaction.response.send_message(f"🗑️ Data for {target.name} has been wiped from the global database.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ No data found for that user.", ephemeral=True)

    # This handles the error if someone who ISN'T you tries to use the command
    @setmoney.error
    @deletedatauser.error
    async def admin_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message("⛔ You do not have permission to use Developer commands.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))
