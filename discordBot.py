import discord
import requests
import os
from discord.ext import commands
from discord.utils import get
import json
import pickle
import time
import rankingServer
from oldQue import *
from gameActivationHandler import *
from multiprocessing import *

TOKEN = '' //  Inset bot token
GUILD = 'Bot Test Server'

key = '' // Api Key

client = commands.Bot(command_prefix='!', case_insensitive=True, description='This is a bot designed to run and manage The Better Party Finder made by NoseThe')

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

def getIGN(uuid):
    names = requests.get('https://api.mojang.com/user/profiles/' + str(uuid) + '/names').json()
    return names[len(names)-1]['name']

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def compareKey(input):
    return input[1]

def returnWanted(list):
    pass

def returnHave(list):
    pass

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

@client.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title=str(error).capitalize())
    await ctx.send(embed=embed)

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
    await msg.edit(embed=discord.Embed(title='Account has been created!', color=0xff00ff))
    await ctx.message.author.edit(nick=getIGN(getUUID(ign)))
    await ctx.message.author.add_roles(discord.utils.get(ctx.author.guild.roles, name='Member'))

@client.command(pass_context=True, aliases=['que', 'queue', 'joinq', 'joinqueue', 'jq'])
async def q(ctx, *args):
    global qFloor1  #[time, skill average, # of players, [discord, am, want]]
    global qFloor2
    global qFloor3
    global qFloor4
    global qFloor5
    global qFloor6
    global qFloor7

    msg = await ctx.send(embed=discord.Embed(title="Joining Queue.", color=0xff00ff))

