import hashlib

class packet:
    def __init__(self, id:int, route:str, seq:int, data:str):
        self._packetID = id
        self._seq = seq
        self._route = route
        self._data = data
    
    def getPacket(self) -> str:
        text_packet = f"{self.__packetID}${self.__route}${self.__seq}${self.__data}"
        return text_packet


class outboundPacket(packet):
    def __init__(self, id:int, route:str, seq:int, data:str):
        '''
        :param id: 0=hello packet, 1=telegram packet, 2=image packet
        '''
        super().__init__(id, route, seq, data)
    
    def getID(self) -> None:
        return self._packetID

    def getRoute(self) -> str:
        return self._route

    def getData(self) -> str:
        return self._data

    def getPacket(self) -> str:
        #패킷 구조 id/route/seq/data
        text_packet = f"{self._packetID}${self._route}${self._seq}${self._data}"
        return text_packet


class inboundPacket(outboundPacket):
    def __init__(self, id:int, route:str, number:int, data:str, rssi:int):
        super().__init__(id, route, number, data)
        self._rssi = rssi

    def getRSSI(self) -> int:
        return self._rssi

    def getPacket(self) -> str:
        #패킷 구조 id/route/seq/data
        text_packet = f"{self._packetID}${self._route}${self._seq}${self._data}${self._rssi}"
        return text_packet