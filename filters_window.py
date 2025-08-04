import tkinter as tk

filters_window = None 

def filters_func(parent, change_filter_callback):
    global filters_window

    # Exist window or no
    if filters_window is not None and filters_window.winfo_exists():
        filters_window.lift()  
        return

    filters_window = tk.Toplevel(parent)
    filters_window.title("Filters")
    filters_window.geometry("275x250")

    def set_filter_none():
        change_filter_callback("none")

    def set_filter_gray():
        change_filter_callback("gray")

    def set_filter_red():
        change_filter_callback("red")

    def set_filter_invert():
        change_filter_callback("invert")
    def set_filter_caddy():
        change_filter_callback("caddy")
    def set_filter_facetrack():
        change_filter_callback("facetrack")
    
    btn_frame = tk.Frame(filters_window)
    btn_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

    tk.Button(btn_frame, text="No filter", command=set_filter_none).pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Gray filter", command=set_filter_gray, bg="grey").pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Red filter", command=set_filter_red, bg="red").pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Inversion", command=set_filter_invert, bg="yellow").pack(side=tk.LEFT)
    tk.Button(btn_frame, text="Caddy", command=set_filter_caddy, bg="orange").pack(side=tk.LEFT)

    btn_frame2 = tk.Frame(filters_window)
    btn_frame2.pack(side=tk.TOP, fill=tk.X, pady=5)

    tk.Button(btn_frame2, text="Face track", command=set_filter_facetrack, bg="purple").pack(side=tk.LEFT)

    def on_close():
        global filters_window
        filters_window.destroy()
        filters_window = None

    filters_window.protocol("WM_DELETE_WINDOW", on_close)
