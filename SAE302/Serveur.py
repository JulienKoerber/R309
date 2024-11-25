import socket
import ssl
import threading
import psutil
import subprocess
import queue
import json

MAX_QUEUE_SIZE = 5
SLAVES = [("127.0.0.1", 9001)]  # Liste des serveurs esclaves

task_queue = queue.Queue(MAX_QUEUE_SIZE)


def monitor_server():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    return cpu, memory


def execute_program(program_code):
    try:
        process = subprocess.run(["python3", "-c", program_code], capture_output=True, text=True)
        return process.stdout if process.returncode == 0 else process.stderr
    except Exception as e:
        return f"Execution Error: {str(e)}"


def delegate_to_slave(slave_ip, slave_port, program_code):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((slave_ip, slave_port)) as sock:
            with context.wrap_socket(sock, server_hostname=slave_ip) as ssock:
                ssock.sendall(program_code.encode('utf-8'))
                response = ssock.recv(4096).decode('utf-8')
                return response
    except Exception as e:
        return f"Error delegating to slave: {str(e)}"


def handle_client(client_socket):
    try:
        program_code = client_socket.recv(4096).decode('utf-8')

        cpu, memory = monitor_server()
        if cpu > 75 or task_queue.full():  # Condition de délégation
            for slave_ip, slave_port in SLAVES:
                response = delegate_to_slave(slave_ip, slave_port, program_code)
                client_socket.sendall(response.encode('utf-8'))
                return

        # Exécution locale
        task_queue.put(program_code)
        result = execute_program(program_code)
        task_queue.get()
        client_socket.sendall(result.encode('utf-8'))
    except Exception as e:
        client_socket.sendall(f"Server Error: {str(e)}".encode('utf-8'))
    finally:
        client_socket.close()


def start_server(ip, port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, port))
        server.listen(5)
        print(f"Server started at {ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            client_socket = context.wrap_socket(client_socket, server_side=True)
            threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_server("0.0.0.0", 9000)
