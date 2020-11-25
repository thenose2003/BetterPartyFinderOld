import pickle

dataFolder = 'data'

floor1 = pickle.load(open(dataFolder + "/floor1.dat", "rb"))
floor2 = pickle.load(open(dataFolder + "/floor2.dat", "rb"))
floor3 = pickle.load(open(dataFolder + "/floor3.dat", "rb"))
floor4 = pickle.load(open(dataFolder + "/floor4.dat", "rb"))
floor5 = pickle.load(open(dataFolder + "/floor5.dat", "rb"))
floor6 = pickle.load(open(dataFolder + "/floor6.dat", "rb"))
floor7 = pickle.load(open(dataFolder + "/floor7.dat", "rb"))

print(floor1)
print(floor2)
print(floor3)
print(floor4)
print(floor5)
print(floor6)
print(floor7)
