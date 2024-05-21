# Build Your Own Redis Server Challenge

This repository contains the code for the "Build Your Own Redis Server" challenge in Python. 
Given the challenge to build a Redis server from scratch, I implemented a simple version of a Redis server using Python and the Redis protocol (RESP2).

The Project description can be found [here](https://codingchallenges.fyi/challenges/challenge-redis).

## Prerequisites

Before getting started, make sure you have the following installed:

- Python (version 3.11.0 or higher)
- [Redis](https://redis.io/) (version 7.2.4)

## Getting Started

To get started with the challenge, follow these steps:

1. Clone this repository to your local machine.
4. Run the Python script to start your own Redis server implementation:
    ```
    python redis_server.py
    ```

## Usage

Once your Redis server is up and running, you can interact with it using the Redis command-line interface. Here are a few examples:

- Check if the server is running:
  ```
  redis-cli PING
  ```

- Echo a message:
  ```
  redis-cli ECHO "Hello, World!"
  ```

- Set a key-value pair:
  ```
  redis-cli SET key value [EX seconds | PX milliseconds |  EXAT unix-time-seconds | PXAT unix-time-milliseconds]
  ```
  Example: redis-cli SET name "Alice" EX 10

  The SET command sets the value of a key. If the key already exists, it will be overwritten. The optional EX argument specifies the expiration time in seconds. In this example, the key "name" is set to "Alice" with an expiration time of 10 seconds.
  
  The command also supports a set of other options like
  - EX seconds: Set the specified expire time, in seconds.
  - PX milliseconds: Set the specified expire time, in milliseconds.
  - EXAT unix-time-seconds: Set the specified Unix time at which the key will expire, in seconds.
  - PXAT unix-time-milliseconds: Set the specified Unix time at which the key will expire, in milliseconds.

- Get the value of a key:
  ```
  redis-cli GET key
  ```

- Delete a key:
  ```
  redis-cli DEL key
  ```

- Check if a key exists:
  ```
  redis-cli EXISTS key
  ```

- Increment the value of a key:
  ```
  redis-cli INCR key
  ```

- Decrement the value of a key:
  ```
  redis-cli DECR key
  ```

- Check if a key Exists:
  ```
  redis-cli EXISTS key
  ```

- Insert a value at the head of a list, if the list does not exist, it will be created:
  ```
  redis-cli LPUSH key value
  ```

- Insert the specified value at the tail of the list stored at key:
  ```
  redis-cli RPUSH key value
  ```

- Save the current state of the database to disk:
  ```
  redis-cli SAVE
  ```

This is a simple implementation of a Redis server, so not all Redis commands are supported. For a complete list of available commands, refer to the [Redis documentation](https://redis.io/commands).

## Pending work
- [ ] Porting the code to rust

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).