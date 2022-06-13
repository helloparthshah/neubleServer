import asyncio
from websockets import serve
import websockets


class Room:
    def __init__(self, p1):
        self.p1 = p1
        self.p2 = None


rooms = []
games = []


async def handler(websocket):
    try:
        message = await websocket.recv()
        print(message)
        if(message == "Hello"):
            if len(rooms) == 0:
                room = Room(websocket)
                rooms.append(room)
                await echo(room, "p1")
            else:
                print("Room full")
                room = rooms[0]
                room.p2 = websocket
                rooms.pop(0)
                games.append(room)
                await websocket.send("Connected")
                await echo(room, "p2")
    except websockets.ConnectionClosed as e:
        # delete room if player disconnects
        for room in rooms:
            if room.p1 == websocket:
                rooms.remove(room)
                break
        for game in games:
            if game.p1 == websocket or game.p2 == websocket:
                await game.p1.send("Disconnected")
                games.remove(game)
                break
        print(e)


async def echo(room, player):
    while True:
        if(not room.p2):
            await room.p1.send("Waiting")
        if(player == "p1"):
            message = await room.p1.recv()
            if(room.p2):
                await room.p2.send(message)
        else:
            message = await room.p2.recv()
            await room.p1.send(message)


async def main():

    async with serve(handler, "0.0.0.0", 3000):
        # print server ip address and port
        await asyncio.Future()  # run forever

asyncio.run(main())
