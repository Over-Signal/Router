import csv

class node:
    def __init__(self, nodeId:int, nodeName:str, IP:list) -> None:
        self.nodeId = nodeId
        self.nodeName = nodeName
        self.subnetIp = IP

class table:
    def __init__(self):
        self.table=[]

    def load_table_file(self) -> list:
        node_table=[]
        try:
            with open('table.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # 필요한 데이터 타입으로 변환하여 저장
                    # ip일단 str list로 작성함. 차후 소요에 따라서 변경가능
                    node_table.append(node(int(row['nodeId']), row['nodeName'], row['nodeIp'].split('.')))
            self.table = node_table

        except:
            print('File Not found')

if __name__ == "__main__":
    t=table()
    t.load_table_file()