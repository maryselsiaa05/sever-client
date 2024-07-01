import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

HOST = '127.0.0.1'
PORT = 1234
count = 0

root = tk.Tk()
root.geometry("600x600")
root.title("Conversation Room")
root.resizable(False,False)
FONT = ("Helvetica",16)
TFONT = ("Helvetica",9)
BFONT = ("Helvetica",15)
MFONT = ("Helvetica",12)
OB = '#464EBB'
MGREY = '#1F1B24'

try:
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except:
    print("Server is not Available")
    exit(0)

def update_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END,message+'\n')
    message_box.config(state=tk.DISABLED)

def update_team_count(count):
    team_count_num.config(text=count)

def connect():
    try:
        global username
        username = username_textbox.get()
        print(username)
        if username != '':
            print("Connecting....")
            client.connect((HOST,PORT))
            message_button.config(state=tk.NORMAL)
            print(f"Successfully connected to SERVER on {HOST} {PORT}")
            update_message("[SERVER] \"Successfully connected to the HOST\"")
            client.sendall(username.encode())
            username_textbox.config(state=tk.DISABLED)
            username_button.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Invalid Error","Username cannot be empty")
            return 
            
        threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    except:
        messagebox.showerror("Connection Failed",f"Unable to connect to SERVER on {HOST} {PORT}")
        return

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0,len(message)+1)
    else:
        messagebox.showerror("Exit","Empty Message")

root.grid_rowconfigure(0,weight=1)
root.grid_rowconfigure(1,weight=4)
root.grid_rowconfigure(2,weight=1)

top_frame = tk.Frame(root,width=600,height=100,bg="lightblue")
top_frame.grid(row=0,column=0,sticky=tk.NSEW)

middle_frame = tk.Frame(root,width=600,height=400,bg="#000")
middle_frame.grid(row=1,column=0,sticky=tk.NSEW)

bottom_frame = tk.Frame(root,width = 600,height=100,bg='lightblue')
bottom_frame.grid(row=2,column=0,sticky=tk.NSEW)

username_label = tk.Label(top_frame,text="Enter Username : ",font =FONT,fg="#000",bg="lightblue")
username_label.pack(side=tk.LEFT,padx=10)

username_textbox = tk.Entry(top_frame,font=FONT,fg="#000",width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame,text="Join",font=BFONT,bg=OB,fg="#fff",command=connect)
username_button.pack(side=tk.LEFT,padx=38)

message_textbox = tk.Entry(bottom_frame,font=FONT,fg="#000",width=40)
message_textbox.pack(side=tk.LEFT,padx=15)

message_button = tk.Button(bottom_frame,text="Send",font=BFONT,bg=OB,fg="#fff",command=send_message)
message_button.config(state=tk.DISABLED)
message_button.pack(side=tk.LEFT,padx=10)

message_box = scrolledtext.ScrolledText(middle_frame,font=MFONT,bg="white",fg="#000",width=67,height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

team_count = tk.Label(middle_frame,text="Group Strength :",font=TFONT,fg="#fff",bg="#000")
team_count.pack(side=tk.LEFT,padx=10)
team_count_num = tk.Label(middle_frame,font=TFONT,fg="#fff",bg="#000")
team_count_num.pack(side=tk.LEFT)

    
def listen_for_messages_from_server(client):
    try:
        while True:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split('~')[0]
                content = message.split('~')[1]
                count = message.split('~')[2]

                update_message(f"[{username}]   \"{content}\"")
                update_team_count(count)
                
            else:
                messagebox.showerror("Invalid Error","Message recieved from client is empty")
    except:
        update_message(f"!! ~~ SERVER {HOST} {PORT} has Disconnected ~~")
        username_button.config(state=tk.NORMAL)
        username_textbox.config(state=tk.NORMAL)
        message_button.config(state=tk.DISABLED)
        update_team_count("")
        print("Can't reach the SERVER...")
        
def on_closing():
    if messagebox.askokcancel("Quti","Do you want ot Leave from this Chat ?"):
        try:
            if username != '':
               # message = f"{username} has left from the Chat"
                #client.sendall(message.encode())
                client.close()
                print("Disconnected from the server")
        except:
            pass
        finally:
            root.destroy()

def main():
    root.protocol("WM_DELETE_WINDOW",on_closing)
    root.mainloop()

if __name__ == '__main__':
    main()
