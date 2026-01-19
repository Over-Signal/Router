import serial
import time
import threading
import table
import queue
import packet
import telegram
from tkinter import*

class link:
    def __init__(self, tk, port, boardrate, bootWaitingTime:int = 2):
        self.window = tk
        self.port = self.open_serial(port, boardrate, bootWaitingTime)

        #가입자/가입자 정보
        self.nodeId=0
        self.nodeName=''
        self.ip=[]
        self.table = table.table()
        self.table.load_table_file()
        
        #수신패킷 처리
        self.runningFlag=True
        self.pri_high_q = queue.Queue()
        self.pri_low_q = queue.Queue()
        self.packet_checker = packet.packetCheck()

        #송신패킷 처리
        self.sequence = packet.sequence()
        self.transmit_q = queue.Queue()

        #전문처리
        self.telegram_processor = telegram.telegramData(self.table.nodeTable)

        #threading/mutex
        self.mutex = threading.Lock()

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
        node = self.table.nodeTable[nodeID]
        self.nodeId = node.nodeId
        self.nodeName = node.nodeName
        self.ip = node.subnetIp

    def set_outbound_packet(self, id:int, route:object, data:str) -> packet.outboundPacket:
        seq = self.sequence.getSeq()
        sendPacket = packet.outboundPacket(id, route, seq, data)
        return sendPacket.getPacket()
    
    def set_inbound_packet(self, data:str) -> packet.inboundPacket:
        #[packetID, route, seq, data, rssi]
        dataSplit = data.split('$')
        return packet.inboundPacket(dataSplit[0], dataSplit[1], dataSplit[2], dataSplit[3], dataSplit[4])
    
    # def hello_packet_process(self, inboundPacket:packet.inboundPacket) -> None:

    def telegram_packet_process(self, inboundPacket:packet.inboundPacket) -> None:
        route = inboundPacket.getRoute()
        route = route.split('-')
        seq = inboundPacket.getSeq()
        if len(route) == 1:#flooding시 송신노드 확인 / 송신노드가 발신노드
            '''
            for문을 돌려서 확인하는게 아니라, packet처럼 set으로 확인하던지, if not in 으로 하던지 해야 깔끔함
            '''
            if route in self.table.nodeTable: #성능저하 발생시 set으로 전환
                id = self.table.check_id(route)
                if self.packet_checker.packet_duplicate_check(id, seq) == True: # 패킷 미중복
                    self.telegram_processor.telegram_data_save(id, inboundPacket)
                    self.transmit_q.put(inboundPacket.getPacket().encode('utf-8'))
                else:
                    pass
            else:
                pass
            # for i in range(len(self.table.nodeTable)):#가입자 table
            #     if self.table.nodeTable[i].subnetIp == route:#route상 ip가 발신가입자 뿐일경우
            #         id = self.table.nodeTable[i].nodeId
            #         if self.packet_checker.packet_duplicate_check(id, seq) == True: #패킷 미중복
            #             '''
            #             전문 전시창 업데이트/전문csv 업데이트/재송신패킷 구성 및 송신
            #             '''
            #             self.telegram_processor.telegram_data_save(id, inboundPacket)
            #             self.transmit_q.put(inboundPacket.getPacket().encode('utf-8'))
            #     else:
            #         print('가입자 확인되지 않음')
        else:
            '''
            라우팅 작업 및 송신
            '''
            pass


    def set_route(self):
        #routing Thread로 이전예정
        print()

    def send_telegram(self) -> None:
        text=StringVar()
        text = self.telegram.get('1.0', END) #자동으로 개행문자 삽입됨.
        route = '0.0.0.0-0.0.0.0-0.0.0.0'#temp
        sendPacket = self.set_outbound_packet(1, route, text)
        #self.port.write(sendPacket.encode('utf-8'))
        self.transmit_q.put(sendPacket)
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

    def thread_receive(self):
        while self.runningFlag:
            try:
                if self.port.in_waiting > 0:
                    time.sleep(0.03)#30ms
                    with self.mutex:
                        print(self.port.in_waiting) 
                        raw=self.port.read_until()
                    if raw:
                        data = raw[:-2].decode()#println 개행문자 자르기
                        pri = raw[0]
                        if pri == 0:
                            self.pri_high_q.put(data)
                        else:
                            self.pri_low_q.put(data)
            except:
                print('수신에러')
                
            time.sleep(0.01)#10ms

    def thread_processor(self):
        target = None
        data = None
        inboundPacket = None
        while self.runningFlag:
            if not self.pri_high_q.empty():
                target = self.pri_high_q
            elif not self.pri_low_q.empty():
                target = self.pri_low_q
            else:
                time.sleep(0.05)#50ms
                continue

            data = target.get()#deque
            inboundPacket = self.set_inbound_packet(data) #패킷 객체 return받음
            match inboundPacket.getID():
                case 0:
                    self.hello_packet_process(inboundPacket)
                case 1:
                    self.telegram_packet_process(inboundPacket)
                case 2:
                    self.image_packet_process(inboundPacket)

            time.sleep(0.05)#50ms

    def thread_transmit(self):
        while self.runningFlag:
            if not self.transmit_q.empty():
                if self.port.in_waiting == 0:
                    with self.mutex:
                        to_transmit_data = self.transmit_q.get()
                        self.port.write(to_transmit_data.encode('utf-8'))
                else:
                    time.sleep(0.01)#10ms
            else:
                continue

    def run_thread(self):
        receiver = threading.Thread(target=self.thread_receive, daemon=True)
        transmitter = threading.Thread(target=self.thread_transmit, daemon=True)
        processor = threading.Thread(target=self.thread_processor, daemon=True)
        receiver.start()
        transmitter.start()
        processor.start()

if __name__ == "__main__":
    win = Tk()
    li = link(win, 'COM5', 9600)
    li.set_window()
    li.set_my_node(2)
    li.run_thread()
    li.telegram_packet_process(packet.inboundPacket(1,'178.8.12.3', 2, 'test', '-19'))
    win.mainloop()