#token: ODU1NTQwNTkxMzA3MTI4ODk0.YMz-RA.Jg12YgPaMGScphTuoMMxwuKG6x4
#perm id: 2184396608

import discord
import time

from discord.ext import commands, tasks

TOKEN = 'ODU1NTQwNTkxMzA3MTI4ODk0.YMz-RA.Jg12YgPaMGScphTuoMMxwuKG6x4'
client = commands.Bot(command_prefix = '.')

vc_list = []


@client.event
async def on_ready():
    print("bot is ready")
    await getChannels()
    await checkForBong.start()

@client.event
async def getChannels():
        for server in client.guilds:
            for channel in server.channels:
                if str(channel.type) == 'voice':
                    vc_list.append(channel)

@client.command()
async def joinAndBong(numBongs):
    
    for channels in vc_list:
        if len(channels.members) > 0:
            vc = await channels.connect()
            
            if(vc.is_connected()):
                print("Connected Successfully!")
            
            i = 0
            while(i < numBongs):
                vc.play(discord.FFmpegPCMAudio(source=r"C:\Users\legok\Desktop\bigBenBot\bong-clipped.mp3"))
                
                while(vc.is_playing()):
                    time.sleep(0.1);
                    
                i = i+1
                
            await vc.disconnect()
            if(not vc.is_connected()):
                print("Disconnected Successfully");
        else:
            print("Channel is empty");
    
    
    #await vc_list[0].disconnect()
            # vc_list[i].connect;
            # 
            # for i in range (numBongs):
            #     print("On the Hour!" + str(i+1))
            #     time.sleep(1);

@tasks.loop(seconds=1)
async def checkForBong():
                
    # for i in range (len(vc_list)):
    #     print(vc_list[i].id);
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    if(t.tm_min == t.tm_min and t.tm_sec == t.tm_sec):
        numBongs = t.tm_hour % 12
        await joinAndBong(numBongs)
    # else:
    #     print("Not on the Hour!")
    
    
client.run(TOKEN)