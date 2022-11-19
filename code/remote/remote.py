import tkinter as tk


def up():
    print('up')

def down_down(event):
    print('down down', event)

def down_up(event):
    print('down up', event)

def left():
    pass

def right():
    pass

root = tk.Tk()

button_up = tk.Button(root, text="▲")
button_down = tk.Button(root, text="▼")
button_left = tk.Button(root, text="◄")
button_right = tk.Button(root, text="►")

button_up.grid(row=0, column=1, padx='2', pady='2', sticky='ew')
button_down.grid(row=1, column=1, padx='2', pady='2', sticky='ew')
button_down.bind('<ButtonPress-1>', down_down)
button_down.bind('<ButtonRelease-1>', down_up)
button_left.grid(row=1, column=0, padx='2', pady='2', sticky='ew')
button_right.grid(row=1, column=2, padx='2', pady='2', sticky='ew')


root.mainloop()