import discord_rpc
from time import mktime, sleep


discord = discord_rpc.DiscordIpcClient.for_platform()
print("RPC connection successful.")

while True:
    status, voice_status = discord.get_voice_status()
    print(voice_status["data"]["mute"])
    sleep(0.1)
