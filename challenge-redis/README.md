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
  redis-cli SET key value
  ```

- Get the value of a key:
  ```
  GET key
  ```

<!-- - Delete a key:
  ```
  DEL key -->
  ```

This is a simple implementation of a Redis server, so not all Redis commands are supported. For a complete list of available commands, refer to the [Redis documentation](https://redis.io/commands).

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).