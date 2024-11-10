import json
import threading
import socket
from kivy.core.window import Window

# from ssh_client_dashboard import set_K_values

Window.size = (720, 480)

SERVER_IP = "192.168.50.50"  # Host
PORT = 5000  # The same port as the server


class ssh_client():
    def __init__(self, **kwargs):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.Kp = 0
        self.Ki = 0
        self.Kd = 0
        self.Kp2 = 0
        self.Ki2 = 0
        self.Kd2 = 0
        self.json_data = {"Kp": 1, "Ki": 2, "Kd": 3, "Kp2": 4, "Ki2": 5, "Kd2": 6}

    def connect_to_server(self):
        try:
            self.socket.connect((SERVER_IP, PORT))
            print(f"Connected to server {SERVER_IP}:{PORT}")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            print(f"Connection failed: {e}")

    def receive_data(self):     # Receive data from RP
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                self.json_data = json.loads(data)
                self.data_rcv_update = True
                self.Kp = self.json_data['Kp']
                self.Ki = self.json_data['Ki']
                self.Kd = self.json_data['Kd']
                self.Kp2 = self.json_data['Kp2']
                self.Ki2 = self.json_data['Ki2']
                self.Kd2 = self.json_data['Kd2']
                # print(self.json_data)
                # Clock.schedule_once(lambda dt: self.update_labels(json_data))
            except Exception as e:
                print(f"Error receiving data: {e}")
                break
        self.socket.close()
