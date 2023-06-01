import cv2
import sys
import utils.menu as menu
import json
import time
import threading
import utils.vkeyboard as vkeyboard
import screeninfo
from test import *
import numpy as np
import mediapipe as mp
import pyautogui as pyag
from multiprocessing import Process

monitors = screeninfo.get_monitors()
SCREEN_WIDTH, SCREEN_HEIGHT = monitors[0].width, monitors[0].height
READ_INPUT = True

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5)

mp_drawing = mp.solutions.drawing_utils

wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

prev_x, prev_y = 1, 1
prev_pos = (0, 0)
pyag.FAILSAFE = False
frameR = 100
SMOOTHENING = 17  # SENSITIVITY
wScr, hScr = monitors[0].width, monitors[0].height
plocX, plocY = 0, 0
clocX, clocY = 0, 0
RIGHT_EYE_RATIO, LEFT_EYE_RATIO = 0.015, 0.015
OPEN_KEYBOARD = False


def show_menu():
    """
    Displays TKinter menu on screen
    """
    app = menu.show()
    app.mainloop()


def show_keyboard():
    """Displays a virtual on-screen keyboard
    """
    vkeyboard.main()


proc = Process(target=show_menu)
proc.start()
frameRead = 0
screen_size = pyag.size()


def check_settings():
    """
    Reads settings.json to update config variables
    """
    global READ_INPUT, OPEN_KEYBOARD, RIGHT_EYE_RATIO, LEFT_EYE_RATIO, SMOOTHENING
    while True:
        with open("settings.json") as file:
            s = file.read()
            if s:
                s = json.loads(s)
                if s.get("mouseOpen") == "0":
                    READ_INPUT = False
                else:
                    READ_INPUT = True

                if s.get("openKeyboard") == "1":
                    if not OPEN_KEYBOARD:
                        Process(target=show_keyboard).start()
                        OPEN_KEYBOARD = True
                else:
                    OPEN_KEYBOARD = False
                RIGHT_EYE_RATIO = float(s.get("righteye", 0.015))
                LEFT_EYE_RATIO = float(s.get("righteye", 0.015))
                SMOOTHENING = int(s.get("sensitivity", 17))
        time.sleep(2)


threading.Thread(target=check_settings).start()
img_h, img_w = 480, 640
single_blink = False
last_blinks = []
blink_and_hold = False
while cap.isOpened():
    success, image = cap.read()
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = face_mesh.process(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    face_3d = []
    face_2d = []
    if READ_INPUT:
        frameRead += 1
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                clicked = False
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)
                            sP = (lm.x * SCREEN_WIDTH, lm.y * SCREEN_HEIGHT)
                        x, y = int(lm.x * img_w), int(lm.y * img_h)
                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])
                face_2d = np.array(face_2d, dtype=np.float64)

                left_eye = [face_landmarks.landmark[145],
                            face_landmarks.landmark[159]]
                right_eye = [face_landmarks.landmark[374],
                             face_landmarks.landmark[386]]

                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                dist_matrix = np.zeros((4, 1), dtype=np.float64)

                success, rot_vec, trans_vec = cv2.solvePnP(
                    face_3d, face_2d, cam_matrix, dist_matrix)

                rmat, jac = cv2.Rodrigues(rot_vec)

                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                x3 = np.interp(p2[0], (frameR, wCam-frameR), (0, wScr))
                y3 = np.interp(p2[1], (frameR, hCam - frameR), (0, hScr))

                # for landmark in left_eye:
                #     x_ = int(landmark.x * img_w)
                #     y_ = int(landmark.y * img_h)
                right_clicked = False

                if (right_eye[0].y - right_eye[1].y < RIGHT_EYE_RATIO):
                    right_clicked = True
                if (left_eye[0].y - left_eye[1].y < LEFT_EYE_RATIO):
                    if right_clicked:
                        if frameRead > 8:
                            frameRead = 0
                            pyag.doubleClick()
                            right_clicked = False
                            break
                    last_blinks.append(True)
                    if frameRead > 8:
                        frameRead = 0

                        if all(last_blinks[-4:]):
                            blink_and_hold = True
                            if x < -10:
                                # Scroll down
                                pyag.scroll(-10)
                            elif x > 10:
                                # Scroll up
                                pyag.scroll(10)

                        else:
                            last_blinks.append(True)
                            frameRead = 0
                            pyag.click()
                            break
                else:
                    last_blinks.append(False)
                if right_clicked:
                    if frameRead > 8:
                        pyag.click(button="right")
                        break

                if abs(prev_x - x) > 0.3 or abs(prev_y - y) > 0.3:
                    clocX = plocX + (x3 - plocX) / SMOOTHENING
                    clocY = plocY + (y3 - plocY) / SMOOTHENING
                    pyag.moveTo(clocX, clocY)  # , tween=pyag.easeOutQuad
                    plocX, plocY = clocX, clocY
                    prev_x, prev_y = x, y
                last_blinks = last_blinks[-30:]
    cv2.imshow('Mouse Control using Head Gestures', image)
    if cv2.waitKey(1) & 0xFF == 27:
        sys.exit()
