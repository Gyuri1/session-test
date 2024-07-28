"""

This python script demonstrates how to test session on Firewalls 
Server side

https://stackoverflow.com/questions/34588/how-do-i-change-the-number-of-open-files-limit-in-linux/8285278#8285278
"""

import socket, threading

TCP_PORT=5002
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', TCP_PORT))
serversocket.listen(5)


# Thread-safe counter for active sessions
active_sessions_lock = threading.Lock()
active_sessions = 0


def client_listener(connection, address):
    global active_sessions
    session_id = threading.get_ident()
   

    #print(f"New connection {connection=} {address=} {session_id=}")

    while True:
        try:
            buf = connection.recv(64)
            if not buf:
                #print(f"Closing connection {connection=} {address=}")
                with active_sessions_lock:
                    active_sessions -= 1
                    print(f"\rActive sessions: {active_sessions}", end =" ")
                break
            connection.sendall(buf)  # Send back the received packet
            #print(buf)
        except Exception as e:
            print(f"Error in session {session_id}: {e}")    

print(f"TCP server started on port {TCP_PORT} ")
print(f"\rActive sessions: {active_sessions}", end =" ")
while True:
    connection, address = serversocket.accept()
    threading.Thread(target=client_listener, args=(connection, address)).start()
    with active_sessions_lock:
        active_sessions += 1
        print(f"\rActive sessions: {active_sessions}", end =" ")