import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)) # Hack sys.path to import from parent directory
import tkinter as tk
import ttkbootstrap as ttks

from tkinter import ttk, PhotoImage
from tkinter.messagebox import askokcancel

from gauge.models import Gear
from pages import *




class MainApplication(ttk.Frame):
    """
    Main application class creates three frames.
    """
    def __init__(self, root, *args, **kwargs):
        # global g_
        ttk.Frame.__init__(self, root)
        root.configure(borderwidth=15, relief="flat")
        
        # g_['gear1'] = 50
        
        self.home_frame = HomeFrame(root)
        self.home_frame.grid(row=0, column=1, sticky="nsew")

        self.calc_frame = CalcFrame(root)
        self.calc_frame.grid(row=0, column=2, sticky="nsew")

        nav_frame = NavBar(root, controller=self, home_frame=self.home_frame, calc_frame=self.calc_frame)
        nav_frame.grid(row=0, column=0, sticky="nsew")


class HomeFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        container = self

        container.grid(padx=20, pady=0, sticky="nsew")

        self.frames = {}

        for sub_frame in (EnterGear, ShowGear):
            page_name = sub_frame.__name__
            frame = sub_frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_frame("EnterGear")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        return frame
    
def on_closing():
    if askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


class CalcFrame(ttk.Frame):
    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        container = self
        container.grid(padx=20, pady=0, sticky="nsew")
        self.frames = {}

        for sub_frame in (SimpleCalculator, StartPage, SpanForm, TtForm, SpttForm):
            page_name = sub_frame.__name__
            frame = sub_frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_frame("SimpleCalculator")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        return frame
    

class NavBar(ttk.Frame):
    def __init__(self, parent, controller, home_frame, calc_frame):
        super(NavBar, self).__init__(parent)
        
        self.gear_buttons = []
                
        self.myImage = PhotoImage(file='images/logo-sm.png')
        ttk.Label(self, image=self.myImage).grid(row=0, column=0, padx=(0,0))

        title = ttk.Label(self, text="Precision Technologies Ltd", anchor="center", font=("Arial", 10), padding=5)
        title.grid(row=1, column=0, sticky="ew")
        self.gear_buttons.append(title)

        for idx, sub_frame in enumerate(home_frame.frames.values(), start=2):
            button = ttk.Button(
                self, 
                text=sub_frame.desc, 
                command=lambda frame=sub_frame: home_frame.show_frame(frame.__class__.__name__)
            )
            button.grid(row=idx, column=0, sticky="ew", columnspan=1)
            self.gear_buttons.append(button)

        spacer1 = tk.Label(self, text="").grid(row=4, column=0)
        self.gear_buttons.append(spacer1)
        
        for idx, sub_frame in enumerate(calc_frame.frames.values(), start=6):
            button = ttk.Button(
                self, 
                text=sub_frame.desc, 
                command=lambda frame=sub_frame: calc_frame.show_frame(frame.__class__.__name__)
            )
            button.grid(row=idx, column=0, sticky="ew", columnspan=1)
            self.gear_buttons.append(button)
   


class EnterGear(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        # print(g_["gear1"])    
        # g_["gear1"] = 49
        # print(g_["gear1"])    
        self.controller = controller
        self.desc = "Enter Gear"
        self.title_label = ttk.Label(self, text="Gear Specifications ...", font=("Arial", 14)).grid(row=0, columnspan=2, pady=(0, 30))

        label_teeth = ttk.Label(self, text="Num of Teeth : ")
        label_teeth.grid(row=1, column=0, sticky="w", padx=10, pady=0)
        label_mod = ttk.Label(self, text="Module : ")
        label_mod.grid(row=2, column=0, sticky="w", padx=10, pady=0)
        label_pa = ttk.Label(self, text="Pressure Angle : ")
        label_pa.grid(row=3, column=0, sticky="w", padx=10, pady=0)
        label_ha = ttk.Label(self, text="Helix Angle : ")
        label_ha.grid(row=4, column=0, sticky="w", padx=10, pady=0)

        self.teeth_entry = ttk.Entry(self)
        self.mod_entry = ttk.Entry(self)
        self.pa_entry = ttk.Entry(self)
        self.ha_entry = ttk.Entry(self)
        self.button1 = ttk.Button(self, text="Create", command=self.generate_gear)

        self.teeth_entry.grid(row=1, column=1, sticky="nsew", padx=0, pady=0)
        self.mod_entry.grid(row=2, column=1, sticky="nsew", padx=0, pady=0)
        self.pa_entry.grid(row=3, column=1, sticky="nsew", padx=0, pady=0)
        self.ha_entry.grid(row=4, column=1, sticky="nsew", padx=0, pady=0)
        self.button1.grid(row=5, column=1, pady=5, padx=5, sticky="E")


    def generate_gear(self):
        teeth = float(self.teeth_entry.get())
        mod = float(self.mod_entry.get())
        pa = float(self.pa_entry.get())
        try :
            ha = float(self.ha_entry.get()) 
        except ValueError:
            ha = 0

        if ha == 0:
            self.master.gear = Gear.make_spur(teeth, mod, pa)


        else:        
            self.master.gear = Gear.make_helical(ha, teeth, mod, pa)        
            
        frame = self.controller.show_frame("ShowGear")
        frame.update_result(str(self.master.gear))
 

class ShowGear(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.desc = "Calculate"
        self.title_label = ttk.Label(self, text="Gear Specification", font=("Arial", 14)).grid()
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.label = ttk.Label(self, text="Gear specifications not yet entered.")
        self.label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        button2 = ttk.Button(self, text="Enter Gear Details", command=lambda: controller.show_frame("EnterGear"))
        button2.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

    # added function to update self.label
    def update_result(self, value):
        self.label.configure(text=value)

def change_theme(theme_name):
    style.theme_use(theme_name)


if __name__ == "__main__":
    """
    Create root an instance of Tkinter.Tk and add menbur.
    """
    root = tk.Tk()
    style = ttks.Style()  # Create the style object without passing the root
    style.theme_use('flatly')  # Use a valid theme name like 'flatly'
    root.title("Gear and Spline Calculator")
    root.geometry("850x600")
    root.eval('tk::PlaceWindow . center')


    # Create a menubar
    menubar = tk.Menu(root)
    menubar.configure(border=1, relief="solid", bg="white")

    # Create a Calculations menu
    calculations_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Calculations", menu=calculations_menu)

    # Add the sub-frames to the Calculations menu
    calculations_menu.add_command(label="Pin Diameter", command=lambda: root.home_frame.show_frame("PINDIA"))
    calculations_menu.add_command(label="Dimension Over Pins", command=lambda: root.home_frame.show_frame("DOP"))
    calculations_menu.add_command(label="Tooth Thickness", command=lambda: root.home_frame.show_frame("TT"))


    # Create a theme menu and add it to the menubar
    theme_menu = tk.Menu(menubar, tearoff=0)
    theme_menu.add_command(label="Flatly", command=lambda: change_theme('flatly'))
    theme_menu.add_command(label="Darkly", command=lambda: change_theme('darkly'))
    theme_menu.add_command(label="Lumen", command=lambda: change_theme('lumen'))
    theme_menu.add_command(label="Cosmo", command=lambda: change_theme('cosmo'))
    theme_menu.add_command(label="Solar", command=lambda: change_theme('solar'))
    menubar.add_cascade(label="Theme", menu=theme_menu)

    # Configure the root window to use the menubar
    root.config(menu=menubar)
    root.protocol("WM_DELETE_WINDOW", on_closing)


    MainApplication(root).grid(row=0, column=0, sticky='nsew')

    root.mainloop()