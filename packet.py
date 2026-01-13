import collections

class packetCheck:
    def __init__(self):
        self.set = set()
        self.history_queue = collections.deque(maxlen=100)

    def packet_duplicate_check(self, nodeId:int, seq:int):
        '''
        nodeId와 seq를 받아 중복이면 False, 미중복이면 True를 return
        '''
        if (nodeId, seq) in self.set:
            return False #내부존재
        
        self.set.add((nodeId, seq))
        self.history_queue.append((nodeId, seq))

        if(len(self.history_queue) > self.history_queue.maxlen):
            old_data = self.history_queue.popleft()
            self.set.discard(old_data)

        return True

class sequence:
    def __init__(self):
        self.seq= -1
    
    def getSeq(self):
        self.seq = (self.seq + 1) % 256
        return self.seq

class packet:
    def __init__(self, id:int, route:str, seq:int, data:str):
        self._packetID = id
        self._seq = seq
        self._route = route
        self._data = data
    
    def getPacket(self) -> str:
        text_packet = f"{self._packetID}${self._route}${self._seq}${self._data}"
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
    
    def getSeq(self) -> int:
        return self._seq

    def getData(self) -> str:
        return self._data

    def getPacket(self) -> str:
        #패킷 구조 id/route/seq/data
        text_packet = f"{self._packetID}${self._route}${self._seq}${self._data}"
        return text_packet


class inboundPacket(outboundPacket):
    def __init__(self, id:int, route:str, seq:int, data:str, rssi:int):
        super().__init__(id, route, seq, data)
        self._rssi = rssi

    def getRSSI(self) -> int:
        return self._rssi

    def getPacket(self) -> str:
        #패킷 구조 id/route/seq/data
        text_packet = f"{self._packetID}${self._route}${self._seq}${self._data}${self._rssi}"
        return text_packet