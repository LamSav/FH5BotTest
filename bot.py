import discord
from discord.ext import commands
from discord.ui import Button, View
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the bot token from environment variables
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Intents setup
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Define a view with buttons
class MenuView(View):
    def __init__(self):
        super().__init__(timeout=None)
        # Add Menu button
        self.add_item(Button(label='Menu', style=discord.ButtonStyle.primary, custom_id='menu'))

    @discord.ui.button(label='Verify', style=discord.ButtonStyle.success, custom_id='verify')
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Verification process started.', ephemeral=True)

    @discord.ui.button(label='SelectFile', style=discord.ButtonStyle.secondary, custom_id='selectfile')
    async def selectfile_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('File selection initiated.', ephemeral=True)

    @discord.ui.button(label='Back', style=discord.ButtonStyle.danger, custom_id='back')
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content='Main Menu', view=MenuView())

# Event: on_ready
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

# Command: menu
@bot.command()
async def menu(ctx):
    """Displays a menu with additional options."""
    view = MenuView()
    await ctx.send('Main Menu', view=view)

# Command: ping
@bot.command()
async def ping(ctx):
    """Responds with 'Pong!' to test bot responsiveness."""
    await ctx.send('Pong!')

# Command: shutdown
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    """Shuts down the bot (owner only)."""
    await ctx.send('Shutting down...')
    await bot.close()

# Global error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use a valid command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing arguments for this command.")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("There was an error in the command execution.")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send("An unexpected error occurred.")
        # Log the error
        print(f"An unexpected error occurred: {error}")

# Run the bot
bot.run(TOKEN)
