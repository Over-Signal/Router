import tkinter as tk
import router

class linkGui:
    def __init__(self, tk:tk, router_link:router.link):
        self.tk = tk
        self.window = tk.Tk()
        self.router = router_link
        
    def send_telegram(self) -> None:
        text=self.tk.StringVar()
        text = self.telegram.get('1.0', self.tk.END) #자동으로 개행문자 삽입됨.
        route = self.router.ip #temp
        sendPacket = self.router.set_outbound_packet(1, route, text[:-1])
        #print(sendPacket.getPacket())
        #self.port.write(sendPacket.encode('utf-8'))
        
        try:
            res = self.router.packet_checker.packet_duplicate_check(self.router.nodeId, sendPacket.getSeq())
            #res = self.router.telegram_processor.telegram_data_save(self.router.nodeId, sendPacket)
            if res:
                self.router.telegram_processor.telegram_data_save(self.router.nodeId, sendPacket)
            else:
                pass
        except:
            print('전송패킷 중복')
        self.router.transmit_q.put(sendPacket.getPacket())
        self.telegram.delete('1.0', self.tk.END)

    def set_window(self):
        '''
        test gui
        '''
        self.window.geometry('500x600')
        self.window.title('송신창 테스트')
        self.tk.Label(self.window, text='전문 입력').grid(row=0, column=0)
        self.telegram=self.tk.Text(self.window, width=30, height=15)
        self.telegram.grid(row=1, column=0, padx=145)
        self.tk.Button(self.window, text='전송', width=10, command=self.send_telegram).grid(row=2, column=0)
        self.tk.Button(self.window, text='종료', width=10, command=self.router.close).grid(row=3, column=0)
        self.window.mainloop()

if __name__ == "__main__":
    ligui = linkGui(tk, router.link())
    ligui.set_window()
    