from PIL import Image, ImageTk
import tkinter


class PanoramaViewer():
    def __init__(self, image_path, wraps=True):
        self.wraps = wraps
        self.img_path = image_path
        image = Image.open(image_path)
        self.img_width = 2 * image.width
        self.img_height = 2 * image.height
        image = image.resize((2*image.width, 2*image.height))
        self.shift_y = 0
        self.shift_x = 0
        self.scale = 1

        self.window_width = min(600, image.width)
        self.window_height = min(300, image.height)

        window = tkinter.Tk()
        window.geometry("{}x{}".format(self.window_width, self.window_height))
        window.resizable(False, False)
        self.canvas = tkinter.Canvas(window, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        window.bind("<Key>", self.key_press)
        window.title("My Panorama Viewer")

        tk_img = ImageTk.PhotoImage(image)
        self.left_img_id = self.canvas.create_image(-image.width+1, 0, image=tk_img, anchor="nw")
        self.right_img_id = self.canvas.create_image(0, 0, image=tk_img, anchor="nw")
        window.mainloop()

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

if __name__ == "__main__":
    PanoramaViewer("pano5.jpg", True)