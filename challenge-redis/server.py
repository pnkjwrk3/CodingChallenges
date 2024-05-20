# import sys
# import socketserver
# import socket
import asyncio
import time


key_value_store = {}
key_expiry_store = {}


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
    if data:
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
            for s in split_data:
                if s:
                    if s[0] == "$":
                        continue
                    commands.append(s)
            return commands
    return None


# Need to optimize this function, using a tree or a heap or radix sort tree to store expiry times and keys
# def delete_expired_keys():
#     while True:
#         for key in key_expiry_store:
#             if key_expiry_store[key] < int(time.time()):
#                 key_value_store.pop(key, None)
#                 key_expiry_store.pop(key, None)
#         time.sleep(1)


def set_key(key, value, expiry_time=None):
    key_value_store[key] = value
    if expiry_time:
        key_expiry_store[key] = expiry_time


def delete_key(key):
    if key_value_store.get(key, None):
        del key_value_store[key]
    if key_expiry_store.get(key, 0) > 0:
        del key_expiry_store[key]
    # key_value_store.pop(key, None)
    # key_expiry_store.pop(key, None)


def exists_key(key):
    return key_value_store.get(key, None) and not (
        key_expiry_store.get(key, 0) > 0
        and key_expiry_store.get(key, 0) < int(time.time())
    )


def handle_command(commands):
    match commands[0].upper():
        case "PING":
            return "PONG"
        case "ECHO":
            return commands[1]
        case "SET":
            match len(commands):
                case 3:
                    set_key(commands[1], commands[2])
                case 5:
                    match commands[3].upper():
                        case "EX":
                            expiry_time = (
                                int(commands[4]) + time.time()
                                if commands[3].upper() == "EX"
                                else int(commands[4])
                            )
                            set_key(commands[1], commands[2], expiry_time)
                        case "PX":
                            expiry_time = (
                                int(commands[4]) + int(time.time() * 1000)
                                if commands[3].upper() == "PX"
                                else int(commands[4])
                            )
                            set_key(commands[1], commands[2], expiry_time)
            return "OK"
        case "EXPIRY":
            if len(commands) == 3:
                key_expiry_store[commands[1]] = int(commands[2])
        case "GET":
            if exists_key(commands[1]):
                return key_value_store.get(commands[1], "Error Message")
            else:
                delete_key(commands[1])
                return None
        case "DEL":
            delete_key(commands[1])
            return "OK"
        case "EXISTS":
            return "OK" if exists_key(commands[1]) else "Error Message"
        case "INCR":
            if exists_key(commands[1]):
                key_value_store[commands[1]] = int(key_value_store[commands[1]]) + 1
                return key_value_store[commands[1]]
            else:
                return "Error Message"
        case "DECR":
            if exists_key(commands[1]):
                key_value_store[commands[1]] = int(key_value_store[commands[1]]) - 1
                return key_value_store[commands[1]]
            else:
                return "Error Message"
        case "LPUSH":
            if exists_key(commands[1]):
                key_value_store[commands[1]].insert(0, commands[2])
            else:
                key_value_store[commands[1]] = [commands[2]]
            return len(key_value_store[commands[1]])
        case "RPUSH":
            if exists_key(commands[1]):
                key_value_store[commands[1]].append(commands[2])
            else:
                key_value_store[commands[1]] = [commands[2]]
            return len(key_value_store[commands[1]])
        case "SAVE":
            for key in key_value_store:
                if exists_key(key):
                    with open("redis_dump.txt", "a") as f:
                        f.write(f"{key} {key_value_store[key]}\n")
                else:
                    delete_key(key)
            return "OK"
        case "CONFIG":
            return "OK"
        case _:
            return "Error Message"

    # if commands[0].upper() == "PING":
    #     return "PONG"
    # if commands[0].upper() == "ECHO":
    #     return commands[1]
    # if commands[0].upper() == "SET":
    #     if len(commands) == 3:
    #         set_key(commands[1], commands[2])
    #     elif commands[3].upper().startswith("EX") and (
    #         commands[4].isdigit() or int(commands[4]).isdigit()
    #     ):
    #         expiry_time = (
    #             int(commands[4]) + time.time()
    #             if commands[3].upper() == "EX"
    #             else int(commands[4])
    #         )
    #         set_key(commands[1], commands[2], expiry_time)

    #     elif commands[3].upper().startswith("PX") and (
    #         commands[4].isdigit() or int(commands[4]).isdigit()
    #     ):
    #         expiry_time = (
    #             int(commands[4]) + int(time.time() * 1000)
    #             if commands[3].upper() == "PX"
    #             else int(commands[4])
    #         )
    #         set_key(commands[1], commands[2], expiry_time)
    #     return "OK"
    # if commands[0].upper() == "EXPIRY":
    #     if len(commands) == 3:
    #         key_expiry_store[commands[1]] = int(commands[2])
    # if commands[0].upper() == "GET":
    #     if key_expiry_store.get(commands[1], 0) > 0:
    #         if key_expiry_store[commands[1]] < int(time.time()):
    #             delete_key(commands[1])
    #             return None
    #     return key_value_store.get(commands[1], "Error Message")
    # if commands[0].upper() == "CONFIG":
    #     return "OK"

    # return "Error Message"


