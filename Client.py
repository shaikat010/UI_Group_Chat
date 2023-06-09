import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

# Create a socket for the client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prompt the user to choose a nickname before joining the server
nickname = input("Choose your nickname before joining the server: ")

# Connect to the server
client.connect(('127.0.0.1', 55555))

# Create the main window using Tkinter
root = tk.Tk()
root.title("Chat Application")
root.configure(bg='black')

# Create a scrolled text widget to display messages
message_box = scrolledtext.ScrolledText(root, state='disabled', bg='black', fg='white')
message_box.pack(fill=tk.BOTH, expand=True)

# Create an entry widget for user input
input_entry = tk.Entry(root)
input_entry.pack(fill=tk.BOTH)


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                display_message(message)

        except:
            display_message("An error occurred!")
            client.close()
            break


def write():
    def send_message():
        message = f"{nickname}: {input_entry.get()}"
        client.send(message.encode('ascii'))
        input_entry.delete(0, tk.END)

    # Create a button to send messages
    send_button = tk.Button(root, text="Send", command=send_message, bg='white', fg='black')
    send_button.pack()


def display_message(message):
    message_box.configure(state='normal')
    message_box.insert(tk.END, f"{message}\n", 'message')
    message_box.configure(state='disabled')
    message_box.see(tk.END)


# Apply tags to the message box to make the text colorful
message_box.tag_config('message', foreground='green', font=('Arial', 14))

# Start the receive thread
receive_thread = threading.Thread(target=receive)
receive_thread.start()

# the thread for writing
write_thread = threading.Thread(target=write)
write_thread.start()

# Start the Tkinter event loop
root.mainloop()
