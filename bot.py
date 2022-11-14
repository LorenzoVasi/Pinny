import interactions # For command on DS
import os # Required for dotenv
from dotenv import load_dotenv # Load library dotenv
from requests import get # For curl request
import json # For use HA Api
import logging # For logging

load_dotenv() # Load .env file

# Take variable from .env
api_url = os.getenv('HOMEASSISTANT_URL')  # Take HA url from .env file, if the bot and HA has the same host url is something like localhost:8123
tokenHA = os.getenv('HOMEASSISTANT_TOKEN') # Take HA Token from .env file
TOKEN = os.getenv('DISCORD_TOKEN') # Take Discord TOKEN from /env file

headers = { # Headers for API Access 
    "Authorization": "Bearer " + tokenHA,
    "content-type": "application/json",
}

bot = interactions.Client(token=TOKEN) # Set TOKEN client

# -----------------------------------
# Function used in commands

# MC Server Status
def getMCServerStatus():
    MinecraftServerStatusPull = get(api_url + "api/states/binary_sensor.minecraft_server_status", headers=headers, ) # Curl Request for take json file
    MinecraftServerStatusJson = json.loads(MinecraftServerStatusPull.text) # Json to object
    MinecraftServerStatus = MinecraftServerStatusJson["state"] # Variable with data
    return MinecraftServerStatus

# MC Server max_player number
def getMCServerPlayerMax():
    MinecraftServerPlayerMaxPull = get(api_url + "api/states/sensor.minecraft_server_players_max", headers=headers, ) # Curl Request for take json file
    MinecraftServerPlayerMaxJson = json.loads(MinecraftServerPlayerMaxPull.text) # Json to object
    MinecraftServerPlayerMax = MinecraftServerPlayerMaxJson["state"] # Variable with data
    return MinecraftServerPlayerMax

# MC Server online_players number
def getMCServerPlayerOnline():
    MinecraftServerPlayerOnlinePull = get(api_url + "api/states/sensor.minecraft_server_players_online", headers=headers, ) # Curl Request for take json file
    MinecraftServerPlayerOnlineJson = json.loads(MinecraftServerPlayerOnlinePull.text) # Json to object
    MinecraftServerPlayerOnline = MinecraftServerPlayerOnlineJson["state"] # Variable with data
    return MinecraftServerPlayerOnline

# MC server version
def getMCServerVersion():
    MinecraftServerVersionPull = get(api_url + "api/states/sensor.minecraft_server_version", headers=headers, ) # Curl Request for take json file
    MinecraftServerVersionJson = json.loads(MinecraftServerVersionPull.text) # Json to object
    MinecraftServerVersion = MinecraftServerVersionJson["state"] # Variable with data
    return MinecraftServerVersion

# ------------------------------------


@bot.command( # Command Test Event
    name="test",
    description="Testing command",
)
async def my_first_command(ctx: interactions.CommandContext): # Command Test Function of previous event
    await ctx.send("Hi there!") # Send message to DS



@bot.command( # Minecraft Server Status
    name="infoserverminecraft",
    description="Ottieni informazioni sul server",
)
async def serverinfo(ctx: interactions.CommandContext):
    
    MinecraftServerStatus = getMCServerStatus()
    MinecraftServerVersion = getMCServerVersion()
    MinecraftServerPlayerMax = getMCServerPlayerMax()
    MinecraftServerPlayerOnline = getMCServerPlayerOnline()

    message = "Server Minecraft v." + MinecraftServerVersion + ": stato " + MinecraftServerStatus + "\nNumero Giocatori: " + MinecraftServerPlayerOnline + "/" + MinecraftServerPlayerMax
    
    await ctx.send(message)


bot.start() # Start BOT