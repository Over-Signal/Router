class node:
    def __init__(self, nodeId:int, nodeName:str, IP:list) -> None:
        self.nodeId = nodeId
        self.nodeName = nodeName
        self.subnetIp = IP