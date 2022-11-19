import PySimpleGUI as sg
import cv2

SERVER_ADDRESS = "matebot.local:5000"

cap = cv2.VideoCapture(SERVER_ADDRESS + "/video_feed")


layout = [
            [
                [sg.Text("Connected to: " + SERVER_ADDRESS)],
                [sg.Text(size=(3,1), key='filler', justification='c', pad=(0,0)), sg.Button("🡅")],
                [sg.Button("🡄"), sg.Button("🡇"), sg.Button("🡆")]
            ],
            [
                sg.Image(filename='', key='image')
            ]
        ]

# Create the window
window = sg.Window("Remote", layout)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "🡅" or event == sg.WIN_CLOSED:
        break

    ret, frame = cap.read()
    imgbytes = cv2.imencode('.jpg', frame)[1].tobytes()  # ditto
    window['image'].update(data=imgbytes)

window.close()