#------------------------------------
# Get old queue data
#------------------------------------
    args = list(args)
    oldQ = getOldQ(str(ctx.author))
    qType = 0

    if oldQ == None or (args != []):
        try:
            dungeonClass = args[0]
            floor = args[1]
            try:
                want = args[2]
            except:
                want = 'fill'
            saveQ(str(ctx.author), dungeonClass, floor, want)
        except:
            embed = discord.Embed(title="Oops you did something wrong!", color=0xff00ff)
            embed.add_field(name='Be sure to use the correct syntax.\n!queue <class> <floor> <que type>', value='If you need help with the different que types be suer to check out the video or look in #announcements')#0001
            await msg.edit(embed=embed)
            return
    else:
        dungeonClass = oldQ[1]
        floor = oldQ[2]
        want = oldQ[3]

    #------------------------------------
    # Validating all data
    #------------------------------------
    #Main class check
    #Bezerker check
    if (dungeonClass.lower() in ('bezerker', 'bez', 'b', 'bezerk', 'bers')):
        dungeonClass = 'berserker'
    #Mage check
    elif (dungeonClass.lower() in ('mage', 'm')):
        dungeonClass = 'mage'
    #Tank check
    elif (dungeonClass.lower() in ('tank', 't')):
        dungeonClass = 'tank'
    #Archer check
    elif (dungeonClass.lower() in ('archer', 'a', 'arch', 'ar')):
        dungeonClass = 'archer'
    #Healer check
    elif (dungeonClass.lower() in ('healer', 'h', 'heal')):
        dungeonClass = 'healer'
    #No applicaple class detected
    else:
        await msg.edit(embed=discord.Embed(title='Please enter a valid class.', color=0xff00ff))
        return

    #Class request Check
    #Bezerker check
    if (want.lower() in ('berserker', 'ber', 'b', 'bezerk', 'bers')):
        want = 'berserker'
    #Mage check
    elif (want.lower() in ('mage', 'm')):
        want = 'mage'
    #Tank check
    elif (want.lower() in ('tank', 't')):
        want = 'tank'
    #Archer check
    elif (want.lower() in ('archer', 'a', 'arch', 'ar')):
        want = 'archer'
    #Healer check
    elif (want.lower() in ('healer', 'h', 'heal')):
        want = 'healer'
    #Cheching for other types
    elif (want in ('fill', 'f')):
        qType = 0
    elif (want in ('no-dupes', 'nd', 'no', 'dupe', 'dupes')):
        qType = 1
    elif (want in ('hype', 'hy', 'hyper', 'hyperion')):
        qType = 2
    elif (want in ('mage', 'healer', 'berserker', 'tank', 'archer')):
        qType = 3
    else:
        await msg.edit(embed=discord.Embed(title='Please enter a valid class or que type request.', color=0xff00ff))
        return

    try:#validates floor number
        floor = int(floor)
    except:
        await msg.edit(embed=discord.Embed(title="Please enter a valid floor numer. Ex 4", color=0xff00ff))
        return
    if floor > 7 or floor < 1:
        await msg.edit(embed=discord.Embed(title='That floor dosnt exist!', color=0xff00ff))
        return

    #Setting up variables for actually queueing
    floorQ = globals()['qFloor'+str(floor)]
    floorQ.sort(key=compareKey, reverse=True)
    words = ''

    global rs
    data = openData(rs) #[uuid(getUUID(ign)), discord tag(ctx.author), skill]

    #   Que types
    #----------------
    # 0 - Fill
    # 1 - No Dupes
    # 2 - Hyperion
    # 3 - Class request


    #------------------------------------
    # Checking if already in queue
    #------------------------------------
    for i in range(6):
        fQ = globals()['qFloor'+str(i+1)]
        fQ.sort(key=compareKey)
        if fQ != []:
            for g in fQ:
                for r in g[4]:
                    if ctx.author in r:
                        for f in fQ[fQ.index(g)][4]:
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                        embed = discord.Embed(title='You are in a floor ' + str(i+1) + ' waiting room with', color=0xff00ff)
                        embed.add_field(name=str(fQ[fQ.index(g)][2])+' other/s with an average skill of '+str(int(fQ[fQ.index(g)][1])), value=words)
                        await msg.edit(embed=embed)
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
    #   Que types
    # 0 - Fill
    # 1 - No Dupes
    # 2 - Hyperion
    # 3 - Class request
    # You can also request to fill
    words = ''
    if floorQ != []:
        for i in floorQ: #[time, skill average, # of players, q type, [discord, class]]
            maxSkilDif = 30 + (time.time() - i[0])
            if abs(i[1]-aData[2]) < maxSkilDif:

                if i[3] == 0 and (qType == 0 or (qType == 3 and want in [item for sublist in i[4] for item in sublist])): # 0 - Fill group
                    #Join the queue
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1.0)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][4].append([ctx.author, dungeonClass]) # have

                    for f in floorQ[floorQ.index(i)][4]:
                        words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                    embed = discord.Embed(title='You have joined a floor ' + str(floor) + ' waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(int(floorQ[floorQ.index(i)][1])), value=words)
                    await msg.edit(embed=embed)

                    #Check if q is full
                    if floorQ[floorQ.index(i)][2] == 5:
                        words = ''
                        for f in floorQ[floorQ.index(i)][4]:
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        activateGame(floorQ.pop(floorQ.index(i)))
                    return
                elif i[3] == 1 and (dungeonClass not in [item for sublist in i[4] for item in sublist] and (qType == 0 or qType == 1)): # 1 - No Dupes
                    #Join the queue
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1.0)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][4].append([ctx.author, dungeonClass]) # have

                    for f in floorQ[floorQ.index(i)][4]:
                        words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                    embed = discord.Embed(title='You have joined a floor ' + str(floor) + ' waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(int(floorQ[floorQ.index(i)][1])), value=words)
                    await msg.edit(embed=embed)

                    #Check if q is full
                    if floorQ[floorQ.index(i)][2] == 5:
                        words = ''
                        for f in floorQ[floorQ.index(i)][4]:
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        activateGame(floorQ.pop(floorQ.index(i)))
                    return
                elif i[3] == 2 and (discord.utils.get(ctx.guild.roles, name='Hyperion') in ctx.author.roles and (qType == 0 or qType == 2)): # 2 - Hyperion
                    #Join the queue
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1.0)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][4].append([ctx.author, dungeonClass]) # have
                    floorQ[floorQ.index(i)][5].append(want)

                    for f in floorQ[floorQ.index(i)][4]:
                        words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                    embed = discord.Embed(title='You have joined a floor ' + str(floor) + ' waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(int(floorQ[floorQ.index(i)][1])), value=words)
                    await msg.edit(embed=embed)

                    #Check if q is full
                    if floorQ[floorQ.index(i)][2] == 5:
                        words = ''
                        for f in floorQ[floorQ.index(i)][4]:
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        activateGame(floorQ.pop(floorQ.index(i)))
                    return
                elif i[3] == 3 and (dungeonClass in i[5] or i[2]+len(i[5]<5) and (qType == 0 or qType == 3)): # 3 - Class request
                    #Join the queue
                    floorQ[floorQ.index(i)][1] = ((floorQ[floorQ.index(i)][1]*floorQ[floorQ.index(i)][2])+aData[2])/(floorQ[floorQ.index(i)][2]+1.0)# skillaverage
                    floorQ[floorQ.index(i)][2] += 1 # # of players
                    floorQ[floorQ.index(i)][4].append([ctx.author, dungeonClass]) # have
                    floorQ[floorQ.index(i)][5].pop(i[5].index(dungeonClass))

                    for f in floorQ[floorQ.index(i)][4]:
                        words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                    embed = discord.Embed(title='You have joined a floor ' + str(floor) + ' waiting room with', color=0xff00ff)
                    embed.add_field(name=str(floorQ[floorQ.index(i)][2])+' other/s with an average skill of '+str(int(floorQ[floorQ.index(i)][1])), value=words)
                    await msg.edit(embed=embed)

                    #Check if q is full
                    if floorQ[floorQ.index(i)][2] == 5:
                        words = ''
                        for f in floorQ[floorQ.index(i)][4]:
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                        embed = discord.Embed(title='Queue has been filled!', color=0xff00ff)
                        await msg.edit(embed=embed, content=words)
                        activateGame(floorQ.pop(floorQ.index(i)))
                    return

        if qType == 0: #Fill q
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]]])
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
        elif qType == 1:# No dupes
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]]])
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
        elif qType == 2 and (discord.utils.get(ctx.guild.roles, name='Hyperion') in ctx.author.roles): # Hyperion
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]]])
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
        elif qType == 2: #If the person dosn't have a hyperion
            await msg.edit(embed=discord.Embed(title='You don\'t have the Hyperion rank! Apply for it in #hyperion-applications', color=0xff00ff))
        elif qType == 3: #Class request
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]], [want]]) # Couldn't find a queue so made a new que
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
    else:
        if qType == 0: #Fill q
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]]])
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
        elif qType == 1:# No dupes
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]]])
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
        elif qType == 2 and (discord.utils.get(ctx.guild.roles, name='Hyperion') in ctx.author.roles): # Hyperion
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]]])
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
        elif qType == 2: #If the person dosn't have a hyperion
            await msg.edit(embed=discord.Embed(title='You don\'t have the Hyperion rank! Apply for it in #hyperion-applications', color=0xff00ff))
        elif qType == 3: #Class request
            floorQ.append([time.time(), aData[2], 1, qType, [[ctx.author, dungeonClass]], want]) # Couldn't find a queue so made a new que
            await msg.edit(embed=discord.Embed(title='Created a new floor ' + str(floor) + ' queue.', color=0xff00ff))
    print(floorQ)
    globals()['qFloor'+str(floor)] = floorQ
    #print(globals()['qFloor'+str(floor)][floorQ.index(i)])

