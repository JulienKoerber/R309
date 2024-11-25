import socket
import ssl
import tkinter as tk
from tkinter import filedialog, messagebox


def send_program(ip, port, filepath):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip, port)) as sock:
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                with open(filepath, 'r') as file:
                    program_code = file.read()

                ssock.sendall(program_code.encode('utf-8'))
                response = ssock.recv(4096).decode('utf-8')
                return response
    except Exception as e:
        return f"Error: {str(e)}"


def browse_file():
    filepath = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if filepath:
        entry_filepath.delete(0, tk.END)
        entry_filepath.insert(0, filepath)


def submit_program():
    ip = entry_ip.get()
    port = int(entry_port.get())
    filepath = entry_filepath.get()

    if not filepath:
        messagebox.showwarning("Input Error", "Please select a file!")
        return

    response = send_program(ip, port, filepath)
    text_output.delete(1.0, tk.END)
    text_output.insert(tk.END, response)


# GUI Setup
root = tk.Tk()
root.title("Distributed Python Executor - Client")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Server IP:").grid(row=0, column=0, sticky="w")
entry_ip = tk.Entry(frame)
entry_ip.insert(0, "127.0.0.1")
entry_ip.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Port:").grid(row=1, column=0, sticky="w")
entry_port = tk.Entry(frame)
entry_port.insert(0, "9000")
entry_port.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="File Path:").grid(row=2, column=0, sticky="w")
entry_filepath = tk.Entry(frame, width=40)
entry_filepath.grid(row=2, column=1, padx=5, pady=5)

tk.Button(frame, text="Browse", command=browse_file).grid(row=2, column=2, padx=5, pady=5)
tk.Button(frame, text="Submit", command=submit_program).grid(row=3, column=1, pady=10)

text_output = tk.Text(frame, height=15, width=50)
text_output.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
