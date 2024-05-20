import sys
import socketserver
import socket
import asyncio


key_value_store = {}


def make_bulk_string(s):
    return "$" + str(len(s)) + "\r\n" + s + "\r\n"


def serialiser(data):
    if data is None:
        return ("$-1\r\n").encode()
    elif data == "OK":
        return ("+OK\r\n").encode()
    elif data == "Error Message":
        return ("-Error message\r\n").encode()
    elif data == "":
        return ("$0\r\n\r\n").encode()
    elif isinstance(data, int):
        return (":" + str(data) + "\r\n").encode()
    elif isinstance(data, str):
        return ("+" + (data) + "\r\n").encode()
    elif isinstance(data, list):
        serialised_string = "*" + str(len(data)) + "\r\n"
        if len(data) == 1:
            return (serialised_string + make_bulk_string(data[0])).encode()
        for d in data:
            serialised_string += make_bulk_string(d)
        return serialised_string.encode()
    return make_bulk_string(data).encode()


def deserialiser(data):
    data = data.decode("utf8")
    if data == "$-1\r\n" or data == "*-1\r\n" or data == ":-1\r\n":
        return None
    elif data[0] == "-":
        return data.split("\r\n")[0][1:]
    elif data[0] == "+":
        return data.split("\r\n")[0][1:]
    elif data[0] == ":":
        return data.split("\r\n")[0][1:]
    elif data[0] == "$":
        return data.split("\r\n")[1]
    elif data[0] == "*":
        split_data = data.split("\r\n")[1:]
        commands = []
        # len1 = 0
        for s in split_data:
            print(s)
            if s:
                if s[0] == "$":
                    # len1 = s[1:]
                    # print(len1)
                    continue
                # print(len(s))
                # if len(s) == int(len1):
                commands.append(s)
                # len1 = 0
        return handle_command(commands)
    return data.split("\r\n")[1]


def handle_command(commands):
    if commands[0].upper() == "PING":
        return "PONG"
    if commands[0].upper() == "ECHO":
        return commands[1]
    if commands[0].upper() == "SET":
        key_value_store[commands[1]] = commands[2]
        return "OK"
    if commands[0].upper() == "GET":
        return key_value_store.get(commands[1], "Error Message")
    if commands[0].upper() == "CONFIG":
        return "OK"

    return "Error Message"


input_list_de = [
    b"$-1\r\n",
    b"*1\r\n$4\r\nping\r\n",
    b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n",
    b"*2\r\n$3\r\nget\r\n$3\r\nkey\r\n",
    b"+OK\r\n",
    b"-Error message\r\n",
    b"$0\r\n\r\n",
    b"+hello world\r\n",
]
# # print(serialiser("PING"))
# for in1 in input_list_de:
#     print(repr(in1) + "\n deserialised \n")
#     print(deserialiser(in1))
#     print("\n")
#     print(repr(in1) + "\n serialised \n")
#     print(repr(serialiser(deserialiser(in1))))


# import asyncio


async def handle_client(reader, writer):
    request = None
    while request != "quit":
        request = await reader.read(255)
        print(repr(request))
        response = serialiser(deserialiser(request))
        print(repr(response))
        # response = str(eval(request)) + "\n"
        writer.write(response)
        await writer.drain()
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 6379)
    async with server:
        await server.serve_forever()


asyncio.run(run_server())


#     with socketserver.ThreadingTCPServer((host, port), MyTCPHandler) as server:
#         try:
#             loop = asyncio.get_running_loop()
#             server_task = loop.run_in_executor(None, server.serve_forever)
#             await server_task
#         except KeyboardInterrupt:
#             server.shutdown()
#             server.server_close()
#             sys.exit()


# if __name__ == "__main__":
#     asyncio.run(main())
