class hlShell:
    def __init__(self, router_method):
        self.router = router_method
        
    def run_input(self):
        print("=== Headless Mode Started (Type 'exit' to quit) ===")
        print("명령어 예시: send [메시지] / exit")
        
        try:
            while True:
                user_input = input("\r>> ") 
                
                # 2. 입력값 처리
                if not user_input:
                    continue
                    
                command_parts = user_input.split()
                cmd = command_parts[0].lower()
                
                if cmd == 'exit':
                    self.close()
                    break
                    
                elif cmd == 'send':
                    # 입력 예: send hello world
                    #따옴표 고려
                    if len(command_parts) > 1:
                        msg = " ".join(command_parts[1:])
                        print(msg)
                        # [기존 로직 재사용]
                        # GUI의 send_telegram 로직을 가져와서 실행
                        route = self.router.ip 
                        sendPacket = self.router.set_outbound_packet(1, route, msg)
                        print(sendPacket.getPacket())
                        self.router.transmit_q.put(sendPacket.getPacket())
                        print(f"[System] 전송 큐 등록: {msg}")
                    else:
                        print("[Error] 메시지를 입력하세요. (예: send hello)")
                        
                else:
                    print(f"[Error] 알 수 없는 명령어: {cmd}")
                    
        except KeyboardInterrupt:
            self.router.close()

if __name__ == "__main__":
    sh = hlShell()
    sh.run_input()