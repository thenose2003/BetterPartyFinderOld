import pickle
import rankingServer

dataFolder = 'data'

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

def activateGame(game): #[time, skill average, # of players, qType, [discord, am, want], times checked]
    print(game)
    data = pickle.load(open(dataFolder + "/activeGames.dat", "rb"))
    for i in game[4]:
        game[4][game[4].index(i)] = str(game[4][game[4].index(i)])
    game.append(0)
    data.append(game)
    pickle.dump(data, open(dataFolder + "/activeGames.dat", "wb"))

def findGame(uuid, rs):
    data = openData(rs)

    player = str(uuid)

    for fData in data: #finds authors data
        for aData in fData:
            if player in aData:
                #[uuid(getUUID(ign)), discord tag(ctx.author), skill]
                break

    data = pickle.load(open(dataFolder + "/activeGames.dat", "rb"))
    players = []
    for i in data:
        for p in i[3]:
            if aData[1] in p:
                players = i[3]
                data[data.index(i)][4] += 1

    if players == []:
        return None
    returnData = []
    uData = openData(rs)
    for p in players:
        for aData in uData[0]:
            if p[0] in aData:
                #[uuid(getUUID(ign)), discord tag(ctx.author), skill]
                break
        returnData.append(aData[0])

    if i[4] >= len(i[3]):
        data.pop(data.index(i))
    pickle.dump(data, open(dataFolder + "/activeGames.dat", "wb"))
    return returnData


if __name__ == '__main__':#[time, skill average, # of players, [discord, am, want], number of times checked]
    rs = rankingServer.rankingServer()
    #activateGame([987879776878, 150, 5, [['NotTheNose#6857', 'mage', 'healer'],['TheNose#8293', 'healer', 'tank'],['discord3', 'tank', 'berserker'],['discord4', 'berserker', 'archer'],['discord5', 'archer', 'mage']]])
    print(findGame('9983f7e223de466bb66a81120fbf7f9c', rs))
