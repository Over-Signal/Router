import serial
import time

'''
아래 클래스를 기반으로 비동기처리, 병렬처리를 통해 아두이노와 Serial 통신
'''
class link:
    def __init__(self, port:str, boardrate:int, bootWaitingTime:int = 2):
        self.port = serial.Serial(port, boardrate)
        time.sleep(bootWaitingTime) #아두이노 부팅 시간에 따라 조정필요

    def send_packet(self, data:str) -> None: #예외처리 필요 시 return 타입 명시하고 사용
        buf_data = data + '\n'
        self.port.write(buf_data.encode('utf-8'))
        time.sleep(0.2)

    def receive_packet(self) -> str:
        #버퍼 재검사 후 읽기
        if self.port.in_waiting > 0:
            data = self.port.read_all()
            data = data.decode('utf-8').strip()
            return data
        
    def connection_close(self) -> None:
        self.port.close()
