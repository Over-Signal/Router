import router
import shell
import interface

try:
    import tkinter as tk
    HEADLESS = False
    
except ImportError:
    import shell
    HEADLESS = True

PORT = 'COM5'
# HEADLESS = True

def show_node_list(table):
    print('==========================================')
    print('                NODE TABLE                ')
    print('==========================================')
    for node in table:
        print(f"{node.nodeId} | {node.nodeName}")
    print('==========================================')

def run():
    if HEADLESS:
        run_router = router.link(headless=HEADLESS)
        sh = shell.hlShell(run_router)
        node_table = run_router.table.nodeTable
        show_node_list(node_table)
        selectedNode = int(input('사용자 번호 입력>>>'))
        run_router.set_my_node(selectedNode)
        run_router.open_serial(PORT, 9600)
        run_router.run_thread()
        sh.run_thread()
        sh.run_input()

    else:#gui
        rt = router.link()
        node_table = rt.table.nodeTable
        show_node_list(node_table)
        selectedNode = int(input('사용자 번호 입력>>>'))
        rt.set_my_node(selectedNode)
        rt.open_serial(PORT, 9600)
        rt.run_thread()
        ui = interface.linkGui(tk, rt)
        ui.set_window()

if __name__ == "__main__":
    run()