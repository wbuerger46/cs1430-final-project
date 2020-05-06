from PIL import Image, ImageTk
import tkinter

left_img_id = 0
right_img_id = 0
tk_img = None
canvas = None
img_width = 0
img_height = 0
window_width = 0
window_height = 0
shift_x = 0
shift_y = 0
wrapping = True

def view_image(image_path, wraps=True):
    global left_img_id, right_img_id, canvas, img_width, img_height, \
         window_width, window_height, tk_img, wrapping
    wrapping = wraps
    image = Image.open(image_path)
    img_width = image.width
    img_height = image.height

    window_width = min(600, img_width)
    window_height = min(350, img_width)
    img_id = None
    window = tkinter.Tk()
    window.geometry("{}x{}".format(window_width, window_height))
    window.resizable(False, False)
    canvas = tkinter.Canvas(window, width=window_width, height=window_height)
    canvas.pack()

    window.bind("<Key>", key_press)
    window.title("My Panorama Viewer")

    tk_img = ImageTk.PhotoImage(image)
    left_img_id = canvas.create_image(-image.width/2, image.height/2, image=tk_img)
    right_img_id = canvas.create_image(image.width/2, image.height/2, image=tk_img)
    window.mainloop()

def key_press(event):
    global canvas, img_width, img_height, window_width, window_height, \
        shift_x, shift_y, wrapping
    dx = 0
    dy = 0
    if event.keysym == 'Right':
        dx -= 10
    elif event.keysym == 'Left':
        dx += 10
    elif event.keysym == 'Down':
        dy -= 10
    elif event.keysym == 'Up':
        dy += 10

    if shift_y - dy < 0:
        dy = 0
    elif shift_y - dy > img_height - window_height:
        dy = 0

    if wrapping:
        if shift_x < -img_width:
            dx -= img_width
        elif shift_x > 0:
            dx += img_width
    else:
        if shift_x - dx < 0:
            dx = 0
        elif shift_x - dx > img_width - window_width:
            dx = 0

    canvas.move(left_img_id, dx, dy)
    canvas.move(right_img_id, dx, dy)
    shift_x -= dx
    shift_y -= dy


if __name__ == "__main__":
    view_image("sample_image.jpg", True)