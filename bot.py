import interactions # For command on DS
import os # Required for dotenv
from dotenv import load_dotenv # Load library dotenv
from requests import get
import json

#connection and data pull from Home assistant

api_url = os.getenv('HOMEASSISTANT_URL')  #take HA url from .env file, if the bot and HA has the same host url is something like localhost:8123
tokenHA = os.getenv('HOMEASSISTANT_TOKEN') # take HA token from .env file

headers = { # haders for api access 
    "Authorization": "Bearer " + tokenHA,
    "content-type": "application/json",
}

# the following part probably can be better

# MC server status
def getMCServerStatus():
    MinecraftServerStatusPull = get(api_url + "states/binary_sensor.minecraft_server_status", headers=headers, )
    MinecraftServerStatusJson = json.loads(MinecraftServerStatusPull.text)
    MinecraftServerStatus = MinecraftServerStatusJson["state"] # variable to use
    return MinecraftServerStatus

# MC server latency
def getMCServerLatency():
    MinecraftServerLatencyPull = get(api_url + "states/binary_sensor.minecraft_latency_time", headers=headers, )
    MinecraftServerLatencyJson = json.loads(MinecraftServerLatencyPull.text)
    MinecraftServerLatency = MinecraftServerLatencyJson["state"] # variable to use
    return MinecraftServerLatency

# MC server max player number
def getMCServerPlayerMax():
    MinecraftServerPlayerMaxPull = get(api_url + "states/binary_sensor.minecraft_server_players_max", headers=headers, )
    MinecraftServerPlayerMaxJson = json.loads(MinecraftServerPlayerMaxPull.text)
    MinecraftServerPlayerMax = MinecraftServerPlayerMaxJson["state"] # variable to use
    return MinecraftServerPlayerMax

# MC server online players number
def getMCServerPlayerOnline():
    MinecraftServerPlayerOnlinePull = get(api_url + "states/binary_sensor.minecraft_server_players_online", headers=headers, )
    MinecraftServerPlayerOnlineJson = json.loads(MinecraftServerPlayerOnlinePull.text)
    MinecraftServerPlayerOnline = MinecraftServerPlayerOnlineJson["state"] # variable to use
    return MinecraftServerPlayerOnline

# MC server protocol version
def getMCServerProtocolVersion():
    MinecraftServerProtocolVersionPull = get(api_url + "states/binary_sensor.minecraft_server_protocol_version", headers=headers, )
    MinecraftServerProtocolVersionJson = json.loads(MinecraftServerProtocolVersionPull.text)
    MinecraftServerProtocolVersion = MinecraftServerProtocolVersionJson["state"] # variable to use
    return MinecraftServerProtocolVersion

# MC server version
def getMCServerVersion():
    MinecraftServerVersionPull = get(api_url + "states/binary_sensor.minecraft_server_server_version", headers=headers, )
    MinecraftServerVersionJson = json.loads(MinecraftServerVersionPull.text)
    MinecraftServerVersion = MinecraftServerVersionJson["state"] # variable to use
    return MinecraftServerVersion


load_dotenv() # Load .env file
TOKEN = os.getenv('DISCORD_TOKEN') # Take variable from env file

bot = interactions.Client(token=TOKEN) # Set TOKEN client

@bot.command( # Command test
    name="test",
    description="Testing command",
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("Finalmente!")

@bot.command( #minecraft server info command
    name="InfoServerMinecraft",
    description="Ottieni informazioni sul server",
)
async def serverinfo(ctx: interactions.CommandContext):
    
    MinecraftServerStatus = getMCServerStatus()
    MinecraftServerLatency = getMCServerLatency()
    MinecraftServerVersion = getMCServerVersion()
    MinecraftServerPlayerMax = getMCServerPlayerMax()
    MinecraftServerPlayerOnline = getMCServerPlayerOnline()
    MinecraftServerProtocolVersion = getMCServerProtocolVersion()

    message = "Server status: " + getMCServerStatus() + "\n" + "Latenza: " + getMCServerLatency() + "\n" + "Versione server: " + getMCServerVersion() + "\n" + "giocatori massimi: " + getMCServerPlayerMax() + "\n" + "Numero giocatori online" + getMCServerPlayerOnline() + "\n" + "Versione protocollo: " + MinecraftServerProtocolVersion
    
    
    await ctx.send(message)


bot.start() # Start BOT