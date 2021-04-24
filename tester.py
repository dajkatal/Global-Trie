# Run this script when a Trie server is running and the client-side module is correctly installed.

server_IP = '0.0.0.0'  # Put IP of Trie Server
server_PORT = 8000  # Put Port of Trie Server


# Only change things below if you know what you are doing.
import socket, threading, time

ADDRESS = (server_IP, server_PORT)
disconnect_message = 'disconnect'

standard_tests = [
    'add hello',  # Add new word
    'add howdy',  # Add new word
    'add hey',  # Add new word
    'add hey',  # Try to add word that already exists
    'add test',  # Add new word
    'print',  # Print Trie
    'exists hey',  # Exists with word in Trie
    'remove howdy',  # Remove existing word
    'add totally',  # Add new word
    'add laugh',  # Add new word
    'remove test',  # Remove existing word
    'exists test',  # Exists with word that is not in Trie
    'print',  # Print Trie
    'remove hey',  # Remove existing word
    'add hey',  # Add word that was just removed
    'add amazing',  # Add new word
    'add incredible',  # Add new word
    'remove incredible',  # Remove existing word
    'print',  # Print Trie
    'autocomplete i',  # Autocomplete to get 'No Words'
    'autocomplete h',  # Autocomplete to get 'hello, hey'
    'save'  # Save current state of Trie
]  # Tests how the application is used normally.

edge_case_tests = [
    'autocomplete h',
    'exists hello',
    'add hElLO',  # Should say 'hello' already exists in Trie
    'remove hello',
    'add <1w23812-?!#>',  # Tests if 'word' that is not alphabetical throws unhandled error
    'remove hey',
    'remove totally',
    'remove laugh',
    'print',
    'remove amazing',
    'print',  # Print empty Trie
    'exists hello',  # Exists with empty Trie
    'autocomplete h',  # Autocomplete with empty Trie
    'save',  # Save empty Trie
]  # Tests times where application could make mistakes or throw errors.

two_clients_tests = [
    # Client 1
    [
        'add hello',
        'remove test',
        'print'
    ],
    # Client 2
    [
        'print',
        'add test',
        'print'
    ]
]  # Tests rare cases where two clients send requests at the same time.


def send_msg(client, msg):
    # Save code used to communicate with server in CLI.
    msg_length_in_bytes = str(len(msg)).encode('utf-8')
    client.send(b' ' * (64 - len(msg_length_in_bytes)) + msg_length_in_bytes)
    client.send(msg.encode('utf-8'))
    temp = client.recv(64).decode('utf-8')
    msg_length = int(temp)
    msg = client.recv(msg_length).decode('utf-8')
    print(f"[Client] received message: {msg}")
    if msg == disconnect_message:
        print("Disconnected")
        client.close()


print('------STANDARD TESTS------')

client1 = socket.socket()
client1.connect(ADDRESS)
for test in standard_tests:
    send_msg(client1, test)

print('\n\n------EDGE CASE TESTS------')

for test in edge_case_tests:
    send_msg(client1, test)

print('\n\n------TWO CLIENTS TESTS------')


def client_tests(client, client_number):
    client_number-=1  # Convert client numbers 1 and 2 to indices 0 and 1
    for test in two_clients_tests[client_number]:
        send_msg(client, test)
    send_msg(client, 'disconnect')


client2 = socket.socket()
client2.connect(ADDRESS)
t1 = threading.Thread(target=client_tests, args=(client1, 1))
t2 = threading.Thread(target=client_tests, args=(client2, 2))
t1.start()
t2.start()

while threading.active_count() > 1:
    time.sleep(0.3)

print("\n\n------DONE------")
print("No Errors were thrown, meaning the Trie server was set up correctly.")
print("You can start connecting clients and using it as intended.")

