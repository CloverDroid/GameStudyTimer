import tkinter as tk
from tkinter import ttk
from random import randint
from PIL import Image, ImageTk
import os
import pathlib


class Window(tk.Toplevel):

    def __init__(self, parent, img):
        super().__init__(parent)
        #self.photo = tk.PhotoImage(file= r"PYTHON PRACTICEs\\GameStudyTimer\\trollface.png")        
        self.geometry('350x350')
        self.photo = img.resize((350,350))
        self.photo = ImageTk.PhotoImage(self.photo)
        self.title('Toplevel Window')
        self.randomPosition(self)

        ttk.Button(self,
                text='Close',
                command=self.destroy,image=self.photo).pack(expand=True)
        
    def randomPosition(self, win):
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = randint(w,ws-w)
        y = randint(h,hs-h)
        win.geometry('+%d+%d' % (x, y))
        # print(f"W:{w}, H:{h}, WS:{ws}, HS:{hs}, X:{x}, Y{y}")

class App(tk.Tk):
    
    def __init__(self, img):
        super().__init__()  
        
        self.title('Main Window')
        self.photo = img
        self.attributes('-alpha',0.15)
        # place a button on the root window
        self.randomPosition(self)
        ttk.Button(self,
                text='CLOSE',
                command=self.open_window).pack(expand=True)
        self.open_window()

    def open_window(self):
        for x in range(randint(4,8)):
            window = Window(self, img=self.photo)
            window.grab_set()

    def randomPosition(self, win):
        w = win.winfo_reqwidth()
        h = win.winfo_reqheight()
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = randint(w,ws-w)
        y = randint(h,hs-h)
        win.geometry('+%d+%d' % (x, y))


if __name__ == "__main__":
    try:
        cwd = os.getcwd()
        script_location = pathlib.Path(__file__).parent
        data_loc = script_location.parent.joinpath("GameStudyTimer")
        img_name = 'trollface.png'
        imgdir = data_loc.joinpath(img_name)
        photo = Image.open(imgdir)

        app = App(photo)
        app.mainloop()
    except Exception as e:
        pass
    