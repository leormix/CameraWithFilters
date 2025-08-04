import cv2
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import os
from filters_window import filters_func

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


# Папка для сохранения
SAVE_DIR = "../CameraWithFilters"
os.makedirs(SAVE_DIR, exist_ok=True)

# Глобальные переменные
current_filter = None
cap = None
last_display_frame = None
running = False
recording = False
recordedVideo = None
frameRate = 30

root = tk.Tk()
root.title("Video filters")
root.geometry("1300x800")

video_label = tk.Label(root, bg="black")
video_label.pack(fill=tk.BOTH, expand=True)

# Face detection
def detect_bounding_box(vid):
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    for (x, y, w, h) in faces:
        cv2.rectangle(vid, (x, y), (x + w, y + h), (0, 255, 0), 4)
    return faces

# Filter 
def apply_filter(img):

    if current_filter == "gray":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif current_filter == "red":
        b, g, r = cv2.split(img)
        img = cv2.merge((b*0, g*0, r))
    elif current_filter == "invert":
        img = cv2.bitwise_not(img)
    elif current_filter == "caddy":
        img = cv2.GaussianBlur(img, (9, 9), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.Canny(img, 15, 15)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif current_filter == 'facetrack':
        faces = detect_bounding_box(img)
    return img

def update_frame():
    global last_display_frame, recording, recordedVideo
    if running and cap and cap.isOpened():
        ret, img = cap.read()
        if ret:
            img = cv2.flip(img, 1)
            img = apply_filter(img)
            last_display_frame = img.copy()


            if recording and recordedVideo:
                recordedVideo.write(img)


            win_w = video_label.winfo_width()
            win_h = video_label.winfo_height()
            target_w = win_w
            target_h = int(win_w * 9 / 16)
            if target_h > win_h:
                target_h = win_h
                target_w = int(win_h * 16 / 9)

            img_resized = cv2.resize(img, (target_w, target_h))
            img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            img_tk = ImageTk.PhotoImage(Image.fromarray(img_rgb))
            video_label.config(image=img_tk)
            video_label.image = img_tk

    if running:
        root.after(10, update_frame)

def start():
    global cap, running
    if not running:
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FPS, frameRate)
        running = True
        update_frame()

def stop():
    global cap, running, recording, recordedVideo
    running = False
    if cap:
        cap.release()
        cap = None
    if recording:
        toggle_record()  # выключаем запись при остановке
    video_label.config(image='')  # очистка экрана

# Took photo
def screenshot():
    global last_display_frame
    if last_display_frame is not None:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(SAVE_DIR, f"{current_time}.png")
        cv2.imwrite(path, last_display_frame)

def change_filter(new_filter):
    global current_filter
    current_filter = new_filter

# Video record

def toggle_record():
    global recording, recordedVideo
    if not recording:
        if last_display_frame is None:
            return
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        videoFileName = os.path.join(SAVE_DIR, f"{current_time}.avi")
        fourccCode = cv2.VideoWriter_fourcc(*'DIVX')
        h, w = last_display_frame.shape[:2]
        recordedVideo = cv2.VideoWriter(videoFileName, fourccCode, frameRate, (w, h))
        recording = True
        btn_video.config(text="Stop Rec", bg="red")
    else:
        recording = False
        if recordedVideo:
            recordedVideo.release()
            recordedVideo = None
        btn_video.config(text="Video Rec", bg="grey")

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X)

tk.Button(btn_frame, text="▶", width=9, height=2, bg="green", command=start).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="◼", width=9, height=2, bg="red", command=stop).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="Photo", width=9, height=2, bg="blue", command=screenshot).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="Filters", width=9, height=2, bg="orange", command=lambda: filters_func(root, change_filter)).pack(side=tk.LEFT, padx=5, pady=5)

btn_video = tk.Button(btn_frame, text="Video Rec", width=9, height=2, bg="grey", command=toggle_record)
btn_video.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()
