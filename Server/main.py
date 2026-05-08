import asyncio
import yaml
from websockets.asyncio.server import serve

conf= "config.yaml"
message_log = "chat_logs.txt"

messages= [] 

with open(conf, "r") as config_data:
    conf_data= yaml.safe_load(config_data)

with open(message_log, "r") as logr:
    chat_log_r= logr.readlines()
    if len(chat_log_r) >= conf_data["Max_Chat_Length"]:
        dif= len(chat_log_r) - conf_data["Max_Chat_Length"]
        del chat_log_r [0 : dif]

messages.extend(chat_log_r)

async def hello(websocket):
    print(len(messages))
    chat_length = await websocket.recv()

    if len(messages) > 0:
        print(messages, "empty")
        await websocket.send(messages[-int(chat_length): ])
    else:
        print(messages, "notempty")
        await websocket.send("no chats yet!\n")

    message= await websocket.recv()
    messages.append(message)

    with open(message_log, "a") as logw:
        logw.write(f"{message}")

    if len(messages) >= conf_data["Max_Chat_Length"]:
        messages.pop(0)
        
async def main():
    async with serve(hello, conf_data["Ip"], conf_data["Port"]) as server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())