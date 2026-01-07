import hashlib

class packet:
    def __init__(self, id:int, route:str, seq:int, data:str):
        self.__packetID = id
        self.__seq = seq
        self.__route = route
        self.__data = data
    
    def getPacket(self):
        text_packet = f"{self.__packetID}${self.__route}${self.__seq}${self.__data}"
        return text_packet


class outboundPacket(packet):
    def __init__(self, id:int, route:str, seq:int, data:str):
        super().__init__(id, route, seq, data)
        #패킷 정보는 외부접근불가
    
    def getID(self) -> None:
        return self.__packetID

    def getHash(self) -> None:
        return self.__packetHash

    def getRoute(self) -> str:
        return self.__route

    def getData(self) -> str:
        return self.__data

    def getNum(self) -> str:
        return self.__number

    def packet_to_text(self) -> str:
        #패킷 구조 hash/route/number/data
        text_packet = f"{self.__packetID}${self.__route}${self.__seq}${self.__data}"
        return text_packet


class inboundPacket(outboundPacket):
    def __init__(self, id:int, route:str, number:int, data:str, rssi:int):
        super().__init__(id, route, number, data)
        self.__rssi = rssi

    def getRSSI(self) -> int:
        return self.__rssi
