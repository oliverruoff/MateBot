import tkinter as tk
import requests

SERVER_ADDRESS = "http://matebot.local:5000/"

def up_up(event):
    result = requests.get(url = SERVER_ADDRESS + "stop")
    print(result.content)

def up_down(event):
    result = requests.get(url = SERVER_ADDRESS + "move", params = {'forward': True})
    print(result.content)

def down_down(event):
    result = requests.get(url = SERVER_ADDRESS + "move", params = {'forward': False})
    print(result.content)

def down_up(event):
    result = requests.get(url = SERVER_ADDRESS + "stop")
    print(result.content)

def left_down(event):
    result = requests.get(url = SERVER_ADDRESS + "turn", params = {'direction': 'left'})
    print(result.content)

def left_up(event):
    result = requests.get(url = SERVER_ADDRESS + "stop")
    print(result.content)

def right_down(event):
    result = requests.get(url = SERVER_ADDRESS + "turn", params = {'direction': 'right'})
    print(result.content)

def right_up(event):
    result = requests.get(url = SERVER_ADDRESS + "stop")
    print(result.content)

root = tk.Tk()

button_up = tk.Button(root, text="▲")
button_down = tk.Button(root, text="▼")
button_left = tk.Button(root, text="◄")
button_right = tk.Button(root, text="►")

button_up.grid(row=0, column=1, padx='2', pady='2', sticky='ew')
button_up.bind('<ButtonPress-1>', up_down)
button_up.bind('<ButtonRelease-1>', up_up)
button_down.grid(row=1, column=1, padx='2', pady='2', sticky='ew')
button_down.bind('<ButtonPress-1>', down_down)
button_down.bind('<ButtonRelease-1>', down_up)
button_left.grid(row=1, column=0, padx='2', pady='2', sticky='ew')
button_left.bind('<ButtonPress-1>', left_down)
button_left.bind('<ButtonRelease-1>', left_up)
button_right.grid(row=1, column=2, padx='2', pady='2', sticky='ew')
button_right.bind('<ButtonPress-1>', right_down)
button_right.bind('<ButtonRelease-1>', right_up)


root.mainloop()