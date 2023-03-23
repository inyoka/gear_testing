import math
import unittest



def inches(mm):
    return mm * 25.4


def mm(inches):
    return inches / 25.4 

def rads(decimal):
    """
    Convert degrees to radians.
    """
    return math.radians(decimal)


def deg_to_rad(decimal):
    """
    Convert degrees to radians.
    """
    return math.radians(decimal)


def dms_to_deg(degrees, minutes, seconds):
    decimal = degrees + float(minutes)/60 + float(seconds)/3600
    return float(decimal)


def dms_to_rad(dgs, mns, scs):
    return math.radians((dgs + (mns * 60 + scs) / 3600))


def dms_to_rad(degrees, minutes, seconds):
    decimal = dms_to_deg(degrees, minutes, seconds)
    return math.radians(decimal)


def rad_to_deg(radians):
    return math.degrees(radians)


def rad_to_dms(radians):
    degrees = radians * 180 / math.pi
    minutes, seconds = divmod(degrees * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    return int(degrees), int(minutes), int(seconds)


def deg_to_dms(decimal_value):
    pos_or_neg = -1 if decimal_value < 0 else 1
    minutes, seconds = divmod(abs(decimal_value)*3600, 60)
    degrees, minutes = divmod(minutes, 60)
    return int(pos_or_neg*degrees), int(pos_or_neg*minutes), int(pos_or_neg*seconds)


def deg_to_dms(decimal_value):
    pos_or_neg = -1 if decimal_value < 0 else 1
    minutes, seconds = divmod(abs(decimal_value)*3600, 60)
    degrees, minutes = divmod(minutes, 60)
    return int(pos_or_neg*degrees), int(pos_or_neg*minutes), int(pos_or_neg*seconds)

def dms_to_dec(degrees, minutes, seconds):
    decimal = degrees + float(minutes)/60 + float(seconds)/3600
    return float(decimal)


class TestConvert(unittest.TestCase):
    def test_invinv(self):
        self.assertAlmostEqual(invinv(0.0), None, places=7)
        self.assertAlmostEqual(invinv(0.00001), 1.7921333769215897, places=7)
        self.assertAlmostEqual(invinv(0.0002), 4.827933730313794, places=7)
        self.assertAlmostEqual(invinv(0.08109), 33.99917243213663, places=7)
        self.assertAlmostEqual(invinv(0.09822), 35.999566116792636, places=7)
        self.assertAlmostEqual(invinv(0.68485), 59.99993780771472, places=7)
        self.assertAlmostEqual(invinv(0.68486), 60.00012879313373, places=7)

    def test_invol(self):
        self.assertEqual(invol(0), "Error 0 is outside of 0-60")
        self.assertAlmostEqual(invol(15), 0.006149804631973288, places=7)
        self.assertAlmostEqual(invol(25), 0.0299753451564162, places=7)
        self.assertAlmostEqual(invol(30), 0.053751493591326915, places=7)
        self.assertAlmostEqual(invol(35), 0.08934230001169441, places=7)
        self.assertAlmostEqual(invol(45), 0.2146018366025516, places=7)
        self.assertAlmostEqual(invol(36.20), 0.10008, places=4)
        self.assertEqual(invol(60), "Error 60 is outside of 0-60")

    def test_iterate_v2(self):
        self.assertAlmostEqual(iterate_v2(0), 0.0169, places=2)
        self.assertAlmostEqual(iterate_v2(0.001), 0.1438, places=2)
        self.assertAlmostEqual(iterate_v2(15), 1.510, places=2)
        self.assertAlmostEqual(iterate_v2(60), 1.55455, places=2)
        self.assertAlmostEqual(iterate_v2(90), 1.5598, places=2)


if __name__ == "__main__":
    unittest.main()