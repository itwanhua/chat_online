#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket, threading
import tkinter as tk
import tkinter.messagebox as tm


def on_send_msg():
    nick_name = "君哥小号"
    chat_msg = chat_msg_box.get(1.0, "end")
    if chat_msg == "\n":
        return 

    chat_data = nick_name + ":" + chat_msg
    chat_data = chat_data.encode()
    data_len = "{:<15}".format(len(chat_data)).encode()
    try:
        sock.send(data_len + chat_data)
    except:
        sock.close()
        tm.showerror("发送失败")
    else:
        chat_msg_box.delete(1.0, "end")
        chat_record_box.configure(state=tk.NORMAL)
        chat_record_box.insert("end", chat_data.decode() + "\n")
        chat_record_box.configure(state=tk.DISABLED)

def recv_chat_msg():
    global sock
    try:
        while True:
            msg_len_data = sock.recv(15)
            if not msg_len_data:
                break
            msg_len = int(msg_len_data.decode().rstrip())
            # print(msg_len)
            recv_size = 0
            msg_content_data = b""
            while recv_size < msg_len:
                tmp_data = sock.recv(msg_len - recv_size)
                if not tmp_data:
                    break
                recv_size += len(tmp_data)
                msg_content_data += tmp_data
                # print(msg_content_data)
            else:
                # 显示
                chat_record_box.configure(state=tk.NORMAL)
                chat_record_box.insert("end", msg_content_data.decode() + "\n")
                chat_record_box.configure(state=tk.DISABLED)
                continue
            break
    finally:
        sock.close()

        sock = socket.socket()
        sock.connect(("itmojun.com", 9999))

sock = socket.socket()
sock.connect(("itmojun.com", 9999))

root = tk.Tk()
root.title("P1901专属聊天室")
root.minsize(300, 500)

chat_record_box = tk.Text(root)
chat_record_box.configure(state=tk.DISABLED)
chat_record_box.pack(padx=10, pady=10)

chat_msg_box = tk.Text(root)
chat_msg_box.configure(width=65, height=5)
chat_msg_box.pack(side=tk.LEFT, padx=10, pady=10)

send_msg_btn = tk.Button(root, text="发送", command=on_send_msg)
send_msg_btn.pack(side=tk.RIGHT, padx=10, pady=10, ipadx=15, ipady=15)

threading.Thread(target=recv_chat_msg).start()

root.mainloop()
sock.close()