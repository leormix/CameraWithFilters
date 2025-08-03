import cv2
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import os
from filters_window import filters_func

current_filter = None
cap = None
last_display_frame = None
running = False  

SAVE_DIR = "../Camera"
os.makedirs(SAVE_DIR, exist_ok=True)

root = tk.Tk()
root.title("Video filters")
root.geometry("1300x800")

video_label = tk.Label(root, bg="black")
video_label.pack(fill=tk.BOTH, expand=True)

def update_frame():
    global last_display_frame, current_filter
    if running and cap and cap.isOpened():
        ret, img = cap.read()
        if ret:
            img = cv2.flip(img, 1)

            # Enable filter
            if current_filter == "gray":
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) 
            elif current_filter == "red":
                # Delete colors
                b, g, r = cv2.split(img)
                img = cv2.merge((b*0, g*0, r))
            elif current_filter == "invert":
                img = cv2.bitwise_not(img)
            elif current_filter == "caddy":
                img = cv2.GaussianBlur(img, (9, 9), 0)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                img = cv2.Canny(img, 15, 15)

            win_w = video_label.winfo_width()
            win_h = video_label.winfo_height()

            target_w = win_w
            target_h = int(win_w * 9 / 16)
            if target_h > win_h:
                target_h = win_h
                target_w = int(win_h * 16 / 9)

            img_resized = cv2.resize(img, (target_w, target_h))
            last_display_frame = img_resized.copy()

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
        running = True
        update_frame()

def stop():
    global cap, running
    running = False
    if cap:
        cap.release()
        cap = None
    video_label.config(image='')  # clear screen

def screenshot():
    global last_display_frame
    if last_display_frame is not None:
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(SAVE_DIR, f"{current_time}.png")
        cv2.imwrite(path, last_display_frame)

def change_filter(new_filter):
    global current_filter
    current_filter = new_filter


btn_frame = tk.Frame(root)
btn_frame.pack(fill=tk.X)

tk.Button(btn_frame, text="▶", width=9, height=2, bg="green", command=start).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="◼", width=9, height=2, bg="red", command=stop).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="Photo", width=9, height=2, bg="blue", command=screenshot).pack(side=tk.LEFT, padx=5, pady=5)
tk.Button(btn_frame, text="Filters", width=9, height=2, bg="orange",command=lambda: filters_func(root, change_filter)).pack(side=tk.LEFT, padx=5, pady=5)


root.mainloop()
