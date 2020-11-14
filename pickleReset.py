import pickle

dataFolder = 'data'

data = [['9983f7e223de466bb66a81120fbf7f9c', 'NotTheNose#6857', 100]]

pickle.dump(data, open(dataFolder + "/floor1.dat", "wb"))
pickle.dump(data, open(dataFolder + "/floor2.dat", "wb"))
pickle.dump(data, open(dataFolder + "/floor3.dat", "wb"))
pickle.dump(data, open(dataFolder + "/floor4.dat", "wb"))
pickle.dump(data, open(dataFolder + "/floor5.dat", "wb"))
pickle.dump(data, open(dataFolder + "/floor6.dat", "wb"))
