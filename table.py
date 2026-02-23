import csv
from dataclasses import dataclass

@dataclass
class node:
    nodeId:int
    nodeName:str
    subnetIp:str

class table:
    def __init__(self):
        self.nodeTable=[]
        self.nodeIpTable=[]

    def ip_to_hex(self, ip:str) -> str:
        #255.255.255.255
        result_hex_ip = ''
        for data in ip.split('.'):
            result_hex_ip +=f'{int(data):02x}'

        return result_hex_ip
    
    def ip_to_dec(self, ip_hex:str) -> str:
        result_dec_ip = ''
        for i in range(4):
            result_dec_ip +=f'{int(ip_hex[2*i:2*i+2], 16)}'
            if i != 3:
                result_dec_ip+='.'
                
        return result_dec_ip


    def load_table_file(self) -> None:
        node_table=[]
        try:
            with open('table.csv', 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # 필요한 데이터 타입으로 변환하여 저장
                    # ip일단 str list로 작성함. 차후 소요에 따라서 변경가능
                    ip =  self.ip_to_hex(row['nodeIp'])
                    node_table.append(node(int(row['nodeId']), row['nodeName'], ip))
                    self.nodeIpTable.append(ip)
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
    t.ip_to_dec('b2080c12')
    print(t.nodeIpTable)