# Global-Trie

This project is divided into two sections. The Trie Server itself, and the program for clients to connect with the server.

## Installing the server

The server can be installed simply with PIP

```sh
$ pip install globaltrie-server
```

To start the server, you must host it on a certain port.
```sh
$ trieserver --start PORT  # Replace PORT with your desired port.
```

## Installing the client

The client is also installed with PIP

```sh
$ pip install globaltrie
```

### Using client as CLI
To start the client as a CLI, you must specify the server's IP and PORT it provided.
```sh
$ globaltrie --ip IP --port PORT  # Replace IP and PORT with your server's ip and port.
```
Once connected to the server, use the following commands
```sh
[Client] Available Commands:
        - add 'input_word'              # Adds a word to the Trie
        - remove 'input_word'           # Removes a word from the Trie
        - exists 'input_word'           # Checks if word is in the Trie
        - autocomplete 'input_prefix'     # Returns words in the Trie that start with a prefix
        - print                         # Prints out the Trie
        - save                          # Saves the data in the Trie for future use
        - disconnect                    # Disconnects the client from the server
```

### Using client as module

```python
from globaltrie import global_trie as trie

client = trie('IP', PORT)  # Replace IP and PORT with your server's ip and port.
client.connect()

# Possible commands that can be run...
client.add_keyword('Any word')                   # Adds a word to the Trie
client.remove_keyword('Any word')                # Removes a word from the Trie
client.keyword_exists('Any word')                # Checks if word is in the Trie
client.autocomplete('Any alphabetical prefix')   # Returns words in the Trie that start with a prefix
client.print()                                   # Prints out the Trie
client.save()                                    # Saves the data in the Trie for future use


# When you are done using the Trie, make sure to disconnect.
client.disconnect()
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
