import interactions # For command on DS
import os # Required for dotenv
from dotenv import load_dotenv # Loading library dotenv

load_dotenv() # Load .env file
TOKEN = os.getenv('DISCORD_TOKEN') # Take variable from it

bot = interactions.Client(token=TOKEN) # Set TOKEN client

@bot.command( # Command test
    name="test",
    description="Testing command",
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Finalmente!")

bot.start() # Start BOT