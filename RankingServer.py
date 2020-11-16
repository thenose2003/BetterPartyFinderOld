import pickle
import rankHandler
import socket
import json

version = '0.0.1'
dataFolder = 'data'

HOST = '66.175.233.189'
PORT = 443

class RankingServer:
    def __init__(self, version, dataFolder):
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
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(100)#length of uuid

                        if not data:
                            break

                        rData = data #saves data
                        print(rData)
                        rData = json.loads(rData.decode('utf-8'))

                        #updates rank
                        self.rankChange(rH, rData[0], rData[1], rData[2], rData[3])

                        #sets the veriable to return
                        profile = rH.findProfile(getattr(self, 'floor'+str(rData[1])), rData[0])
                        send = getattr(self, 'floor'+str(rData[1]))[profile]

                        conn.sendall(json.dumps(str(send)).encode()) #returns data

if __name__ == '__main__':
    testList =[ #uuid, skill
        ['NoseThe', 600],
        ['Aquilyawn', 500]]

    #pickle.dump(testList, open("data/floor1.dat", "wb"))

    rs = RankingServer(version, dataFolder).run()
