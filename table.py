import csv

class node:
    def __init__(self, nodeId:int, nodeName:str, IP:str) -> None:
        self.nodeId = nodeId
        self.nodeName = nodeName
        self.subnetIp = IP

class table:
    def __init__(self):
        self.nodeTable=[]
        self.nodeIpTable=[]

    def load_table_file(self) -> None:
        node_table=[]
        try:
            with open('table.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # 필요한 데이터 타입으로 변환하여 저장
                    # ip일단 str list로 작성함. 차후 소요에 따라서 변경가능
                    node_table.append(node(int(row['nodeId']), row['nodeName'], row['nodeIp']))
                    self.nodeIpTable.append(row['nodeIp'])
            self.nodeTable = node_table

        except:
            print('File Not found')

    def check_id(self, ip:str) -> int:
        try:
            for i in range(len(self.nodeTable)):
                if self.nodeTable[i].subnetIp == ip:
                    return i
            raise IndexError
        except:
            print('table에 가입자가 존재하지 않음')

if __name__ == "__main__":
    t=table()
    l=t.load_table_file()
    t.check_id('178.8.12.18')