import tkinter as tk
import router
import datetime

class linkGui:
    def __init__(self, tk:tk, router_link:router.link):
        self.tk = tk
        self.window = tk.Tk()
        self.router = router_link
        self.messages = {}
        self.check_vars = {}
        self.msg_counter = 0
        
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

    def display_telegram(self, telegram:list):
        pass

    def delete_selected(self):
        pass

    def mock_receive_message(self):
        import random
        titles = ["K01.01 적 발견", "K02.14 화력 요청", "K09.05 상황 보고"]
        contents = ["내용 A", "내용 B", "내용 C"]
        idx = random.randint(0, 2)
        self.add_message_row(titles[idx], contents[idx], sender=f"Node-{random.randint(1,5)}")
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def _on_mousewheel(self, event):
        """실제 스크롤 동작을 수행하는 함수"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _apply_scroll_event(self, widget):
        """[핵심] 어떤 위젯이든 스크롤 이벤트가 작동하도록 바인딩하는 함수"""
        widget.bind("<MouseWheel>", self._on_mousewheel)

    def add_message_row(self, title, content, sender="Unknown"):
        self.msg_counter += 1
        msg_id = self.msg_counter
        time_str = datetime.datetime.now().strftime("%H:%M:%S")
        
        self.messages[msg_id] = {
            "title": title, "content": content, "sender": sender, "time": time_str
        }

        row_frame = tk.Frame(self.scrollable_frame, bg="white", pady=2)
        row_frame.pack(fill="x", expand=True, padx=5, pady=2)

        self._apply_scroll_event(row_frame)
        
        self.messages[msg_id]["widget"] = row_frame

        chk_var = tk.BooleanVar()
        self.check_vars[msg_id] = chk_var
        chk = tk.Checkbutton(row_frame, variable=chk_var, bg="white")
        chk.pack(side="left")
        self._apply_scroll_event(chk) # 체크박스 위에서도 스크롤 되게

        # 3. 메타 정보 (ID/시간)
        meta_info = f"[{msg_id}] {time_str}"
        lbl_meta = tk.Label(row_frame, text=meta_info, width=12, fg="gray", bg="white", anchor="w")
        lbl_meta.pack(side="left")
        self._apply_scroll_event(lbl_meta) # 라벨 위에서도 스크롤 되게

        # 4. 제목 (클릭 가능)
        lbl_title = tk.Label(row_frame, text=title, fg="blue", bg="white", cursor="hand2", anchor="w")
        lbl_title.pack(side="left", fill="x", expand=True)
        self._apply_scroll_event(lbl_title) # 제목 위에서도 스크롤 되게

        # 클릭 이벤트 (스크롤과 별개로 작동)
        lbl_title.bind("<Button-1>", lambda event, mid=msg_id: self.display_telegram([]))

    def set_window(self):
        '''
        test gui
        '''
        self.window.geometry('1500x900')
        self.window.title('송신창 테스트')

        tele_frame = self.tk.Frame(self.window)
        tele_frame.grid(row=0, column=0)

        func_frame = self.tk.Frame(tele_frame, bg="#ddd", height=40)
        func_frame.grid(row=0, column=0, columnspan=2, sticky='ew')

        btn_delete = self.tk.Button(func_frame, text="선택 삭제", command=self.delete_selected)
        btn_delete.grid(row=0, column=0)
        
        btn_test = self.tk.Button(func_frame, text="[TEST] 전문 수신", command=self.mock_receive_message)
        btn_test.grid(row=0, column=1, padx=(200,0))

        self.canvas = self.tk.Canvas(tele_frame, bg="white", height=800)
        self.scrollbar = self.tk.Scrollbar(tele_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = self.tk.Frame(tele_frame, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        tele_frame.grid_rowconfigure(1, weight=1)
        
        self.canvas.grid(row=2, column=0, sticky='nsew')
        self.scrollbar.grid(row=2, column=1, sticky='ns')

        telegram_frame = self.tk.Frame(self.window, background="#D6D6D6")
        telegram_frame.grid(row=0, column=3, sticky='ns')

        self.tk.Label(telegram_frame, text="전문 전시").grid(row=0, column=0, sticky='ew')

        self.telegarm_title = self.tk.Text(telegram_frame, width=30, height=1, font=("",30,"bold"), state='disabled')
        self.telegarm_title.grid(row=1, column=0, padx=15, pady=(15,0))

        self.telegram_context = self.tk.Text(telegram_frame, width=60, height=10, state='disabled', font=("", 15))
        self.telegram_context.grid(row=2, column=0, padx=15, pady=(15,0))
        
        self.input_frame = self.tk.Frame(self.window)
        self.input_frame.grid(row=0, column=4, padx=10, pady=10, sticky='ns')

        self.tk.Label(self.input_frame, text='전문 입력').grid(row=0, column=0)
        self.telegram=self.tk.Text(self.input_frame, width=30, height=15)
        self.telegram.grid(row=1, column=0)
        self.tk.Button(self.input_frame, text='전송', width=10, command=self.send_telegram).grid(row=2, column=0)
        self.tk.Button(self.input_frame, text='종료', width=10, command=self.router.close).grid(row=3, column=0)
        self.window.mainloop()

    def check_queue(self):
        telegram = self.router.get_telegram()

        if telegram:
            #데이터 출력
            pass

if __name__ == "__main__":
    ligui = linkGui(tk, router.link())
    ligui.set_window()
    