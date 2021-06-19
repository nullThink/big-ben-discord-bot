#token: ODU1NTQwNTkxMzA3MTI4ODk0.YMz-RA.Jg12YgPaMGScphTuoMMxwuKG6x4
#perm id: 2184396608

import discord
import time

from discord.ext import commands, tasks

TOKEN = 'ODU1NTQwNTkxMzA3MTI4ODk0.YMz-RA.Jg12YgPaMGScphTuoMMxwuKG6x4'
client = commands.Bot(command_prefix = '.')

vc_list = []

#TODO: make so user can set time the bot should operate
run_default = True
run_start_hour = 0
run_end_hour = 0
overnight = False

operatingHours = False


@client.command()
async def h(ctx):
    await ctx.send("Command Prefix: .")
    await ctx.send("set_hours: Sets the hours between when the bot should run")
    await ctx.send(" .set_hours start_hour, am/pm, end_hour, am/pm")
    await ctx.send("get_hours: returns the hours of operation")
    await ctx.send("reset: resets the hours of operation and makes run all day")

#gets the working hour range
@client.command()
async def hours(ctx):
    global run_start_hour
    global run_end_hour
    global run_default
    
    if(not run_default):
        await ctx.send(str(run_start_hour) + " - " + str(run_end_hour))
    else:
        await ctx.send("No declared hours.")

@client.command()
async def reset(ctx):
    global run_start_hour
    global run_end_hour
    global run_default
        
    run_start_hour = 0
    run_end_hour = 0
    run_default = True
    await ctx.send("Hours reset!")

@client.command()
async def set_hours(ctx, *args):
    
    global run_start_hour
    global run_end_hour
    global run_default
            global overnight
    
    if(args[0] == "12" and args[1].lower() == "am"):
        run_start_hour = 0
    elif(args[0] == "12" and args[1].lower() == "pm"):
        run_start_hour = 12
    else:
        run_start_hour = int(args[0])
        
        if(args[1].lower() == "pm"):
            run_start_hour = run_start_hour + 12
        
    if(args[2] == "12" and args[3].lower() == "am"):
        run_end_hour = 0
    elif(args[2] == "12" and args[3].lower() == "pm"):
        run_end_hour = 12
    else:
        run_end_hour = int(args[2])
            
        if(args[3].lower() == "pm"):
            run_end_hour = run_end_hour + 12
        
    if(run_end_hour < run_start_hour):
        overnight = True
    
    run_default = False
    
    #print(str(run_start_hour) + " - " + str(run_end_hour))

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

@client.event
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
                    time.sleep(0.01);
                    
                i = i+1
                
            await vc.disconnect()
            if(not vc.is_connected()):
                print("Disconnected Successfully");
        else:
            print("Channel is empty");
    
@client.event
async def time_to_operate(time1, time2):
    
    if(overnight):
        if((time.localtime().tm_hour >= time1 and time.localtime().tm_hour <= time2 + 24)):
            return True
        else:
            return False
    else:
        if((time.localtime().tm_hour >= time1 and time.localtime().tm_hour <= time2)):
            return True
        else:
            return False

@tasks.loop(seconds=1)
async def checkForBong():
    operatingHours = await time_to_operate(run_start_hour, run_end_hour)
    
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    
    if(t.tm_min == 0 and t.tm_sec == 0 and operatingHours):
        
        if(t.tm_hour == 12):
            numBongs = 12
        else:
            numBongs = t.tm_hour % 12
        await joinAndBong(numBongs)
    # else:
    #     print("Not on the Hour!")
    
    
client.run(TOKEN)