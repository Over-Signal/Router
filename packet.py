import hashlib

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
    
    def addRoute(self, route:str) -> None:
        self.__route = route

    def getRoute(self) -> str:
        return self.__route
    
    def addData(self, data:str) -> None:
        self.__data = data

    def getData(self) -> str:
        return self.__data
    
    def addNum(self, number:str = 1) -> None:
        self.__number = number

    def getNum(self) -> str:
        return self.__number
    
    def addRSSI(self, rssi:str) -> None:
        self.__rssi = rssi

    def getRSSI(self) -> str:
        return self.__rssi
    
    def hashing(self) -> str:
        processing_text = f"{self.__route}/{self.__number}/{self.__data}"
        hash_str = hashlib.sha256(processing_text.encode('utf-8')).hexdigest()
        return hash_str[:6]

    def packet_to_text(self) -> str:
        #패킷 구조 hash/route/number/data
        self.__packetHash = self.hashing()
        text_packet = f"{self.__packetHash}/{self.__route}/{self.__number}/{self.__data}"
        return text_packet
