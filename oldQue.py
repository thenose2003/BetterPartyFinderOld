import pickle
dataFolder = 'data'

def getOldQ(ctx):
    data = pickle.load(open(dataFolder + "/oldQueue.dat", "rb")) # [[discord, class, floor, qType]]
    try:
        for i in data:
            if i[0] == ctx:
                return data[data.index(i)]
    except:
        return None

def saveQ(*args):#class, floor, qType
    data = pickle.load(open(dataFolder + "/oldQueue.dat", "rb"))
    for i in data:
        if i[0] == args[0]:
            data[data.index(i)] = list(args)
            pickle.dump(data, open(dataFolder + "/oldQueue.dat", "wb"))
            return
    data.append(list(args))
    pickle.dump(data, open(dataFolder + "/oldQueue.dat", "wb"))
    return

if __name__ == "__main__":
    saveQ('TheNose#8293', 'm', '6', 'h')
    print("Old Q: " + str(getOldQ('TheNose#8293')))
