# Only change things unless you know what you are doing.

import os, dill, socket, threading
from trie import trie_class

# Set up the address of server.
PORT = 8000
IP = socket.gethostbyname(socket.gethostname())
ADDRESS = ('0.0.0.0', PORT)
# Disconnect message to let clients disconnect.
disconnect_message = 'disconnect'
# Name of file storing trie
file_name = 'trie_dump'

# Load Trie
trie = None
if os.path.isfile(f'./{file_name}'):
    with open(file_name, 'rb') as dill_file:
        trie = dill.load(dill_file)
    print("Loaded saved Trie")
else:
    trie = trie_class()
    print("Trie was not saved... new Trie made")

# Start server.
server = socket.socket()
server.bind(ADDRESS)
print("[Starting] server is starting...")


def save_trie():
    # If save command is run, the Trie is saved to a file.
    with open(file_name, "wb") as dill_file:
        dill.dump(trie, dill_file)


def send_msg(response, connection):
    # Function to send message back to the client.

    msg_length_in_bytes = str(len(response)).encode('utf-8')
    connection.send(b' ' * (64 - len(msg_length_in_bytes)) + msg_length_in_bytes)
    connection.send(response.encode('utf-8'))


queue = []
needs_initiation = [True]


def queue_handler():
    # Handles priority if multiple requests are made at once.

    # Instead of checking queue length, just try.
    try:
        # Check message.
        data = queue.pop()
        msg = data[0].lower()
        print(f"{msg} from {data[1]}", queue)
        split_msg = msg.split(" ")
        # Make sure message contains only command word and input. (i.e ADD hello)
        if len(split_msg) > 2 or not msg.replace(" ", "").isalpha():
            send_msg("Wrong message format", data[1])
        else:
            first_word = split_msg[0]
            if first_word == 'save':
                save_trie()
                send_msg("The Trie was saved", data[1])
            elif first_word == 'add':
                output = trie.add_keyword(split_msg[1])
                send_msg(output, data[1])
            elif first_word == 'remove':
                output = trie.remove_keyword(split_msg[1])
                send_msg(output, data[1])
            elif first_word == 'exists':
                output = trie.keyword_exists(split_msg[1])
                send_msg(output, data[1])
            elif first_word == 'autocomplete':
                output = trie.autocomplete(split_msg[1])
                if len(output) == 0:
                    output = ['No Words']
                send_msg(f"Words that start with '{split_msg[1]}' are: " + ', '.join(output), data[1])
            elif first_word == 'print':
                output = trie.print()
                if len(output) == 0:
                    output = 'Empty'
                if len(output) == 0:
                    output = "No data in Trie"
                send_msg('\n' + output, data[1])
            # Allow client to disconnect.
            elif msg == disconnect_message:
                send_msg("disconnect", data[1])
                data[1].close()
            else:
                send_msg('This script has been tampered with. Make sure the command words are correct.', data[1])

        queue_handler()
    except IndexError:
        needs_initiation[0] = True


def client_function(connection):
    while True:
        try:
            # Get message length.
            msg_length = connection.recv(64)
            msg_length = int(msg_length.decode('utf-8'))
            # Receive message.
            msg = connection.recv(msg_length).decode('utf-8')
            queue.append([msg, connection])
            if needs_initiation[0]:
                needs_initiation[0] = False
                queue_handler()
        except:
            connection.close()


thread = threading.Thread(target=queue_handler)
thread.start()
server.listen(2)
while True:
    client, address = server.accept()
    print(f"[Connected] connection made to {address[0]}:{address[1]}...")
    thread = threading.Thread(target=client_function, args=(client,))
    thread.start()
    print(f"[Clients] {threading.active_count()-1} active clients...")
