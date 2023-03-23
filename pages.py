import sys
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Button
from pathlib import Path
from functools import partial
# from main import g_


sys.path.append(str(Path(__file__).resolve().parent.parent)) # Hack sys.path to import from parent directory

from gauge.models import Gear



class StartPage(ttk.Frame):

    def __init__(self, parent, controller, master):
        ttk.Frame.__init__(self, parent)
        self.desc = "Start Page"
        self.master = master
        self.controller = controller
        self.grid(padx=20, pady=20, sticky="nsew")
        
        self.title_label = ttk.Label(self, text="Calculations Pane").grid(row=0)


class SpanForm(ttk.Frame):
    def __init__(self, parent, controller, master):
        super().__init__(parent)
        parent = parent
        self.desc = "Span"
        self.master = master
        self.controller = controller
        self.grid()
        self.title_label = tk.Label(self, text="Calculate Span Size:").grid(pady=10)
        
        
        self.num1_label = tk.Label(self, text="Tooth Thickness:").grid()
        self.num1_entry = tk.Entry(self)
        self.num1_entry.grid()

        self.num2_label = tk.Label(self, text="No. of Teeth to Span:").grid()
        self.num2_entry = tk.Entry(self)
        self.num2_entry.grid()

        self.calculate_button = tk.Button(self, text="Calculate", command=lambda: self.calc_span())

        self.calculate_button.grid(sticky=(tk.W, tk.E))
        
        self.result_label = tk.Label(self, text="Result:")
        self.result_label.grid(pady=10)


        self.result_label = tk.Label(self, text="Base Tangent :").grid()

        self.result_value = tk.StringVar()
        self.result_entry = tk.Entry(self, textvariable=self.result_value, state='readonly')
        self.result_entry.grid()
    
        self.result_label = tk.Label(self, text="Contact diameter :").grid()
        
        self.result_value_imp = tk.StringVar()
        self.result_entry_imp = tk.Entry(self, textvariable=self.result_value_imp, state='readonly')
        self.result_entry_imp.grid()
        
        
    def calc_span(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            
            # This lines causes the error - AttributeError: '_tkinter.tkapp' object has no attribute 'gear'
            base_tangent, contact_diameter = self.master.gear.add(num1, num2)

                
            base_tangent = f" {base_tangent:.4f} ({base_tangent/25.4:.5f})"
            contact_diameter = f"{contact_diameter:.4f} ({contact_diameter/25.4:.5f})"
            
            self.result_value.set(base_tangent)
            self.result_value_imp.set(contact_diameter)
        except ValueError:
            self.result_value.set("Invalid input. Please enter numbers.")

