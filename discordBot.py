import discord
import requests
import os
from discord.ext import commands
from discord.utils import get
import json
import pickle
import time
import rankingServer
from multiprocessing import *

TOKEN = 'NTkzODEwNTYxOTA5Nzg0NjA0.XRTTLg.SmcFxucDrcmz1ZTCQzp8LopAxGY'
GUILD = 'Bot Test Server'

key = '02255bb1-7d7c-4da8-ba97-4c33df70ebac'

client = commands.Bot(command_prefix='!')

qFloor1 = []
qFloor2 = []
qFloor3 = []
qFloor4 = []
qFloor5 = []
qFloor6 = []
qFloor7 = []

dataFolder = 'data'

#[getUUID(ign), str(ctx.author), 100] format

def saveData(data):
    global rs
    global dataFolder
    pickle.dump(data[0], open(dataFolder + "/floor1.dat", "wb"))
    pickle.dump(data[1], open(dataFolder + "/floor2.dat", "wb"))
    pickle.dump(data[2], open(dataFolder + "/floor3.dat", "wb"))
    pickle.dump(data[3], open(dataFolder + "/floor4.dat", "wb"))
    pickle.dump(data[4], open(dataFolder + "/floor5.dat", "wb"))
    pickle.dump(data[5], open(dataFolder + "/floor6.dat", "wb"))
    pickle.dump(data[6], open(dataFolder + "/floor7.dat", "wb"))

def openData(rs):
    rs.load()
    global floor1
    floor1 = rs.floor1
    global floor2
    floor2 = rs.floor2
    global floor3
    floor3 = rs.floor3
    global floor4
    floor4 = rs.floor4
    global floor5
    floor5 = rs.floor5
    global floor6
    floor6 = rs.floor6
    global floor7
    floor7 = rs.floor7

    return [floor1, floor2, floor3, floor4, floor5, floor6, floor7]

def getUUID(ign):
    return requests.get("https://api.mojang.com/users/profiles/minecraft/"+ign).json()['id']
    return -1

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def compareKey(input):
    return input[1]

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game('with your ranks...'))
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

#@client.event
#async def on_command_error(ctx, error):
#    embed = discord.Embed(title=str(error).capitalize())
#    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def save(ctx):
    if ctx.message.author.guild_permissions.administrator == True:
        saveData(data)
        await ctx.send('Data has been saved!')

@client.command(pass_context=True)
async def register(ctx, ign):
    global rs
    data = openData(rs)
    try:
        ign = ign
    except:
        await ctx.send(embed=discord.Embed(title='Please enter a username with the format !register <in game name>', color=0xff00ff))
        return
    f = requests.get('https://api.hypixel.net/player?key='+key+'&name='+ign).json()
    msg = await ctx.send(embed=discord.Embed(title='Creating your account...', color=0xff00ff))

    if(f['player'] == None):
        await msg.edit(embed=discord.Embed(title='ERROR: This player has never logged into hypixel.', color=0xff00ff))
        return

    try:
        f['player']['socialMedia']['links']['DISCORD']
    except:
        await msg.edit(embed=discord.Embed(title='ERROR: There is no discord account linked to this user.', color=0xff00ff))
        return

    if not(f['player']['socialMedia']['links']['DISCORD'] == str(ctx.author)):
        await msg.edit(embed=discord.Embed(title='ERROR: The discord you are using is not linked to this account.', color=0xff00ff))
        return

    for d in data:
        for i in d:
            if not getUUID(ign) in i and str(f['player']['socialMedia']['links']['DISCORD']) == str(ctx.author):
                pass
            else:
                await msg.edit(embed=discord.Embed(title='ERROR: Account already exists!', color=0xff00ff))
                return
    for i in range(len(data)):
        data[i].append([getUUID(ign), str(ctx.author), 100])
    print(data)
    saveData(data)
    await ctx.message.author.add_roles(discord.utils.get(ctx.author.guild.roles, name='Member'))
    await msg.edit(embed=discord.Embed(title='Account has been created!', color=0xff00ff))

