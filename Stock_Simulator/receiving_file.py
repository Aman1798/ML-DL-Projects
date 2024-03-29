import socket
from threading import Thread
from taipy.gui import Gui, State, invoke_callback, get_state_id
import pandas as pd

HOST = "127.0.0.1"
PORT = 5050

state_id_list = []

def on_init(state: State):
    state_id = get_state_id(state)
    if (state_id := get_state_id(state)) is not None:
        state_id_list.append(state_id)

def client_handler(gui: Gui, state_id_list: list):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    conn, _ = s.accept()
    while True:
        if data := conn.recv(1024):
            print(f"Data received: {data.decode()}")
            if hasattr(gui, "_server") and state_id_list:
                invoke_callback(
                    gui, state_id_list[0], update_received_data, (str(data.decode()),)
                )
        else:
            print("Connection closed")
            break


def update_received_data(state: State, val):
    state.received_data = val
    tempdata = state.data
    tempdata = ["Price"][0] = tempdata["Price"][1]
    tempdata = ["Price"][1] = tempdata["Price"][2]
    tempdata = ["Price"][2] = tempdata["Price"][3]
    tempdata = ["Price"][3] = state.received_data.split(",")[0]
    state.company_name = state.received_data.split(",")[1]
    state.data = tempdata

title = "STOCK-SIMULATOR"
path = "logo.png"
company_name = "Tata"
company_minp = 340
company_maxp = 740


def submit(state):
    print("submit")
    print(state.path)
    print(state.company_minp)

    with open("data.txt", "w") as f:
        f.write(f"{state.company_name},{state.company_minp},{state.company_maxp}")


data = {
    "Date": pd.date_range("2024-01-01", periods=4, freq="D"),
    "Price": [222, 419.7, 662.7, 323.5],


}


received_data = "No Data"

md = """
<|text-center |
<|{path}|image|>

<|{title}|hover_text=Welcome to Stock Simulator|>

Name of Stock: <|{company_name}|input|>

Min Price: <|{company_minp}|input|>

Max Price: <|{company_maxp}|input|>

<|Submit|button|on_action=submit|>

<|{title}|hover_text={company_name}|>

<|{data}|chart|mode=lines|x=Date|y[1]=Price|line[1]=dash|>


>




"""
gui = Gui(page=md)

t = Thread(
    target=client_handler,
    args=(
        gui,
        state_id_list,
    ),
)
t.start()

gui.run(title="Receiver Page")

