import tkinter as tk
import json
import time
import threading
import utils.vkeyboard as vkeyboard
LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

    def stopMouse(self, value="0"):
        with open("settings.json", 'r+') as file:
            curSettings = {}
            s = file.read()
            if s:
                curSettings = json.loads(s)
            curSettings["mouseOpen"] = value
            file.seek(0)
            file.truncate()
            json.dump(curSettings, file, indent=4)
        if value == "0":
            t = threading.Thread(target=time.sleep, args=(60,))
            t.start()
            t.join()
            self.stopMouse(value="1")

    def openKeyboard(self, value="1"):
        with open("settings.json", 'r+') as file:
            curSettings = {}
            s = file.read()
            if s:
                curSettings = json.loads(s)
            curSettings["openKeyboard"] = "1"
            file.seek(0)
            file.truncate()
            json.dump(curSettings, file, indent=4)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="MouseControlMenu", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = tk.Button(self, text="Stop Mouse for a minute",
                           command=lambda: controller.stopMouse())
        button.pack()

        button2 = tk.Button(self, text="Open Keyboard",
                            command=lambda: controller.openKeyboard())
        button2.pack()

        button3 = tk.Button(self, text="Resume Mouse",
                            command=lambda: controller.stopMouse(value="1"))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


def show():
    app = SeaofBTCapp()
    app.attributes('-topmost', True)
    app.geometry("+{}+{}".format(app.winfo_screenwidth(),
                 app.winfo_screenheight()))
    return app


if __name__ == "__main__":
    app = SeaofBTCapp()
    app.mainloop()