@client.command(pass_context=True, aliases=['que', 'queue', 'joinq', 'joinqueue', 'jq'])
async def q(ctx, dungeonClass, floor, want):
    global qFloor1  #[time, skill average, # of players, want, have, discords]
    global qFloor2
    global qFloor3
    global qFloor4
    global qFloor5
    global qFloor6
    global qFloor7

    #Setting up variables for actually queueing
    floorQ = globals()['qFloor'+str(floor)]
    floorQ.sort(key=compareKey, reverse=True)
    words = ''

    global rs
    data = openData(rs) #[uuid(getUUID(ign)), discord tag(ctx.author), skill]

    msg = await ctx.send(embed=discord.Embed(title="Joining Queue.", color=0xff00ff))

    #------------------------------------
    # Checking if already in queue
    #------------------------------------
    for i in range(6):
        fQ = globals()['qFloor'+str(i+1)]
        fQ.sort(key=compareKey)
        if fQ != []:
            for g in fQ:
                if ctx.author in g[5]:
                    for f in fQ[fQ.index(g)][5]:
                        words += str(f.mention) + '\n'
                    embed = discord.Embed(title='You are already in a waiting room with', color=0xff00ff)
                    embed.add_field(name=str(fQ[fQ.index(g)][2])+' other/s with an average skill of '+str(fQ[fQ.index(g)][1]), value=words)
                    await msg.edit(embed=embed)
                    return


    #------------------------------------
    # Validating all data
    #------------------------------------

    try:#validates floor number
        floor = int(floor)
    except:
        await msg.edit(embed=discord.Embed(title="Please enter a valid floor numer. Ex 4", color=0xff00ff))
        return
    if floor > 6:
        await msg.edit(embed=discord.Embed(title='That foor hasn\'t been released silly', color=0xff00ff))
        return

    #Main class check
    #Bezerker check
    if (dungeonClass.lower() in ('bezerker', 'bez', 'b', 'bezerk', 'bers')):
        dungeonClass = 'b'
    #Mage check
    elif (dungeonClass.lower() in ('mage', 'm')):
        dungeonClass = 'm'
    #Tank check
    elif (dungeonClass.lower() in ('tank', 't')):
        dungeonClass = 't'
    #Archer check
    elif (dungeonClass.lower() in ('archer', 'a', 'arch', 'ar')):
        dungeonClass = 'a'
    #Healer check
    elif (dungeonClass.lower() in ('healer', 'h', 'heal')):
        dungeonClass = 'h'
    #No applicaple class detected
    else:
        await msg.edit(embed=discord.Embed(title='Please enter a valid class.', color=0xff00ff))
        return

    #Class request Check
    #Bezerker check
    if (want.lower() in ('bezerker', 'bez', 'b', 'bezerk', 'bers')):
        want = 'b'
    #Mage check
    elif (want.lower() in ('mage', 'm')):
        want = 'm'
    #Tank check
    elif (want.lower() in ('tank', 't')):
        want = 't'
    #Archer check
    elif (want.lower() in ('archer', 'a', 'arch', 'ar')):
        want = 'a'
    #Healer check
    elif (want.lower() in ('healer', 'h', 'heal')):
        want = 'h'
    #No applicaple class detected
    else:
        await msg.edit(embed=discord.Embed(title='Please enter a valid class request.', color=0xff00ff))
        return

    done = False
    for aData in data[floor-1]: #finds authors data
        if aData[1] == str(ctx.author):
            done = True #[uuid(getUUID(ign)), discord tag(ctx.author), skill]
            break
    if not done:
        return

    #------------------------------------
    # Starting the actual queing Process
    #------------------------------------
    #floorQ =         [[999,        100,         1,       [], ['h'],  []]]
    #                    0      1               2           3     4     5
    words = ''
    if floorQ != []:
        for i in floorQ: #[time, skill average, # of players, want, have, discords]
            maxSkilDif = 100 + (time.time() - i[0])
            if abs(i[1]-aData[2]) < maxSkilDif:
                if dungeonClass in Diff(i[3], i[4]) and want in i[4] and i[2]<5: #Everything with this party is great
                    print('1')
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][3].append(want) # want
                    floorQ[floorQ.index(i)][4].append(dungeonClass) # have
                    floorQ[floorQ.index(i)][5].append(ctx.author) #discords
                    print(floorQ)

                    for f in floorQ[floorQ.index(i)][5]:
                        words += str(f.mention) + '\n'
                    embed = discord.Embed(title='You have joined a waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(floorQ[floorQ.index(i)][1]), value=words)
                    await msg.edit(embed=embed)

                    if floorQ[floorQ.index(i)][2] == 5:
                        for f in floorQ[floorQ.index(i)][5]:
                            words += str(f.mention) + ' '
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        floorQ.pop([floorQ.index(i)])

                    return
                elif dungeonClass in Diff(i[3], i[4]) and i[2]<4: #This party is missing your want
                    print('2')
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][3].append(want) # want
                    floorQ[floorQ.index(i)][4].append(dungeonClass) # have
                    floorQ[floorQ.index(i)][5].append(ctx.author) #discords
                    print(floorQ)

                    for f in floorQ[floorQ.index(i)][5]:
                        words += str(f.mention) + '\n'
                    embed = discord.Embed(title='You have joined a waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(floorQ[floorQ.index(i)][1]), value=words)
                    await msg.edit(embed=embed)

                    if floorQ[floorQ.index(i)][2] == 5:
                        for f in floorQ[floorQ.index(i)][5]:
                            words += str(f.mention) + ' '
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        floorQ.pop([floorQ.index(i)])

                    return
                elif 5 - len(Diff(i[3], i[4])) > 2 or (5 - len(Diff(i[3], i[4])) > 1 and (want in i[3] or want in i[4])): #fill in spot
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][3].append(want) # want
                    floorQ[floorQ.index(i)][4].append(dungeonClass) # have
                    floorQ[floorQ.index(i)][5].append(ctx.author) #discords
                    print(floorQ)

                    for f in floorQ[floorQ.index(i)][5]:
                        words += str(f.mention) + '\n'
                    embed = discord.Embed(title='You have joined a waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(floorQ[floorQ.index(i)][1]), value=words)
                    await msg.edit(embed=embed)

                    if floorQ[floorQ.index(i)][2] == 5:
                        for f in floorQ[floorQ.index(i)][5]:
                            words += str(f.mention) + ' '
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        floorQ.pop([floorQ.index(i)])

                    return
        floorQ.append([time.time(), aData[2], 1, [want], [dungeonClass], [ctx.author]]) # Couldn't find a queue so made a new que
        await msg.edit(embed=discord.Embed(title='Created a new queue.', color=0xff00ff))
    else:
        floorQ.append([time.time(), aData[2], 1, [want], [dungeonClass], [ctx.author]]) # Que is empty making new que
        await msg.edit(embed=discord.Embed(title='Created a new queue.', color=0xff00ff))
    print(floorQ)
    globals()['qFloor'+str(floor)] = floorQ
    #print(globals()['qFloor'+str(floor)][floorQ.index(i)])

@client.command(pass_context=True, aliases=['ql', 'queuelist'])
async def qlist(ctx):
    global qFloor1  #[time, skill average, # of players, want, have, discords]
    global qFloor2
    global qFloor3
    global qFloor4
    global qFloor5
    global qFloor6
    global qFloor7
    words = ''
    msg = await ctx.send(embed=discord.Embed(title="Searching for your queue.", color=0xff00ff))
    for i in range(6):
        fQ = globals()['qFloor'+str(i+1)]
        fQ.sort(key=compareKey)
        if fQ != []:
            for g in fQ:
                if ctx.author in g[5]:
                    for f in fQ[fQ.index(g)][5]:
                        words += str(f.mention) + '\n'
                    embed = discord.Embed(title='You are in a waiting room with', color=0xff00ff)
                    embed.add_field(name=str(fQ[fQ.index(g)][2])+' other/s with an average skill of '+str(fQ[fQ.index(g)][1]), value=words)
                    await msg.edit(embed=embed)
                    return
    embed = discord.Embed(title='You are not currently in a queue.', color=0xff00ff)
    await msg.edit(embed=embed)

@client.command(pass_context=True, aliases=['queueleave', 'l', 'leave'])
async def qleave(ctx):
    global ql
    for i in ql:
        if ctx.author in i:
            ql.pop(ql.index(i))
            embed=discord.Embed(title='You have been removed from queue.', color=0xff00ff)
            await ctx.send(embed = embed)
            return
    embed=discord.Embed(title='You are not currently in queue. ¯\_(ツ)_/¯', color=0xff00ff)
    await ctx.send(embed = embed)

@client.command(pass_context=True, aliases=['r'])
async def rank(ctx):
    msg = await ctx.send(embed=discord.Embed(title="Searching for information", color=0xff00ff))
    data = openData(rs)
    send = ''
    for fData in data: #finds authors data
        for aData in fData:
            if aData[1] == str(ctx.author):
                print(data.index(fData))
                send += 'Floor '+str(data.index(fData)+1)+': '+str(aData[2])+'\n'
                #[uuid(getUUID(ign)), discord tag(ctx.author), skill]
                break
    embed = discord.Embed(title='Ranking Data', color=0xff00ff)
    embed.add_field(name='All found information', value=send)
    await msg.edit(embed=embed)

if __name__ == "__main__":
    global rs
    rs = rankingServer.rankingServer()

    data = openData(rs)

    p = Process(target=rs.run)
    p.start()

    client.run(TOKEN)
8
