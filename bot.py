import interactions # For command on DS
import os # Required for dotenv
from dotenv import load_dotenv # Load library dotenv
import requests
import json # For use HA Api
import logging # For logging
import time # For sleeptimer

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
    MinecraftServerStatusPull = requests.get(api_url + "api/states/binary_sensor.minecraft_server_status", headers=headers, ) # Curl Request for take json file
    MinecraftServerStatusJson = json.loads(MinecraftServerStatusPull.text) # Json to object
    MinecraftServerStatus = MinecraftServerStatusJson["state"] # Variable with data
    return MinecraftServerStatus

# MC Server max_player number
def getMCServerPlayerMax():
    MinecraftServerPlayerMaxPull = requests.get(api_url + "api/states/sensor.minecraft_server_players_max", headers=headers, ) # Curl Request for take json file
    MinecraftServerPlayerMaxJson = json.loads(MinecraftServerPlayerMaxPull.text) # Json to object
    MinecraftServerPlayerMax = MinecraftServerPlayerMaxJson["state"] # Variable with data
    return MinecraftServerPlayerMax

# MC Server online_players number
def getMCServerPlayerOnline():
    MinecraftServerPlayerOnlinePull = requests.get(api_url + "api/states/sensor.minecraft_server_players_online", headers=headers, ) # Curl Request for take json file
    MinecraftServerPlayerOnlineJson = json.loads(MinecraftServerPlayerOnlinePull.text) # Json to object
    MinecraftServerPlayerOnline = MinecraftServerPlayerOnlineJson["state"] # Variable with data
    return MinecraftServerPlayerOnline

# MC server version
def getMCServerVersion():
    MinecraftServerVersionPull = requests.get(api_url + "api/states/sensor.minecraft_server_version", headers=headers, ) # Curl Request for take json file
    MinecraftServerVersionJson = json.loads(MinecraftServerVersionPull.text) # Json to object
    MinecraftServerVersion = MinecraftServerVersionJson["state"] # Variable with data
    return MinecraftServerVersion

def startMCServer():
    data = {'entity_id': 'switch.docker_minecraft_server'}
    output = requests.post(api_url + "api/services/switch/turn_on", json=data, headers=headers)

def stopMCServer():
    data = {'entity_id': 'switch.docker_minecraft_server'}
    output = requests.post(api_url + "api/services/switch/turn_off", json=data, headers=headers)

# ------------------------------------

@bot.command( # Minecraft Server Status
    name="infoserverminecraft",
    description="Ottieni informazioni sul server di minecraft",
)
async def servermine_info(ctx: interactions.CommandContext):
    MinecraftServerStatus = getMCServerStatus()
    if (MinecraftServerStatus == "on"):
        MinecraftServerVersion = getMCServerVersion()
        MinecraftServerPlayerMax = getMCServerPlayerMax()
        MinecraftServerPlayerOnline = getMCServerPlayerOnline()
        message = "Server Minecraft v." + MinecraftServerVersion + ": stato " + MinecraftServerStatus + "\nNumero Giocatori: " + MinecraftServerPlayerOnline + "/" + MinecraftServerPlayerMax
        await ctx.send(message)
    else:
        await ctx.send("Il server e' spento!")

@bot.command(
    name="startserverminecraft",
    description="Avvia server di minecraft",
)
async def servermine_start(ctx: interactions.CommandContext):
    if(getMCServerStatus() == "off"):
        startMCServer()
        await ctx.send("Avvio in corso del server minecraft...")
        while(True):
            status = getMCServerStatus()
            if (status == "on"):
                break
            time.sleep(1)
        await ctx.send("Server minecraft avviato!")
    else:
        await ctx.send("Il server e' gia acceso!")

@bot.command(
    name="stopserverminecraft",
    description="Stoppa server di minecraft",
)
async def servermine_start(ctx: interactions.CommandContext):
    if(getMCServerStatus() == "on"):
        stopMCServer()
        await ctx.send("Spegnimento in corso del server minecraft...")
        while(True):
            status = getMCServerStatus()
            if (status == "off"):
                break
            time.sleep(1)
        await ctx.send("Server minecraft spento!")
    else:
        await ctx.send("Il server e' gia spento!")

bot.start() # Start BOT