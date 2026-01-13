import csv
import packet
import datetime
import table
from collections import deque
from dataclasses import dataclass

@dataclass
class telegram:
    date:str
    nodeName:str
    seq:int
    data:str
    
    def to_str(self):
        return f'{self.date},{self.nodeName},{self.seq},{self.data}'

class telegramData:
    def __init__(self, nodeList:list, file_name:str = 'telegram.csv') -> None:
        self.telegram_data_list = deque(maxlen=1000)
        self.file_name = file_name
        self.nodeList = nodeList

    def telegram_data_load(self) -> list:
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.telegram_data_list.appendleft(telegram(row['date'], row['nodeName'], row['seq'], row['data']))
        except:
            print('File not found')
    
    def telegram_data_save(self, nodeId:int, inboundPacket:packet.inboundPacket) -> bool:
            data = inboundPacket.getData()
            seq = inboundPacket.getSeq()
            time = datetime.datetime.now()
            date=time.strftime("%Y-%m-%d %H:%M:%S")
            nodeName = self.nodeList[nodeId].nodeName
            rowData = {
                'date':date,
                'nodeName':nodeName,
                'seq':seq,
                'data':data
            }
            with open(self.file_name, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=['date','nodeName','seq','data'])
                writer.writerow(rowData)
        # except:
        #     print('File not found')
                

if __name__ == "__main__":
    t = table.table()
    t.load_table_file()
    tele = telegramData(t.nodeTable)
    p = packet.inboundPacket(1, '178.8.12.3', 24, '작전중 이상 무', '-18')
    tele.telegram_data_save(0, p)
    