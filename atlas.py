import rocket
import stage
import math
import unittest


# Details from:
# https://en.wikipedia.org/wiki/Atlas_V

class AtlasVFirstStage401(stage.Stage):

    def __init__(self):
        super().__init__(21054, 284089, 253, 3827.0e3, 3.81, True, "Atlas V 401 First Stage")
        # RD-180
        # https://en.wikipedia.org/wiki/RD-180
        #self._ispVac = 337.8
        #self._exit_area = ( 1.445 / 2.0 ) ** 2 * math.pi

class AtlasVCentaur(stage.Stage):

    def __init__(self):
        super().__init__(2316, 20830, 842, 99.2e3, 3.05, True, "Atlas V Centaur Upper Stage")
        # RL10A-4-2
        # https://en.wikipedia.org/wiki/RL10
        #self._ispVac = 450.5
        #self._exit_area = ( 2.21 / 2.0 ) ** 2 * math.pi


class AtlasVPayload42(stage.Stage):

    def __init__(self, mass):
        super().__init__(mass, 0, 0, 0, 4.2, False, "4.2 Meter Fairing Payload")

class AtlasVPayload54(stage.Stage):

    def __init__(self, mass):   
        super().__init__(mass, 0, 0, 0, 5.4, False, "5.4 Meter Fairing Payload")



# http://www.spacelaunchreport.com/atlas5.html
# 401 can do 8.9e3kg to LEO @ 407km 51.6 deg

class AtlasV401(rocket.Rocket):

    def __init__(self, payload_mass, position, orientation=None):

        stages = [
            AtlasVFirstStage401(),
            AtlasVCentaur(),
            AtlasVPayload42(payload_mass)
        ]

        # max force is 10 Mega Newton. Guestimate.
        # engines do 3MN at SL and 4MN in VAC.
        super().__init__(stages, 10.0e6, position, orientation)




class AtlastUnitTest(unittest.TestCase):


    def test_force_rd180(self):

        rd180 = AtlasVFirstStage401()
        rd180.throttle = 1.0
        F = rd180.thrust(1e5)
        print(F)
        self.assertTrue( F >= 3830  and F < 4150 )