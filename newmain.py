""" Improved substantially by Thingamabobs from SO, but still needs work"""



import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent)) # Hack sys.path to import from parent directory
from pprint import pprint

import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttks
from tkinter.messagebox import askokcancel
from gauge.models import Gear


class BaseFrame(ttk.Frame):

    def __init__(self, parent, desc):
        super().__init__(parent)
        self.desc = desc
        self.controller = parent
        

class StartPage(BaseFrame):

    def __init__(self, parent):
        super().__init__(parent, "Start Page")
        self.title_label = ttk.Label(self, text="Calculations Pane")
        self.title_label.grid(row=0)


class SpanForm(BaseFrame):
    
    def __init__(self, parent):
        super().__init__(parent, "Span")
        #children
        self.title_label = tk.Label(self, text="Calculate Span Size:")
        self.num1_label = tk.Label(self, text="Tooth Thickness:")
        self.num1_entry = tk.Entry(self)
        self.num2_label = tk.Label(self, text="No. of Teeth to Span:")
        self.num2_entry = tk.Entry(self)
        self.calculate_button = tk.Button(self, text="Calculate", command=self.calc_span)
        
        self.result_label = tk.Label(self, text="Result:")
        self.result_label_tan = tk.Label(self, text="Base Tangent :")
        self.result_value = tk.StringVar()
        self.result_entry = tk.Entry(self, textvariable=self.result_value, state='readonly')
        self.result_label_dia = tk.Label(self, text="Contact diameter :")
        self.result_value_imp = tk.StringVar()
        self.result_entry_imp = tk.Entry(self, textvariable=self.result_value_imp, state='readonly')
        
        #children geometry
        self.title_label.grid(pady=10)
        self.num1_label.grid()
        self.num1_entry.grid()
        self.num2_label.grid()
        self.num2_entry.grid()
        self.calculate_button.grid(sticky=(tk.W, tk.E))
        self.result_label.grid(pady=10)
        self.result_label_tan.grid()
        self.result_entry.grid()
        self.result_label_dia.grid()
        self.result_entry_imp.grid()
        
    def calc_span(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            pprint("Self: ")
            pprint(vars(self))
            pprint("Self.Master: ")
            pprint(vars(self.master))
            tan, d = self.master.master.home_frame.gear.add(num1, num2), self.master.master.home_frame.gear.add(num1, num2)
            # tan, d = self.master.calc_frame.gear.add(num1, num2)                
            base_tangent = f" {tan:.4f} ({tan/25.4:.5f})"
            contact_diameter = f"{d:.4f} ({d/25.4:.5f})"
            #set results
            self.result_value.set(base_tangent)
            self.result_value_imp.set(contact_diameter)
        except ValueError:
            self.result_value.set("Invalid input. Please enter numbers.")


class MainApplication(tk.Tk):
    """
    Main application class creates three frames.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()
        #menubar
        self.menubar = tk.Menu(self)
        self.menubar.configure(border=1, relief="solid", bg="white")
        #Calculations menu
        self.calculations_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(
            label="Calculations", menu=self.calculations_menu)
        
        def show_frame_factory(name):
            'Returns a lambda expression for passing arg to show_frame'
            return lambda arg=name: self.home_frame.show_frame(arg)
        
        calc_menu = {
            "Pin Diameter"          : show_frame_factory("PINDIA"),
            "Dimension Over Pins"   : show_frame_factory("DOP"),
            "Tooth Thickness"       : show_frame_factory("TT")
            }
        
        for text, cmd in calc_menu.items():
            self.calculations_menu.add_command(label=text, command=cmd)
            
        #Theme menu
        self.theme_menu = tk.Menu(self.menubar, tearoff=0)  
        self.menubar.add_cascade(label="Theme", menu=self.theme_menu)
        
        def change_theme_factory(name):
            'Returns a lambda expression for passing arg to change_theme'
            return lambda arg=name: self.change_theme(arg)
        
        theme_menu = {
            "Flatly"    : change_theme_factory('flatly'),
            "Darkly"    : change_theme_factory('darkly'),
            "Lumen"     : change_theme_factory('lumen'),
            "Cosmo"     : change_theme_factory('cosmo'),
            "Solar"     : change_theme_factory('solar')
            }
        
        for text, cmd in theme_menu.items():
            self.theme_menu.add_command(label=text, command=cmd)
        
        #setup
        self.title("Gear and Spline Calculator")
        self.geometry("850x600")
        self.eval('tk::PlaceWindow . center')
        self.configure(borderwidth=15, relief="flat", menu=self.menubar)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.style = ttks.Style()
        self.style.theme_use('flatly')
        #children        
        self.home_frame = HomeFrame(self)
        self.calc_frame = CalcFrame(self)
        self.nav_frame = NavBar(self)
        #children geometry
        self.home_frame.grid(row=0, column=1, sticky="nsew")
        self.calc_frame.grid(row=0, column=2, sticky="nsew")
        self.nav_frame.grid(row=0, column=0, sticky="nsew")

    def on_closing(self):
        if askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def change_theme(self, theme_name):
        self.style.theme_use(theme_name)


class HomeFrame(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.frames = {}

        for sub_frame in (EnterGear, ShowGear):
            page_name = sub_frame.__name__
            frame = sub_frame(parent=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.show_frame("EnterGear")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        return frame

class CalcFrame(ttk.Frame):
    
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.frames = {}
        self.frames["StartPage"] = StartPage(parent=self)
        self.frames["SpanForm"] = SpanForm(parent=self)
        self.frames["StartPage"].grid(row=0, column=0, sticky="nsew")
        self.frames["SpanForm"].grid(row=0, column=0, sticky="nsew") 
        self.show_frame("SpanForm")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        return frame
    

class NavBar(ttk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.logo = ttk.Label(self, text="Logo Place Holder")
        self.title = ttk.Label(self,
                               text="Precision Technologies Ltd",
                               font=("Arial", 10),
                               anchor="center", padding=5)
        self.spacer1 = tk.Label(self, text="")
        self.logo.grid(row=0, column=0, padx=(0,0))
        self.title.grid(row=1, column=0, sticky="ew")
        self.spacer1.grid(row=4, column=0)

        def button_factory(obj, start):
            
            def cmd_factory(name):
                return lambda arg=name: obj.show_frame(arg)
            
            for idx, (name,sub) in enumerate(obj.frames.items(), start=start):
                b = ttk.Button(self, text=sub.desc, command=cmd_factory(name))
                b.grid(row=idx, column=0, sticky="ew")

        button_factory(parent.home_frame, 2)
        button_factory(parent.calc_frame, 6)
   


class EnterGear(ttk.Frame):

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.controller = parent
        self.desc = "Enter Gear"
        #children
        self.title_label = ttk.Label(
            self, text="Gear Specifications ...", font=("Arial", 14))
        self.label_teeth = ttk.Label(self, text="Num of Teeth : ")
        self.label_mod = ttk.Label(self, text="Module : ")
        self.label_pa = ttk.Label(self, text="Pressure Angle : ")
        self.label_ha = ttk.Label(self, text="Helix Angle : ")
        self.teeth_entry = ttk.Entry(self)
        self.mod_entry = ttk.Entry(self)
        self.pa_entry = ttk.Entry(self)
        self.ha_entry = ttk.Entry(self)
        self.button1 = ttk.Button(
            self, text="Create", command=self.generate_gear)
        #geometry
        self.title_label.grid(row=0, columnspan=2, pady=(0, 30))
        lbl_kw = {'column':0,'sticky':"w",'padx':10}
        self.label_teeth.grid(row=1, **lbl_kw)
        self.label_mod.grid(row=2, **lbl_kw)
        self.label_pa.grid(row=3, **lbl_kw)
        self.label_ha.grid(row=4, **lbl_kw)
        enty_kw = {'column':1,'sticky':"nsew"}
        self.teeth_entry.grid(row=1, **enty_kw)
        self.mod_entry.grid(row=2, **enty_kw)
        self.pa_entry.grid(row=3, **enty_kw)
        self.ha_entry.grid(row=4, **enty_kw)
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

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.controller = parent
        self.desc = "Calculate"
        self.title_label = ttk.Label(
            self, text="Gear Specification", font=("Arial", 14))
        self.title_label.grid()
        self.label = ttk.Label(
            self, text="Gear specifications not yet entered.")
        self.label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        button2 = ttk.Button(
            self, text="Enter Gear Details",
            command=lambda: self.controller.show_frame("EnterGear"))
        button2.grid(row=2, column=0, pady=5, padx=5, sticky="nsew")

    # added function to update self.label
    def update_result(self, value):
        self.label.configure(text=value)


if __name__ == "__main__":
    """
    Create root an instance of Tkinter.Tk and add menbur.
    """
    root = MainApplication()
    root.mainloop()