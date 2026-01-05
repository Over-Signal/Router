import serial
import time
import threading
import table
import packet
from tkinter import*

class link:
    def __init__(self, tk, port, boardrate, bootWaitingTime:int = 2):
        self.window = tk
        # self.table = table.table()
        # self.table.load_table_file()
        # self.port = self.open_serial(port, boardrate, bootWaitingTime)
        self.nodeId=0
        self.nodeName=''
        self.ip=[]
        self.runningFlag=True
        # time.sleep(bootWaitingTime) #아두이노 부팅 시간에 따라 조정필요

    def open_serial(self, port:str, boardrate:int, bootWaitingTime:int = 2) -> serial.Serial:
        try:
            self.port = serial.Serial(port, boardrate)
        
        except:
            print("포트 open 불가")
            exit()
        
        time.sleep(2)

    def set_my_node(self, nodeID:int) -> None:
        '''
        가입자 정보 설정
        '''
        #0:nodeId, 1:nodeName, 2:subnetIp
        node = self.table.table[nodeID]
        self.nodeId = node.nodeId
        self.nodeName = node.nodeName
        self.ip = node.subnetIp

    def set_packet(self, route:object, type:int, data:str) -> packet.packet:
        sendPacket = packet.packet()
        
        #패킷 정의
        sendPacket.addData(data)
        sendPacket.addRoute(route)
        sendPacket.addNum()#패킷 번호의 경우 멀티전송 말고는 쓸 필요가 없다.

        packet_str = sendPacket.packet_to_text()

    def set_route(self):
        #something
        print()

    def send_telegram(self):
        text=StringVar()
        text = self.telegram.get('1.0', END) #자동으로 개행문자 삽입됨.
        self.telegram.delete('1.0', END)
        print(list(text))

    def set_window(self):
        '''
        test gui
        '''
        self.window.geometry('500x600')
        self.window.title('송신창 테스트')
        Label(self.window, text='전문 입력').grid(row=0, column=0)
        self.telegram=Text(self.window, width=30, height=15)
        self.telegram.grid(row=1, column=0, padx=145)
        Button(self.window, text='전송', width=10, command=self.send_telegram).grid(row=2, column=0)
        Button(self.window, text='종료', width=10, command=self.close).grid(row=3, column=0)
        

    def close_serial(self):
        self.port.close()
    
    def close(self):
        #self.close_serial()
        exit()

if __name__ == "__main__":
    win = Tk()
    li = link(win, 'COM5', 9600)
    li.set_window()
    #li.set_my_node(2)
    win.mainloop()
    