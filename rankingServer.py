import pickle
import rankHandler
import socket
import json
from multiprocessing import *
import requests

version = '0.0.2'
dataFolder = 'data'

HOST = '127.0.0.1'
PORT = 443

def getUUID(ign):
    return requests.get("https://api.mojang.com/users/profiles/minecraft/"+ign).json()['id']
    return -1

class RankingServer:
    def __init__(self):
        self.version = version
        self.dataFolder = dataFolder

        self.floor1 = pickle.load(open(dataFolder + "/floor1.dat", "rb"))
        self.floor2 = pickle.load(open(dataFolder + "/floor2.dat", "rb"))
        self.floor3 = pickle.load(open(dataFolder + "/floor3.dat", "rb"))
        self.floor4 = pickle.load(open(dataFolder + "/floor4.dat", "rb"))
        self.floor5 = pickle.load(open(dataFolder + "/floor5.dat", "rb"))
        self.floor6 = pickle.load(open(dataFolder + "/floor6.dat", "rb"))

        print('All user data loaded.')
        print('Listening on ', HOST, ':', PORT)

    def load(self):
        self.floor1 = pickle.load(open(dataFolder + "/floor1.dat", "rb"))
        self.floor2 = pickle.load(open(dataFolder + "/floor2.dat", "rb"))
        self.floor3 = pickle.load(open(dataFolder + "/floor3.dat", "rb"))
        self.floor4 = pickle.load(open(dataFolder + "/floor4.dat", "rb"))
        self.floor5 = pickle.load(open(dataFolder + "/floor5.dat", "rb"))
        self.floor6 = pickle.load(open(dataFolder + "/floor6.dat", "rb"))

    def save(self):
        pickle.dump(self.floor1, open(dataFolder + "/floor1.dat", "wb"))
        pickle.dump(self.floor2, open(dataFolder + "/floor2.dat", "wb"))
        pickle.dump(self.floor3, open(dataFolder + "/floor3.dat", "wb"))
        pickle.dump(self.floor4, open(dataFolder + "/floor4.dat", "wb"))
        pickle.dump(self.floor5, open(dataFolder + "/floor5.dat", "wb"))
        pickle.dump(self.floor6, open(dataFolder + "/floor6.dat", "wb"))

    def rankChange(self, rH, uuid, floor, work, totalWork):
        profile = rH.findProfile(getattr(self, 'floor'+str(floor)), uuid)
        #print(getattr(self, 'floor'+str(floor))[profile])
        #def newSkill(self, profile, work, totalWork, **kwargs):
        getattr(self, 'floor'+str(floor))[profile][1] = rH.newSkill(getattr(self, 'floor'+str(floor))[profile], 600, 1000)
        #print(getattr(self, 'floor'+str(floor))[profile])
        self.save()

    def run(self):
        rH = rankHandler.handler(version)
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
#returns data
                self.handleSocket(conn, addr, s, rH)
                #p = Process(target=self.handleSocket, args=(conn, addr, s,))
                #p.start()

    def handleSocket(self, conn, addr, s, rH):
        with conn:
            print('Connected by', addr)
            data = conn.recv(100).decode()#length of imput

            #if not data:
            #    break

            rData = data #saves data
            rData = rData.split('\001')
            print(rData)
            #updates rank
            #rankChange(self, rH, uuid, floor, work, totalWork):
            #list = b'NoseThe\0011\001600\0013000'
            self.rankChange(rH, getUUID(rData[0]), int(rData[1]), int(rData[2]), int(rData[3]))

            #sets the veriable to return
            profile = rH.findProfile(getattr(self, 'floor'+rData[1]), rData[0])
            send = getattr(self, 'floor'+rData[1])[profile]

                #conn.sendall(toBytes(str(send))) #returns data
            conn.sendall(str(rData).encode())
        s.close()

if __name__ == '__main__':
    testList =[ #uuid, skill
        ['NoseThe', 600],
        ['Aquilyawn', 500]]

    #pickle.dump(testList, open("data/floor1.dat", "wb"))

    rs = RankingServer().run()