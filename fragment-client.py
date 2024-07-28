"""

This python script demonstrates how to test session on Firewalls 
Client side

"""

import socket
import threading
import sys
import argparse

import time
import random

# Thread-safe counter for active sessions
active_sessions_lock = threading.Lock()
active_sessions = 0

def handle_server_communication(client_socket, session_id):
    global active_sessions
    with active_sessions_lock:
        active_sessions += 1
        print(f"\rActive sessions: {active_sessions}", end =" ")

    try:
        message = f"Hello from client session {session_id}"
        if session_id % 2 == 0:
            # Fragment the message into smaller packets
            fragments = [message[i:i+5] for i in range(0, len(message), 5)]
            for fragment in fragments:
                client_socket.sendall(fragment.encode('utf-8'))
                time.sleep(0.1)  # Small delay to simulate fragmentation
        else:
            client_socket.sendall(message.encode('utf-8'))



        while True:
            response = client_socket.recv(1024)
            if not response:
                break
            if message.encode('utf-8') != response:
                print(f"\nData mismatch in session {session_id}: Sent '{message}', Received '{response.decode('utf-8')}'")
           
    except Exception as e:
        print(f"Error in session {session_id}: {e}")

    finally:
        print(f"Session {session_id} closing connection.")
        client_socket.close()
        with active_sessions_lock:
                active_sessions -= 1
                print(f"\rActive sessions: {active_sessions}", end =" ")

def create_client_session(host, port, session_id):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        #print(f"Session {session_id} connected to {host}:{port}")
        handle_server_communication(client_socket, session_id)
    except Exception as e:
        print(f"Failed to connect in session {session_id}: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python tcp_client.py <host> <port> <num_sessions>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    num_sessions = int(sys.argv[3])

    threads = []
    for i in range(num_sessions):
        t = threading.Thread(target=create_client_session, args=(host, port, i+1))
        threads.append(t)

        delay = random.uniform(0,0.01)
        time.sleep(delay)

        t.start()

    # Wait for user input before closing the sessions
    #input("Press Enter to close all sessions...")

    for t in threads:
        t.join()



if __name__ == "__main__":
     # Argument parser
    parser = argparse.ArgumentParser(
        description="This script helps in firewall session tests - client"
    )
    main()