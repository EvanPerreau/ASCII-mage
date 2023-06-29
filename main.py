import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import time
import threading


def image_to_ascii(image, width):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    aspect_ratio = gray_image.shape[1] / gray_image.shape[0]
    height = int(width * aspect_ratio / 2)
    resized_image = cv2.resize(gray_image, (width, height))

    ascii_chars = "$@B%8&WM#*/\|()1[]?-_+~<>i!lI;:,^`'. "

    ascii_art = ''
    for row in resized_image:
        for pixel_value in row:
            ascii_index = int(pixel_value / 255 * (len(ascii_chars) - 1))
            ascii_art += ascii_chars[ascii_index]
        ascii_art += '\n'

    return ascii_art


def webcam_to_ascii(width):
    cap = cv2.VideoCapture(1) ####### /!\ modifier suivant la webcam

    if not cap.isOpened():
        print("Erreur lors de l'ouverture de la capture vidéo")
        return

    ascii_art = ''

    delay_counter = 3

    def update_image():
        nonlocal ascii_art

        ret, frame = cap.read()

        if not ret:
            print("Erreur lors de la lecture de la frame")
            return

        ascii_art = image_to_ascii(frame, width)

        ascii_label.config(text=ascii_art)

        ascii_label.after(30, update_image)

    def save_ascii_image():
        nonlocal delay_counter

        delay_counter = 3
        countdown_thread = threading.Thread(target=countdown)
        countdown_thread.start()

    def countdown():
        nonlocal delay_counter

        save_button.config(state=tk.DISABLED)

        while delay_counter > 0:
            time_label.config(text="Enregistrement dans {}s".format(delay_counter))
            delay_counter -= 1
            time_label.update()
            time.sleep(1)

        save_button.config(state=tk.NORMAL)
        time_label.config(text="")

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        filename = current_time + ".txt"

        with open(filename, "w") as file:
            file.write(ascii_art)

    window = tk.Tk()
    window.title("Webcam ASCII Art")

    ascii_label = tk.Label(window, font=("Courier", 8))
    ascii_label.pack()

    save_button = tk.Button(window, text="Enregistrer", command=save_ascii_image)
    save_button.pack()

    time_label = tk.Label(window, font=("Arial", 12))
    time_label.pack()

    update_image()

    window.mainloop()


if __name__ == '__main__':
    width = 100
    webcam_to_ascii(width)
