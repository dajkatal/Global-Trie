# Put the server's IP and POST and run the script in terminal/command prompt with "python3 client.py"

IP = '0.0.0.0'  # Put IP of Trie Server
PORT = 8000  # Put Port of Trie Server


# Only change things below if you know what you are doing.
import socket

ADDRESS = (IP, PORT)
disconnect_message = 'disconnect'

client = socket.socket()
client.connect(ADDRESS)

while True:
    msg = input("[Server] enter your message...")
    if msg.lower() == 'help':
        print("""[Client] Available Commands:
    - add 'input_word'              # Adds a word to the Trie
    - remove 'input_word'           # Removes a word from the Trie
    - exists 'input_word'           # Checks if word is in the Trie
    - autocomplete 'input_word'     # Returns words in the Trie that start with a prefix
    - print                         # Prints out the Trie
    - save                          # Saves the data in the Trie for future use
    - disconnect                    # Disconnects the client from the server""")
        continue
    msg_length_in_bytes = str(len(msg)).encode('utf-8')
    client.send(b' '*(64-len(msg_length_in_bytes)) + msg_length_in_bytes)
    client.send(msg.encode('utf-8'))
    msg_length = int(client.recv(64).decode('utf-8'))
    msg = client.recv(msg_length).decode('utf-8')
    print(f"[Client] received message: {msg}")
    if msg == disconnect_message:
        break
client.close()
