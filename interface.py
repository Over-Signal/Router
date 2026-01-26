import tkinter
import router

class linkGui:
    def __init__(self, tk_window:tkinter, router_link:router.link):
        self.window = tk_window
        self.router = router_link
        
    def send_telegram(self) -> None:
        text=self.window.StringVar()
        text = self.telegram.get('1.0', self.window.END) #자동으로 개행문자 삽입됨.
        route = self.router.ip #temp
        sendPacket = self.router.set_outbound_packet(1, route, text)
        #self.port.write(sendPacket.encode('utf-8'))
        try:
            res = self.router.packet_checker.packet_duplicate_check(self.router.nodeId, sendPacket.getSeq())
            if res:
                pass
            else:
                raise ValueError
        except:
            print('전송패킷 중복')
        self.router.transmit_q.put(sendPacket)
        self.telegram.delete('1.0', self.window.END)

    def set_window(self):
        '''
        test gui
        '''
        self.window.geometry('500x600')
        self.window.title('송신창 테스트')
        self.window.Label(self.window, text='전문 입력').grid(row=0, column=0)
        self.telegram=self.window.Text(self.window, width=30, height=15)
        self.telegram.grid(row=1, column=0, padx=145)
        self.window.Button(self.window, text='전송', width=10, command=self.send_telegram).grid(row=2, column=0)
        self.window.Button(self.window, text='종료', width=10, command=self.router.close).grid(row=3, column=0)