import asyncio
import websockets

from country_list import countries_for_language
countries = [dict(countries_for_language("en"))[i].lower() for i in dict(countries_for_language("en")).keys()]
# print(countries)
print("WELCOME!")
print("Notes:\n- Names may include '.' and '&'\n- Use names like you would see in a form, like 'united states', not 'usa' or 'united states of america'.")
using = input("1. Play As Server 2. Play As Client\n")
if using not in '12':
    print("Please use '1' or '2'.")
    assert True
used = []
if using == '1':
    print("Starting...")
    async def echo(websocket):
        async for message in websocket:
            print(message)
            used.append(message)
            print("YOUR TURN")
            while True:
                guess = input().lower()
                if guess in used: print("Already used.")
                elif guess in countries:
                    break
                else:
                    print("Invalid guess. Check spelling.")
            used.append(guess)
            await websocket.send(guess)

    async def main():
        async with websockets.serve(echo, input("Host (such as localhost or 127.0.0.1): "), int(input("Port: "))):
            await asyncio.Future()  # run forever
    print("When someone joins, it is their turn first.")
    asyncio.run(main())
elif using == '2':
    async def main():
        async with websockets.connect(f'ws://{input("url + port (without ws://): ")}') as websocket:
            while True:
                print("YOUR TURN")
                while True:
                    guess = input().lower()
                    if guess in used: print("Already used.")
                    elif guess in countries:
                        break
                    else:
                        print("Invalid guess. Check spelling.")
                used.append(guess)
                await websocket.send(guess)
                r = await websocket.recv()
                used.append(r)
                print(r)

    asyncio.run(main())