@client.command(pass_context=True, aliases=['ql', 'queuelist'])
async def qlist(ctx):
    global qFloor1  #[time, skill average, # of players, q type, [discord, class]]
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
                for r in g[4]:
                    if ctx.author in r:
                        for f in fQ[fQ.index(g)][4]:
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'
                        embed = discord.Embed(title='You are in a floor ' + str(i+1) + ' waiting room with', color=0xff00ff)
                        embed.add_field(name=str(fQ[fQ.index(g)][2])+' other/s with an average skill of '+str(int(fQ[fQ.index(g)][1])), value=words)
                        await msg.edit(embed=embed)
                        return
    embed = discord.Embed(title='You are not currently in a queue.', color=0xff00ff)
    await msg.edit(embed=embed)

@client.command(pass_context=True, aliases=['queueleave', 'l', 'leave'])
async def qleave(ctx):
    global qFloor1  #[time, skill average, # of players, q type, [discord, class]]
    global qFloor2
    global qFloor3
    global qFloor4
    global qFloor5
    global qFloor6
    global qFloor7
    words = ''
    msg = await ctx.send(embed=discord.Embed(title="Searching for your queue.", color=0xff00ff))

    global rs
    data = openData(rs)

    player = str(ctx.author)

    for fData in data: #finds authors data
        for aData in fData:
            if player in aData:
                #[uuid(getUUID(ign)), discord tag(ctx.author), skill]
                break

    for i in range(6):
        fQ = globals()['qFloor'+str(i+1)]
        fQ.sort(key=compareKey)
        if fQ != []:
            for g in fQ:
                for r in g[4]:
                    if ctx.author in r:
                        for f in fQ[fQ.index(g)][4]: #fQ[fQ.index(g)]
                            words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0]) + '\n'#[time, skill average, # of players, q type, [discord, class]]
                        embed = discord.Embed(title=str(ctx.author)+' has left the queue.', color=0xff00ff)
                        globals()['qFloor'+str(i+1)][fQ.index(g)][1] = ((globals()['qFloor'+str(i+1)][fQ.index(g)][1]*globals()['qFloor'+str(i+1)][fQ.index(g)][2]) - aData[2]) * (globals()['qFloor'+str(i+1)][fQ.index(g)][2] - 1)
                        globals()['qFloor'+str(i+1)][fQ.index(g)][2] += -1
                        globals()['qFloor'+str(i+1)][fQ.index(g)][4].pop(g[4].index(r))

                        if globals()['qFloor'+str(i+1)][fQ.index(g)][2] == 0:
                            globals()['qFloor'+str(i+1)].pop(fQ.index(g))
                            embed = discord.Embed(title='Queue was empty and has been destroyed.', color=0xff00ff)
                            await msg.edit(embed=embed)
                        else:
                            words = ''
                            for f in fQ[fQ.index(g)][4]: #fQ[fQ.index(g)]
                                words += '**' + str(f[1]).capitalize() + ':** ' + str(f[0].mention) + '\n'#[time, skill average, # of players, q type, [discord, class]]
                            embed = discord.Embed(title=str(ctx.author)+' has left your queue.', color=0xff00ff)

                            embed.add_field(name=str(fQ[fQ.index(g)][2])+' other/s with an average skill of '+str(int(fQ[fQ.index(g)][1])), value=words)
                            await msg.edit(embed=embed)
                        return
    embed = discord.Embed(title='You are not currently in a queue.', color=0xff00ff)
    await msg.edit(embed=embed)

@client.command(pass_context=True, aliases=['r'])
async def rank(ctx, *args):
    if args == ():
        player = str(ctx.author)
    else:
        player = getUUID(args[0])
    msg = await ctx.send(embed=discord.Embed(title="Searching for information", color=0xff00ff))
    data = openData(rs)
    send = ''
    for fData in data: #finds authors data
        for aData in fData:
            if player in aData:
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
