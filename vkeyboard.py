BUTTON_BACKGROUND 		= "black"
MAIN_FRAME_BACKGROUND 	= "cornflowerblue"
BUTTON_LOOK 			= "flat" #flat, groove, raised, ridge, solid, or sunken
TOP_BAR_TITLE 			= "Python Virtual KeyBoard."
TOPBAR_BACKGROUND 		= "skyblue"
TRANSPARENCY 			= 0.7
FONT_COLOR 				= "white"

try:
    import Tkinter
except:
    import tkinter as Tkinter

import pyautogui, json, sys

keys =[ 
[


    [

        ("Function_Keys"),

        ({'side':'top','expand':'yes','fill':'both'}),
        [
            ('esc', 'F1', 'F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12')
        ]
    ],

    [
        ("Character_Keys"),
        ({'side':'top','expand':'yes','fill':'both'}),
        [
            ('`',',','.','/','-','=','\\','[',']','backspace'),
            ('~','!','@','#','$','%','^','&','*','(',')','_','+','|'),
            ('tab','q','w','e','r','t','y','u','i','o','p','{','}',";",'\''),
            ('capslock','a','s','d','f','g','h','j','k','l',':',"\"","enter"),
            ("shift",'z','x','c','v','b','n','m','<','>','?',"shift"),
            ("ctrl", "win",'alt','space  ','alt','win','[=]','ctrl')
        ]
    ]
],
[
    [
        ("System_Keys"),
        ({'side':'top','expand':'yes','fill':'both'}),
        [
            (
                "printscreen",
                "scrolllock",
                "pause"
            )
        ]
    ],
    [          
        ("Editing_Keys"),
        ({'side':'top','expand':'yes','fill':'both'}),
        [
            (
                "insert",
                "home",
                "pageup"
                ),
            (	"delete",
                "end",
                "pagedown"
                ),

        ]
    ],

    [
        ("Navigation_Keys"),
        ({'side':'top','expand':'yes','fill':'both'}),
        [
            (
                "up",
                ),
            (	"right",
                "down",
                "left"
                ),
        ]
    ],

],
[

    [
        ("Numeric_Keys"),
        ({'side':'top','expand':'yes','fill':'both'}),
        [
            ("numlock","/","*"),
            ("7","8","9","+"),
            ("4","5","6","-"),
            ("1","2","3","0"),
            (".","enter")
        ]
    ],

]

]

# Create key event
def create_keyboard_event(numlock, capslock, controler, key):
    return

##  Frame Class
class Keyboard(Tkinter.Frame):
    def __init__(self, *args, **kwargs):
        Tkinter.Frame.__init__(self, *args, **kwargs)
        

        self.create_frames_and_buttons()



    def create_frames_and_buttons(self):
        for key_section in keys:
            store_section = Tkinter.Frame(self)
            store_section.pack(side='left',expand='yes',fill='both',padx=10,pady=10,ipadx=10,ipady=10)
            
            for layer_name, layer_properties, layer_keys in key_section:
                store_layer = Tkinter.LabelFrame(store_section)#, text=layer_name)
                #store_layer.pack(side='top',expand='yes',fill='both')
                store_layer.pack(layer_properties)
                for key_bunch in layer_keys:
                    store_key_frame = Tkinter.Frame(store_layer)
                    store_key_frame.pack(side='top',expand='yes',fill='both')
                    for k in key_bunch:
                        k=k.capitalize()
                        if len(k)<=3:
                            store_button = Tkinter.Button(store_key_frame, text=k, width=4, height=2)
                        else:
                            store_button = Tkinter.Button(store_key_frame, text=k.center(5,' '), height=2)
                        if " " in k:
                            store_button['state']='disable'
                        
                        store_button['relief']=BUTTON_LOOK
                        store_button['bg']=BUTTON_BACKGROUND
                        store_button['fg']=FONT_COLOR

                        store_button['command']=lambda q=k.lower(): self.button_command(q)
                        store_button.pack(side='left',fill='both',expand='yes')
        return

        # Function For Detecting Pressed Keyword.
    def button_command(self, event):
        pyautogui.press(event)
        return

class top_moving_mechanism:
    def __init__(self, root, label):
        self.root = root
        self.label = label

    def motion_activate(self, kwargs):
        w,h = (self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        (x,y) = (kwargs.x_root, kwargs.y_root)
        self.root.geometry("%dx%d+%d+%d" % (w,h,x,y))
        return


def move_window_to_bottom_center(window):
  """Moves the window to the bottom center of the screen.

  Args:
    window: The window to move.
  """

  # Get the screen size.
#   screen_size = window.winfo_screenwidth(), window.winfo_screenheight()

#   # Get the window size.
#   window_size = window.winfo_width(), window.winfo_height()

#   # Calculate the x and y coordinates of the bottom center of the screen.
#   x = screen_size[0] - window_size[0] // 2
#   y = screen_size[1] - window_size[1]
#   print(x,y)
  window.geometry("+%d+%d" % (100, 700))


def main(startMinimized=True):

    root = Tkinter.Tk(className=TOP_BAR_TITLE)
    def closeKeyboard():
        with open("settings.json", 'r+') as file:
            curSettings = {}
            s = file.read()
            if s:
                curSettings = json.loads(s)
            curSettings["openKeyboard"] = "0"
            file.seek(0)
            file.truncate()
            json.dump(curSettings, file, indent=4)
        root.destroy()
    k=Keyboard(root, bg=MAIN_FRAME_BACKGROUND)

    root.overrideredirect(True)
    root.wait_visibility(root)
    root.wm_attributes('-alpha',TRANSPARENCY)
    f = Tkinter.Frame(root)
    t_bar=Tkinter.Label(f, text=TOP_BAR_TITLE, bg=TOPBAR_BACKGROUND)
    t_bar.pack(side='left',expand="yes", fill="both")
    mechanism = top_moving_mechanism(root, t_bar)
    t_bar.bind("<B1-Motion>", mechanism.motion_activate)
    Tkinter.Button(f, text="[X]", command= closeKeyboard).pack(side='right')
    f.pack(side='top', expand='yes',fill='both')
    k.pack(side='top')
    move_window_to_bottom_center(root)

    root.mainloop()
    sys.exit()
if __name__=='__main__':
    main()