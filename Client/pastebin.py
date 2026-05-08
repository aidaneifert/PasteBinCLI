from websockets.sync.client import connect
import yaml

config= "config.yaml"

with open(config, "r") as conf:
    config_data= yaml.safe_load(conf)

ip= config_data["Ip"]
port= config_data["Port"]
uri = f"ws://{ip}:{port}"

def Client():
    while True:      
        with connect(uri) as websocket:
            websocket.send(str(config_data["Chat_Length"]))
            messages = websocket.recv()
            print(messages)
            message = input(">")
            websocket.send(f"{message}\n")        

if __name__ == "__main__":
    Client()




