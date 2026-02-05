import tkinter as tk
import router
from datetime import datetime

class linkGui:
    def __init__(self, tk:tk, router_link:router.link):
        self.tk = tk
        self.window = tk.Tk()
        self.router = router_link
        self.messages = {}
        self.check_vars = {}
        self.msg_counter = 0
        self.dup_counter = True
        
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

    def display_telegram(self, msg_id):
        #telegram [nodeName, data]
        self.telegram_title.config(state="normal")
        self.telegram_context.config(state="normal")
        
        self.telegram_title.delete('1.0', self.tk.END)
        self.telegram_context.delete('1.0', self.tk.END)

        telegram = self.messages.get(msg_id)

        time = telegram['time']
        nodeName = telegram['nodeName']
        context = telegram['content']

        # 2. 내용 입력 (맨 끝에 추가)
        self.telegram_title.insert(1.0, time + " | " + nodeName)
        self.telegram_title.see(tk.END)  # 스크롤을 항상 맨 아래로
        
        # 2. 내용 입력 (맨 끝에 추가)
        self.telegram_context.insert(1.0, context)
        self.telegram_context.see(tk.END)  # 스크롤을 항상 맨 아래로

        # 3. 다시 잠금 (읽기 전용 상태로 복구)
        self.telegram_title.config(state="disabled")

        
        # 3. 다시 잠금 (읽기 전용 상태로 복구)
        self.telegram_context.config(state="disabled")

    def check_queue(self):
        try:
            telegram = self.router.get_telegram()

            if telegram:
                current_time = datetime.now().strftime("%H:%M:%S")
                self.add_message_row(current_time, telegram[0], telegram[1])
        except:
            pass

        finally:
            self.window.after(100, self.check_queue)
        
    def _on_mousewheel(self, event):
        """실제 스크롤 동작을 수행하는 함수"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _apply_scroll_event(self, widget):
        """[핵심] 어떤 위젯이든 스크롤 이벤트가 작동하도록 바인딩하는 함수"""
        widget.bind("<MouseWheel>", self._on_mousewheel)
        

    def _bind_to_mousewheel(self, event):
    # Linux 대응까지 포함
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

# 2. 마우스가 나가면(Leave) -> 해제 (그래야 옆에 입력창에서 스크롤 가능)
    def _unbind_to_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def delete_selected(self):
        ids_to_delete = [mid for mid, var in self.check_vars.items() if var.get()]

        for mid in ids_to_delete:
            self.messages[mid]["widget"].destroy()
            del self.messages[mid]
            del self.check_vars[mid]
        
        self.dup_counter = True

    def select_all(self):
        if self.dup_counter:
            for var in self.check_vars.values():
                var.set(True)
            self.dup_counter = False
        else:
            for var in self.check_vars.values():
                var.set(False)
            self.dup_counter = True

    def add_message_row(self, time:str, nodeName:str, content:str):
        self.msg_counter += 1
        msg_id = self.msg_counter
        
        self.messages[msg_id] = {
            "time": time, "nodeName": nodeName, "content": content
        }

        row_frame = self.tk.Frame(self.scrollable_frame, bg="white", pady=2)
        row_frame.pack(fill="x", expand=True, padx=5, pady=2)

        self._apply_scroll_event(row_frame)
        
        self.messages[msg_id]["widget"] = row_frame

        chk_var = self.tk.BooleanVar()
        self.check_vars[msg_id] = chk_var
        chk = self.tk.Checkbutton(row_frame, variable=chk_var, bg="white")
        chk.pack(side="left")
        self._apply_scroll_event(chk) # 체크박스 위에서도 스크롤 되게

        # 3. 메타 정보 (ID/시간)
        meta_info = f"[{msg_id}] {time}"
        lbl_meta = self.tk.Label(row_frame, text=meta_info, width=12, fg="gray", bg="white", anchor="w")
        lbl_meta.pack(side="left")
        self._apply_scroll_event(lbl_meta) # 라벨 위에서도 스크롤 되게

        # 4. 제목 (클릭 가능)
        lbl_title = self.tk.Label(row_frame, text=nodeName, fg="blue", bg="white", cursor="hand2", anchor="w")
        lbl_title.pack(side="left", fill="x", expand=True)
        self._apply_scroll_event(lbl_title) # 제목 위에서도 스크롤 되게

        # 클릭 이벤트 (스크롤과 별개로 작동)
        lbl_title.bind("<Button-1>", lambda event, mid=msg_id: self.display_telegram(msg_id))

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

        btn_select_all = self.tk.Button(func_frame, text="전체 선택/해제", command=self.select_all)
        btn_select_all.grid(row=0, column=1, padx=(250,0))

        self.canvas = self.tk.Canvas(tele_frame, bg="white", height=800)
        self.scrollbar = self.tk.Scrollbar(tele_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = self.tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        tele_frame.grid_rowconfigure(2, weight=1)
        
        self.canvas.grid(row=2, column=0, sticky='nsew')
        self.scrollbar.grid(row=2, column=1, sticky='ns')

        self.canvas.bind('<Enter>', self._bind_to_mousewheel)
        self.canvas.bind('<Leave>', self._unbind_to_mousewheel)
        self.scrollable_frame.bind('<Enter>', self._bind_to_mousewheel)
        self.scrollable_frame.bind('<Leave>', self._unbind_to_mousewheel)

        telegram_frame = self.tk.Frame(self.window, background="#D6D6D6")
        telegram_frame.grid(row=0, column=3, sticky='ns')

        self.tk.Label(telegram_frame, text="전문 전시").grid(row=0, column=0, sticky='ew')

        self.telegram_title = self.tk.Text(telegram_frame, width=30, height=1, font=("",30,"bold"), state='disabled')
        self.telegram_title.grid(row=1, column=0, padx=15, pady=(15,0))

        self.telegram_context = self.tk.Text(telegram_frame, width=60, height=10, state='disabled', font=("", 15))
        self.telegram_context.grid(row=2, column=0, padx=15, pady=(15,0))
        
        self.input_frame = self.tk.Frame(self.window)
        self.input_frame.grid(row=0, column=4, padx=10, pady=10, sticky='ns')

        self.tk.Label(self.input_frame, text='전문 입력').grid(row=0, column=0)
        self.telegram=self.tk.Text(self.input_frame, width=30, height=15)
        self.telegram.grid(row=1, column=0)
        self.tk.Button(self.input_frame, text='전송', width=10, command=self.send_telegram).grid(row=2, column=0)
        self.tk.Button(self.input_frame, text='종료', width=10, command=self.router.close).grid(row=3, column=0)
        self.window.after(100, self.check_queue)
        self.window.mainloop()

if __name__ == "__main__":
    ligui = linkGui(tk, router.link())
    ligui.set_window()