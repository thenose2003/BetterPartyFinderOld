import pickle
import rankHandler
import socket
import json
from gameActivationHandler import *
from multiprocessing import *
import requests

version = '0.0.5'
dataFolder = 'data'

HOST = '74.208.27.238' # IP changed to ensure gaming 
PORT = 443

def getUUID(ign):
    return requests.get("https://api.mojang.com/users/profiles/minecraft/"+ign).json()['id']
    return -1

def getIGN(uuid):
    names = requests.get('https://api.mojang.com/user/profiles/' + str(uuid) + '/names').json()
    return names[len(names)-1]['name']

class rankingServer:
    def __init__(self):
        self.version = version
        self.dataFolder = dataFolder

        self.floor1 = pickle.load(open(dataFolder + "/floor1.dat", "rb"))
        self.floor2 = pickle.load(open(dataFolder + "/floor2.dat", "rb"))
        self.floor3 = pickle.load(open(dataFolder + "/floor3.dat", "rb"))
        self.floor4 = pickle.load(open(dataFolder + "/floor4.dat", "rb"))
        self.floor5 = pickle.load(open(dataFolder + "/floor5.dat", "rb"))
        self.floor6 = pickle.load(open(dataFolder + "/floor6.dat", "rb"))
        self.floor7 = pickle.load(open(dataFolder + "/floor7.dat", "rb"))

        print('All user data loaded.')
        print('Listening on ', HOST, ':', PORT)

    def load(self):
        self.floor1 = pickle.load(open(dataFolder + "/floor1.dat", "rb"))
        self.floor2 = pickle.load(open(dataFolder + "/floor2.dat", "rb"))
        self.floor3 = pickle.load(open(dataFolder + "/floor3.dat", "rb"))
        self.floor4 = pickle.load(open(dataFolder + "/floor4.dat", "rb"))
        self.floor5 = pickle.load(open(dataFolder + "/floor5.dat", "rb"))
        self.floor6 = pickle.load(open(dataFolder + "/floor6.dat", "rb"))
        self.floor7 = pickle.load(open(dataFolder + "/floor7.dat", "rb"))

    def save(self):
        pickle.dump(self.floor1, open(dataFolder + "/floor1.dat", "wb"))
        pickle.dump(self.floor2, open(dataFolder + "/floor2.dat", "wb"))
        pickle.dump(self.floor3, open(dataFolder + "/floor3.dat", "wb"))
        pickle.dump(self.floor4, open(dataFolder + "/floor4.dat", "wb"))
        pickle.dump(self.floor5, open(dataFolder + "/floor5.dat", "wb"))
        pickle.dump(self.floor6, open(dataFolder + "/floor6.dat", "wb"))
        pickle.dump(self.floor7, open(dataFolder + "/floor7.dat", "wb"))

    def rankChange(self, rH, uuid, floor, work, totalWork):
        self.load()
        profile = rH.findProfile(getattr(self, 'floor'+str(floor)), uuid)
        print(getattr(self, 'floor'+str(floor)))
        #def newSkill(self, profile, work, totalWork, **kwargs):
        getattr(self, 'floor'+str(floor))[profile][2] = int(rH.newSkill(getattr(self, 'floor'+str(floor))[profile], work, totalWork))
        self.save()

    def run(self):
        rH = rankHandler.handler(version)
        while True:
            #try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((HOST, PORT))
                    s.listen()
                    conn, addr = s.accept()
                    #returns data
                    self.handleSocket(conn, addr, s, rH)
                    #p = Process(target=self.handleSocket, args=(conn, addr, s,))
                    #p.start()
            #except:
                #print('[server] Error in rankingServer.run()')

    def handleSocket(self, conn, addr, s, rH):
        try:
            with conn:
                print('Connected by', addr)
                data = conn.recv(100).decode()#length of imput

                #if not data:
                #    break

                rData = data
                print(rData)
                rData = rData.rstrip() #saves data
                rData = rData.split(':')

                pData = rData

                print(pData)

                #Finds game and sends back players in active game
                players = findGame(getUUID(rData[0]), self)
                if players == None:
                    print('[SERVER] No Game Found')
                    return
                else:
                    send = ''
                    for i in players:
                        send += str(getIGN(i))+':'
                    send = send[:-1]
                    send += '\n'
                    conn.sendall(str(send).encode())

                #Recieve client confirmation
                data = b''
                while data == b'':
                    data = conn.recv(100).rstrip()#length of imput
                rData = data.decode()
                rData = rData.rstrip()#saves data
                rData = rData.split(':')

                print('rData: '+str(rData))
                #for i in rData:
                #    if getUUID(i) not in players:
                #        return

                #updates rank
                #rankChange(self, rH, uuid, floor, work, totalWork):
                #list = b'NoseThe:1:600:3000
                self.rankChange(rH, getUUID(pData[0]), int(pData[1]), int(pData[2]), int(pData[3]))
                self.save()

                #sets the veriable to return
                profile = rH.findProfile(getattr(self, 'floor'+pData[1]), getUUID(pData[0]))
                send = ''
                for i in getattr(self, 'floor'+pData[1])[profile]:
                    send += str(i)+':'
                send = send[:-1]
                send += '\n'

                    #conn.sendall(toBytes(str(send))) #returns data
                conn.sendall(str(send).encode())
        except:
            print("[SERVER] Error in handleSocket")
        #s.close()

if __name__ == '__main__':
    testList =[ #uuid, skill
        ['NoseThe', 600],
        ['Aquilyawn', 500]]

    #pickle.dump(testList, open("data/floor1.dat", "wb"))

    rs = rankingServer().run()
