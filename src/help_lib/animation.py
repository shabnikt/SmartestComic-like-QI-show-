import tkinter
import customtkinter
from os import listdir
from help_lib.helper import get_img


def frame_animation(widget, next_func, frames, frame_num=0, duration=42):
    if frame_num < len(frames):
        img = get_img(frames[frame_num])
        widget.configure(image=img)
        widget.image = img
        widget.after(duration, frame_animation, widget, next_func, frames, frame_num + 1, duration)
    else:
        next_func()


def animate_text(text, widget, next_func):
    t = widget.cget('text')
    if t != text:
        t += text.replace(t, '')[0]
        widget.configure(text=t)
        widget.after(40, animate_text, text, widget, next_func)
    else:
        next_func()
