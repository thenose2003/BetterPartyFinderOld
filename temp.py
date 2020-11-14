@client.command(pass_context=True, aliases=['que', 'queue', 'joinq', 'joinqueue', 'jq'])
async def q(ctx, floor, class):
    global ql
    global games
    for i in ql:
        if ctx.author in i:
            embed = discord.Embed(title='You are already in queue!')
            await ctx.send(embed=embed)
            return
    if getSkill(str(ctx.author)) == -1:
        embed = discord.Embed(title='You need to register! Register by doing !register <in game name>')
        await ctx.send(embed=embed)
        return
    ql.append([ctx.author, getSkill(str(ctx.author)),int(time.time()), False])
    ql.sort(key=qlELOKey)
    embed = discord.Embed(title='You have joined the game queue.')
    await ctx.send(embed=embed)
    if len(ql) >= 2:
        if int(time.time()) - ql[0][2] < 1:
            ql.sort(key=qlELOKey)
        else:
            long = ql[0]
            ql.sort(key=qlELOKey)
            must = ql.index(long)
            for i in range(len(ql)-1):
                if ql[i][1]-ql[i+1][1] < 91 and i <= must <= i+1:
                    game = [[],[]]
                    for f in range(2):
                        if f % 2 == 0:
                            game[0].append(ql[i+f])
                        else:
                            game[1].append(ql[i+f])
                    game.append(0)
                    game.append(0)
                    players = ''
                    for i in game[0]:
                        players += str(i[0].mention) + ' '
                    for i in game[1]:
                        players += str(i[0].mention) + ' '
                    print(players)
                    print('Creating match')
                    print(game)
                    wordsA = ''
                    wordsB = ''
                    for i in game[0]:
                        wordsA += str(i[0].mention) + ' - ' + str(i[1]) + '\n'
                    for i in game[1]:
                        wordsB += str(i[0].mention) + ' - ' + str(i[1]) + '\n'
                    embed=discord.Embed(title="Players", color=0xff00ff)
                    embed.add_field(name='Team 1', value=wordsA)
                    embed.add_field(name='Team 2', value=wordsB)
                    await ctx.send(content='Found a match ' + players ,embed=embed)
                    for i in game[0]:
                        ql.pop(ql.index(i))
                    for i in game[1]:
                        ql.pop(ql.index(i))
                    games.append(game)
    else:
        print('Que is filling!')
