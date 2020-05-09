from PIL import Image, ImageTk
import tkinter

def view_image(image_path):
    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)
    img_view = tkinter.Label(window, image=tk_img)
    window.geometry("{}x{}+100+100".format(400, 200))
    img_view.place(x=curr_window_x, y=curr_window_y, \
        width=100, height=100)
    #window.resizable(False, False)
    window.mainloop()

def key_press(event):
    curr_window_x -= 10
    img_view.place(x=x, y=y, width=img.size[0], height=img.size[1])
    #window.mainloop()

window = tkinter.Tk()
window.bind("<Key>", key_press)
window.title("My Panorama Viewer")
curr_window_x = 0
curr_window_y = 0
img_view = None