# Unit Tests - Ideally should be in a separate test file. But keeping it here for the sake of submission.
def test_serialiser():
    test_cases = [
        (None, b"$-1\r\n"),
        ("OK", b"+OK\r\n"),
        ("Error Message", b"-Error message\r\n"),
        ("", b"$0\r\n\r\n"),
        (123, b":123\r\n"),
        ("hello world", b"+hello world\r\n"),
        (["ping"], b"*1\r\n$4\r\nping\r\n"),
        (["echo", "hello world"], b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"),
        (["get", "key"], b"*2\r\n$3\r\nget\r\n$3\r\nkey\r\n"),
    ]

    for data, expected_output in test_cases:
        result = serialiser(data)
        assert (
            result == expected_output
        ), f"Failed for input: {data}. Expected: {expected_output}, Got: {result}"

    print("All test cases passed!")


def test_deserialiser():
    test_cases = [
        (b"$-1\r\n", None),
        (b"*1\r\n$4\r\nping\r\n", ["ping"]),
        (b"*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n", ["echo", "hello world"]),
        (b"*2\r\n$3\r\nget\r\n$3\r\nkey\r\n", ["get", "key"]),
        (b"+OK\r\n", "OK"),
        (b"-Error message\r\n", "Error message"),
        (b"$0\r\n\r\n", ""),
        (b"+hello world\r\n", "hello world"),
    ]

    for data, expected_output in test_cases:
        # print(data, expected_output)
        result = deserialiser(data)
        assert (
            result == expected_output
        ), f"Failed for input: {data}. Expected: {expected_output}, Got: {result}"

    print("All test cases passed!")


def test_handle_command():
    test_cases = [
        (["PING"], "PONG"),
        (["ECHO", "hello world"], "hello world"),
        (["SET", "key", "value"], "OK"),
        (["GET", "key"], "value"),
        (["SET", "key2", "value2", "EX", "10"], "OK"),
        (["GET", "key2"], "value2"),
        (["CONFIG"], "OK"),
        (["INVALID"], "Error Message"),
        (["EXISTS", "key"], "OK"),
        (["SET", "key3", "2"], "OK"),
        (["INCR", "counter"], "Error Message"),
        (["INCR", "key3"], 3),
        (["DECR", "key3"], 2),
        (["DEL", "key3"], "OK"),
        (["LPUSH", "list", "item1"], 1),
        (["RPUSH", "list", "item2"], 2),
        (["DEL", "key"], "OK"),
        (["DECR", "counter"], "Error Message"),
        (["EXPIRY", "key", "10"], None),
        (["SAVE"], "OK"),
    ]

    for commands, expected_output in test_cases:
        result = handle_command(commands)
        assert (
            result == expected_output
        ), f"Failed for input: {commands}. Expected: {expected_output}, Got: {result}"

    # Additional test case for checking key retrieval after 10 seconds
    time.sleep(11)
    result = handle_command(["GET", "key2"])
    assert (
        result == None
    ), f"Failed for input: ['GET', 'key2']. Expected: None, Got: {result}"

    print("All test cases passed!")


# test_serialiser()
# test_deserialiser()
# test_handle_command()


# Server Code for concurrent connections using asyncio
async def handle_client(reader, writer):
    request = None
    while request != "quit":
        request = await reader.read(255)
        # print(repr(request))
        deserialised_request = deserialiser(request)
        if isinstance(deserialised_request, list):
            response = serialiser(handle_command(deserialised_request))
        else:
            response = serialiser(deserialiser(request))
        writer.write(response)
        try:
            await writer.drain()
        except ConnectionResetError:
            print("Connection Reset. Closing Connection.")
            break
    try:
        writer.close()
        await writer.wait_closed()
    except BrokenPipeError:
        print("Broken Pipe. Connection Closed.")


async def run_server():
    server = await asyncio.start_server(handle_client, "127.0.0.1", 6379)
    async with server:
        await server.serve_forever()


asyncio.run(run_server())
