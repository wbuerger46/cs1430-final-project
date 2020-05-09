from PIL import Image, ImageTk
import tkinter


class PanoramaViewer():
    def __init__(self, image_path, wraps=True):
        self.wraps = wraps
        self.img_path = image_path
        image = Image.open(image_path)
        self.img_width = image.width
        self.img_height = image.height
        self.shift_y = 0
        self.shift_x = 0
        self.scale = 1

        self.window_width = min(400, image.width)
        self.window_height = min(125, image.height)

        self.window = tkinter.Tk()
        self.window.geometry("{}x{}".format(self.window_width, self.window_height))
        #window.resizable(False, False)
        self.canvas = tkinter.Canvas(self.window, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        self.window.bind("<Key>", self.key_press)
        self.window.title("My Panorama Viewer")

        tk_img = ImageTk.PhotoImage(image)
        self.left_img_id = self.canvas.create_image(-image.width+1, 0, image=tk_img, anchor="nw")
        self.right_img_id = self.canvas.create_image(0, 0, image=tk_img, anchor="nw")
        self.window.mainloop()

    def key_press(self, event):
        dx = 0
        dy = 0
        if event.keysym == 'Right':
            dx -= 10
        elif event.keysym == 'Left':
            dx += 10
        elif event.keysym == 'Down':
            dy -=10
        elif event.keysym == 'Up':
            dy += 10
        elif event.keysym == 'w':
            self.zoom(True)
        elif event.keysym == 's':
            self.zoom(False)

        if self.shift_y < dy:
            dy = 0
        elif self.shift_y > self.img_height - self.window_height + dy:
            dy = 0
        
        if self.wraps:
            if self.shift_x < -self.img_width:
                dx -= self.img_width
            elif self.shift_x > 0:
                dx += self.img_width
        else:
            if self.shift_x < dx:
                dx = 0
            elif self.shift_x > self.img_width - self.window_width + dx:
                dx = 0

        self.canvas.move(self.left_img_id, dx, dy)
        self.canvas.move(self.right_img_id, dx, dy)
        self.shift_x -= dx
        self.shift_y -= dy

    def zoom(self, zoom_in):
        if zoom_in:
            self.scale *= 1.1
        else:
            if (self.img_height * self.scale / 1.1 <= self.window_height):
                return
            self.scale /= 1.1
        image = Image.open(self.img_path).resize(
            (int(self.img_width*self.scale), int(self.img_height*self.scale)), Image.ANTIALIAS)
        newImage = ImageTk.PhotoImage(image)
        self.canvas.itemconfig(self.right_img_id, image=newImage)
        self.canvas.itemconfig(self.left_img_id, image=newImage)

        dx = int((1.1 * self.window_width - self.window_width) / 2)
        if zoom_in:
            dx *= -1
        self.canvas.move(self.right_img_id, dx, 0)

        self.window.mainloop()

if __name__ == "__main__":
    PanoramaViewer("pano5.jpg", True)