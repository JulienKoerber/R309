import socket
import ssl
import subprocess


def execute_program(program_code):
    try:
        process = subprocess.run(["python3", "-c", program_code], capture_output=True, text=True)
        return process.stdout if process.returncode == 0 else process.stderr
    except Exception as e:
        return f"Erreur d'execution: {str(e)}"


def handle_master(master_socket):
    try:
        program_code = master_socket.recv(4096).decode('utf-8')
        result = execute_program(program_code)
        master_socket.sendall(result.encode('utf-8'))
    except Exception as e:
        master_socket.sendall(f"Erreur Esclave: {str(e)}".encode('utf-8'))
    finally:
        master_socket.close()


def start_slave(ip, port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="slave.crt", keyfile="slave.key")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((ip, port))
        server.listen(5)
        print(f"Serveur Esclave {ip}:{port}")

        while True:
            master_socket, addr = server.accept()
            master_socket = context.wrap_socket(master_socket, server_side=True)
            handle_master(master_socket)


if __name__ == "__main__":
    start_slave("0.0.0.0", 9001)
