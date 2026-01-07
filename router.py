import serial
import time
import threading
import table
import packet
from tkinter import*

class sequence:
    def __init__(self):
        self.seq= -1
    
    def getSeq(self):
        self.seq = (self.seq + 1) % 256
        return self.seq

class link:
    def __init__(self, tk, port, boardrate, bootWaitingTime:int = 2):
        self.window = tk
        # self.table = table.table()
        # self.table.load_table_file()
        #self.port = self.open_serial(port, boardrate, bootWaitingTime)
        self.nodeId=0
        self.nodeName=''
        self.ip=[]
        self.runningFlag=True
        self.sequence = sequence()
        # time.sleep(bootWaitingTime) #아두이노 부팅 시간에 따라 조정필요

    def open_serial(self, port:str, boardrate:int, bootWaitingTime:int = 2) -> serial.Serial:
        try:
            openPort = serial.Serial(port, boardrate)
        
        except:
            print("포트 open 불가")
            exit()
        
        time.sleep(bootWaitingTime)
        return openPort

    def set_my_node(self, nodeID:int) -> None:
        '''
        가입자 정보 설정
        '''
        #0:nodeId, 1:nodeName, 2:subnetIp
        node = self.table.table[nodeID]
        self.nodeId = node.nodeId
        self.nodeName = node.nodeName
        self.ip = node.subnetIp

    def set_outbound_packet(self, id:int, route:object, data:str) -> packet.outboundPacket:
        seq = self.sequence.getSeq()
        sendPacket = packet.outboundPacket(id, route, seq, data)
        return sendPacket.getPacket()

    def set_route(self):
        #routing Thread로 이전예정
        print()

    def send_telegram(self) -> None:
        text=StringVar()
        text = self.telegram.get('1.0', END) #자동으로 개행문자 삽입됨.
        route = '0.0.0.0-0.0.0.0-0.0.0.0'
        sendPacket = self.set_outbound_packet(1, route, text)
        #self.port.write(sendPacket.encode('utf-8'))
        print(sendPacket)
        self.telegram.delete('1.0', END)

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
        
    
    def close(self):
        self.port.close()
        self.runningFlag=False
        exit()

    def receive_routine(self):
        while self.runningFlag:
            try:
                if self.port.in_waiting > 0:
                    time.sleep(0.03)#30ms
                    print(self.port.in_waiting) 
                    raw=self.port.read_until()
                    data = raw[:-2].decode()#println 개행문자 자르기
                    #print(data)
                    
            except:
                print('수신에러')
                
            time.sleep(0.01)#10ms

    def run_receiver(self):
        receiver = threading.Thread(target=self.receive_routine, daemon=True)
        receiver.start()

if __name__ == "__main__":
    win = Tk()
    li = link(win, 'COM5', 9600)
    li.set_window()
    #li.set_my_node(2)
    #li.run_receiver()
    win.mainloop()