import json
import threading
import socket

SERVER_IP = "192.168.50.50"  # Host
PORT = 5000  # The same port as the server


class ssh_client:
    def __init__(self, **kwargs):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
        self.Rp = 0
        self.Ri = 0
        self.Rd = 0
        self.Kp = 0
        self.Ki = 0
        self.Kd = 0
        self.Kp2 = 0
        self.Ki2 = 0
        self.Kd2 = 0
        self.Pos = 0
        self.json_data = {"Rp": 1, "Ri": 2, "Rd": 3, "Kp": 4, "Ki": 5, "Kd": 6, "Kp2": 7, "Ki2": 8, "Kd2": 9, "Pos": 10}

    def connect_to_server(self):
        try:
            self.socket.connect((SERVER_IP, PORT))
            print(f"Connected to server {SERVER_IP}:{PORT}")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            print(f"Connection failed: {e}")

    def receive_data(self):  # Receive data from RP
        while True:
            try:
                data = self.socket.recv(1024).decode()
                if not data:
                    break
                self.json_data = json.loads(data)
                self.data_rcv_update = True
                self.Rp = self.json_data["Rp"]
                self.Ri = self.json_data["Ri"]
                self.Rd = self.json_data["Rd"]
                self.v_batt = self.json_data["Vb"]
                self.Kp = self.json_data["Kp"]
                self.Ki = self.json_data["Ki"]
                self.Kd = self.json_data["Kd"]
                self.Kp2 = self.json_data["Kp2"]
                self.Ki2 = self.json_data["Ki2"]
                self.Kd2 = self.json_data["Kd2"]
                self.Pos = self.json_data["Pos"]

            except Exception as e:
                print(f"Error receiving data: {e}")
                break
        self.socket.close()
