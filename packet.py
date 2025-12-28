class packet:
    def __init__(self):
        #패킷 정보는 외부접근불가
        self.__packetHash=''
        self.__route=''
        self.__number=''
        self.__data=''
        self.__rssi=''
        
    def addHash(self, hash:str) -> None:
        self.__packetHash = hash

    def getHash(self) -> None:
        return self.__packetHash
    
    def addRoute(self, route) -> None:
        self.__route = route

    def getRoute(self) -> str:
        return self.__route
    
    def addData(self, data:str) -> None:
        self.__data = data

    def getData(self) -> str:
        return self.__data
    
    def addNum(self, number:str) -> None:
        self.__number = number

    def getNum(self) -> str:
        return self.__number
    
    def addRSSI(self, rssi:str) -> None:
        self.__rssi = rssi

    def getRSSI(self) -> str:
        return self.__rssi

class textPacket(packet):
    def __init__(self):
        super().__init__()
