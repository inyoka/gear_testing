import math

def spurText(self) -> str:
    """Return the text representation of the object."""
    return f"""
Gear Type           \t\t: {self.type} Gear
Num of Teeth          \t: {self.teeth}
Tooth size          \t\t: {self.module_n}
Pressure Angle (Rads) \t: {math.degrees(self.pressure_angle)} 
Pressure Angle (Degs) \t: {math.degrees(self.pa)}
PCD                 \t\t: {self.pcd}
BCD                 \t\t: {self.bcd}
        """

def helicalText(self) -> str:
    """Return the text representation of the object."""
    return f"""
Gear Type           \t\t: {self.type} Gear
Num of Teeth          \t: {self.teeth}
Tooth size          \t\t: {self.module_n}
Pressure Angle (Rads) \t: {math.degrees(self.pressure_angle)} 
Pressure Angle (Degs) \t: {math.degrees(self.pa)}
PCD                 \t\t: {self.pcd}
BCD                 \t\t: {self.bcd}
Helix Angle (Rads)    \t: {self.helix_angle} 
Helix Angle (Degs)    \t: {math.degrees(self.helix_angle)}
Base HA (Rads)        \t: {self.bha}
Base HA (Degs)        \t: {math.degrees(self.bha)}
        """

def windowLines(self):
    lines = [
        ('Gear Type       :'+self.type+'\n'),
        ('Num of Teeth    :'+self.teeth+'\n'),
        ('Tooth size      :'+self.module_n+'\n'),
    ]
    return lines