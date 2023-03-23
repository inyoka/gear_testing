import sys
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Button
from pathlib import Path
from functools import partial
# from main import g_


sys.path.append(str(Path(__file__).resolve().parent.parent)) # Hack sys.path to import from parent directory

from gauge.models import Gear


__all__ = ["StartPage", "SpanForm", "SimpleCalculator", "TtForm", "SpttForm"]



class SpttForm(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.title = "SPTT"
        self.desc = "Tooth Thickness from Span"      


class StartPage(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.desc = "Start Page"

        self.controller = controller
        self.grid(padx=20, pady=20, sticky="nsew")
        
        self.title_label = ttk.Label(self, text="Calculations Pane").grid(row=0)


class SpanForm(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        parent = parent
        self.desc = "Span"
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
            
            if self.master.gear.type == "Spur":
                base_tangent, contact_diameter = self.master.gear.find_span_spur(num1, num2)
            elif self.master.gear.type == "Helical":
                base_tangent, contact_diameter = self.master.gear.find_span_spur_hel(num1, num2)
                
            base_tangent = f" {base_tangent:.4f} ({base_tangent/25.4:.5f})"
            contact_diameter = f"{contact_diameter:.4f} ({contact_diameter/25.4:.5f})"
            
            self.result_value.set(base_tangent)
            self.result_value_imp.set(contact_diameter)
        except ValueError:
            self.result_value.set("Invalid input. Please enter numbers.")


class TtForm(ttk.Frame):
    """Tooth Thickness Calculator
    Args:
        float : Pin Diameter
        float : Dimensions Over Pin 
    Returns:
        float: Tooth Thickness
    """
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.desc = "Tooth Thickness"
        self.grid()
        self.title_label = tk.Label(self, text="Calculate Tooth Thickness:").grid(pady=10)
        
        
        self.num1_label = tk.Label(self, text="Pin Diameter:").grid()
        self.num1_entry = tk.Entry(self)
        self.num1_entry.grid()

        self.num2_label = tk.Label(self, text="Dimension Over Pins:").grid()
        self.num2_entry = tk.Entry(self)
        self.num2_entry.grid()

        self.calculate_button = tk.Button(self, text="Calculate", command=self.calc_span)
        self.calculate_button.grid(sticky=(tk.W, tk.E))
        
        self.result_label = tk.Label(self, text="Result:")
        self.result_label.grid(pady=10)


        self.result_label = tk.Label(self, text="Tooth Thickness :").grid()

        self.result_value = tk.StringVar()
        self.result_entry = tk.Entry(self, textvariable=self.result_value, state='readonly')
        self.result_entry.grid()

        
        
    def calc_span(self):
        try:
            pindia = float(self.num1_entry.get())
            dop = float(self.num2_entry.get())
            
            thickness = self.master.gear.find_thickness(pindia, dop)
            tooth_thickness = f" {thickness:.4f} ({thickness/25.4:.5f})"
            
            self.result_value.set(tooth_thickness)
            
        except ValueError:
            self.result_value.set("Invalid input. Please enter numbers.")






class SimpleCalculator(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.desc = "Addition Calculator"
        self.grid()
        self.create_widgets()

    def create_widgets(self):

        self.result_label = tk.Label(self, text="Add numbers:")
        self.result_label.grid()
        
        self.num1_entry = tk.Entry(self)
        self.num1_entry.grid()

        self.num2_entry = tk.Entry(self)
        self.num2_entry.grid()

        self.calculate_button = tk.Button(self, text="Add", command=self.add_numbers)
        self.calculate_button.grid()

        self.result_label = tk.Label(self, text="Result:")
        self.result_label.grid()

        self.result_value = tk.StringVar()
        self.result_entry = tk.Entry(self, textvariable=self.result_value, state='readonly')
        self.result_entry.grid()

    def add_numbers(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            result = num1 + num2
            self.result_value.set(result)
        except ValueError:
            self.result_value.set("Invalid input. Please enter numbers.")



class NewSpanForm(ttk.Frame):
    PADDING = 10
    ROW_TITLE = 0
    COLUMN_LABEL = 0
    COLUMN_ENTRY = 1

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.desc = "Span"
        self.grid()

        # Title Label
        tk.Label(self, text="Calculate Span Size:").grid(row=self.ROW_TITLE, column=self.COLUMN_LABEL, pady=self.PADDING)

        # Number 1 Widgets
        self.num1_label = tk.Label(self, text="Tooth Thickness:")
        self.num1_entry = ttk.Entry(self)
        self.num1_label.grid(row=self.ROW_TITLE + 1, column=self.COLUMN_LABEL)
        self.num1_entry.grid(row=self.ROW_TITLE + 1, column=self.COLUMN_ENTRY)

        # Number 2 Widgets
        self.num2_label = tk.Label(self, text="No. of Teeth to Span:")
        self.num2_entry = ttk.Entry(self)
        self.num2_label.grid(row=self.ROW_TITLE + 2, column=self.COLUMN_LABEL)
        self.num2_entry.grid(row=self.ROW_TITLE + 2, column=self.COLUMN_ENTRY)

        # Calculate Button
        self.calculate_button = tk.Button(self, text="Calculate", command=partial(self.calc_span))
        self.calculate_button.grid(row=self.ROW_TITLE + 3, column=self.COLUMN_LABEL, columnspan=2, sticky=(tk.W, tk.E))

        # Result Widgets
        self.result_label = tk.Label(self, text="Result:")
        self.result_label.grid(row=self.ROW_TITLE + 4, column=self.COLUMN_LABEL, pady=self.PADDING)

        # Base Tangent Widgets
        self.base_tangent_label = tk.Label(self, text="Base Tangent :")
        self.base_tangent_label.grid(row=self.ROW_TITLE + 5, column=self.COLUMN_LABEL)
        self.base_tangent_value = tk.StringVar()
        self.base_tangent_entry = ttk.Entry(self, textvariable=self.base_tangent_value, state='readonly')
        self.base_tangent_entry.grid(row=self.ROW_TITLE + 5, column=self.COLUMN_ENTRY)

        # Contact Diameter Widgets
        self.contact_diameter_label = tk.Label(self, text="Contact diameter :")
        self.contact_diameter_label.grid(row=self.ROW_TITLE + 6, column=self.COLUMN_LABEL)
        self.contact_diameter_value = tk.StringVar()
        self.contact_diameter_entry = ttk.Entry(self, textvariable=self.contact_diameter_value, state='readonly')
        self.contact_diameter_entry.grid(row=self.ROW_TITLE + 6, column=self.COLUMN_ENTRY)


    def ignore_value_error(self):
        class Ignore(ValueError):
            pass
        return tk._ignore_exception(Ignore, tk.END)


    def calc_span(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
        except ValueError:
            self.base_tangent_value.set("Invalid input. Please enter numbers.")
            self.contact_diameter_value.set("")
            return

        if self.master.gear.type == "Spur":
            base_tangent, contact_diameter = self.master.gear.find_span_spur(num1, num2)
        elif self.master.gear.type == "Helical":
            base_tangent, contact_diameter = self.master.gear.find_span_spur_hel(num1, num2)

        base_tangent = f" {base_tangent:.4f} ({base_tangent/25.4:.5f})"
        contact_diameter = f"{contact_diameter:.4f} ({contact_diameter/25.4:.5f})"

        self.base_tangent_value.set(base_tangent)
        self.contact_diameter_value.set(contact_diameter)

