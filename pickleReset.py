import pickle

dataFolder = 'data'

data = [[1, 150, 5, [['Discord1', 'mage', 'healer']], 0]]
pickle.dump(data, open(dataFolder + "/activeGames.dat", "wb"))

raise Exception("Sorry, no numbers below zero")

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 100]]
pickle.dump(data, open(dataFolder + "/floor1.dat", "wb"))

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 101]]
pickle.dump(data, open(dataFolder + "/floor2.dat", "wb"))

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 102]]
pickle.dump(data, open(dataFolder + "/floor3.dat", "wb"))

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 103]]
pickle.dump(data, open(dataFolder + "/floor4.dat", "wb"))

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 104]]
pickle.dump(data, open(dataFolder + "/floor5.dat", "wb"))

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 105]]
pickle.dump(data, open(dataFolder + "/floor6.dat", "wb"))

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 106]]
pickle.dump(data, open(dataFolder + "/floor7.dat", "wb"))

data = [['NotTheNose#6857', 'mage', 6, 'healer']]
pickle.dump(data, open(dataFolder + "/oldQueue.dat", "wb"))

data = [[1, 150, 5, [['Discord1', 'mage', 'healer']], 0]]
pickle.dump(data, open(dataFolder + "/activeGames.dat", "wb"))
