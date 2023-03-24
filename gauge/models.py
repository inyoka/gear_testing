import os
import math

from gauge.convert import *

from gauge.repr_lib import spurText, helicalText

class Gear(object):
    """
    Constructs a gear object by taking in 'helix_angle, teeth, module_n, pressure_angle'.
    Using a helix angle of zero produces a Spur, otherwise a Helix is produced.
    """

    def __init__(self, helix_angle, teeth, module_n, pressure_angle):
        """
        Creates initial Gear, always works in metric and radians internally.
        Enter 'Helix Angle' of zero for Spur gear.
        """

        # Base Inputs
        self.ha = self.helix_angle = helix_angle
        self.teeth = int(teeth)
        self.modn = self.module_n = module_n
        self.type = 'Spur' if self.helix_angle == 0 else 'Helical'
        self.pa = self.pan = self.pressure_angle = math.radians(pressure_angle)

        self.cpn = self.circle_pitch_n = math.pi * self.module_n
        self.cpt = self.circle_pitch_t = self.circle_pitch_n / math.cos(self.helix_angle)

        self.modt = self.module_t = self.circle_pitch_t / math.pi 
        self.pat = self.pressure_angle_t = math.atan(math.tan(self.pressure_angle) / math.cos(self.helix_angle)) 

        self.pcd = self.teeth * self.module_n / math.cos(self.helix_angle) 
        self.bcd = self.pcd * math.cos(self.pressure_angle_t)

        self.type = 'Spur' if self.helix_angle == 0 else 'Helical'

        """  Alternative Calculation methods ...
        # self.module_t = self.teeth / math.cos(math.degrees(self.helix_angle))
        # self.pcd = self.circle_pitch_t * self.teeth / math.pi 
        """

        if self.helix_angle :
            self.lead = math.pi * self.pcd / math.tan(self.helix_angle) 
            self.bha = self.base_helix_angle = math.atan(math.pi * self.bcd / self.lead)
        else :
            self.helix_angle = 0
            self.lead = False
            self.bha = 0


    @classmethod
    def make_spur(cls, teeth, module_n, pressure_angle):
        """
        Make spur gear programatically, provides a default Helix of zero.
        User calls function with no of teeth, module size and pressure angle.
        Example :  my_gear = Gear.make_spur(50, 1, 17)
        """
        return cls(0, teeth, module_n, pressure_angle)
    

    def display(self):
        """
        Displays a generated gear on the command line along with all 'automatically' 
        generated data.  Example : my_gear.display()
        """

        width, height = os.get_terminal_size()
        print(f"{'_' * width}")
        print(f"Helix Angle         {math.degrees(self.helix_angle):<10.4}   {rad_to_dms(self.helix_angle)}")
        print(f"Teeth               {self.teeth:<10}")
        print(f"DPn                 {round(inches(self.module_n), 5):<10.4}")
        print(f"DPt                 {round(inches(self.module_t), 5):<10.4}")
        print(f"MODn                {float(self.module_n):<10.4}")
        print(f"MODt                {round(self.module_t, 5):<10.4}") 
        print(f"PAn                 {round(math.degrees(self.pressure_angle), 5):<10.5}")
        print(f"PAt                 {round(math.degrees(self.pressure_angle_t), 5):<10.5}\n")
        print(f"PCD                 {mm(self.pcd):<10} ({self.pcd:10.5})")
        print(f"BCD                 {mm(self.bcd):<10.5} ({self.bcd:10.5})")


        half = int(width / 3)
        print(f"{'^' * half}")

    
    def __repr__(self):
        """
        Required code that reproduces object, Generate output for developer
        """
        return f"REPR : Gear('{self.type}\n', '{self.helix_angle}', '{self.teeth}\n', '{self.modn}', '{self.pressure_angle}')"


    def __str__(self):
        """
        Make object readable, Generate output to end user
        """
        if self.type == 'Spur' :
            return spurText(self)
        elif self.type == 'Helical' :
            return helicalText(self)

    def add(self, num1, num2):
        return num1 + num2
