import tkinter
import router

PORT = 'COM5'
HEADLESS = True

def show_node_list(table):
    print('==========================================')
    print('                NODE TABLE                ')
    print('==========================================')
    for node in table:
        print(f"{node.nodeId} | {node.nodeName}")
    print('==========================================')


def run():
    
    if HEADLESS:
        import shell
        run_router = router.link()
        sh = shell.hlShell(run_router)
        node_table = run_router.table.nodeTable
        show_node_list(node_table)
        selectedNode = int(input('사용자 번호 입력>>>'))
        run_router.set_my_node(selectedNode)
        run_router.open_serial(PORT, 9600)
        run_router.run_thread()

    else: 
        window = tkinter.Tk()
        run_router = router.link(window, PORT, 9600)
        node_table = run_router.table.nodeTable
        show_node_list(node_table)
        selectedNode = int(input('사용자 번호 입력>>>'))
        run_router.set_my_node(selectedNode)
        run_router.open_serial(PORT, 9600)
        run_router.run_thread()
        window.mainloop()

if __name__ == "__main__":
    run()