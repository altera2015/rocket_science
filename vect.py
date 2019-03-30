import math
import numpy as np

class Vector:
    
    def __init__(self, other = None):
        if other is None:
            self.pos = [0.0, 0.0, 0.0]
        else:
            self.pos = [
                other[0], other[1], other[2]
            ]


    def __getitem__(self, key):
        return self.pos[key]

    def __setitem__(self, key, value):
        self.pos[key]=value

    def __str__(self):
        return "({},{},{})".format(self.pos[0], self.pos[1], self.pos[2])

    def zero(self):
        self.pos[0] = 0.0
        self.pos[1] = 0.0
        self.pos[2] = 0.0

    @property
    def magnitude(self):
        return np.linalg.norm(self.pos)

    @staticmethod
    def toSpherical( vect ):
        r = np.linalg.norm(vect.pos)
        theta = math.acos( vect[2] / r)
        phi = math.atan2( vect[1], vect[0] )
        return [r,theta, phi]

    @staticmethod
    def toCartesian( vect ):
        x = vect[0] * math.sin( vect[1] ) * math.cos( vect[2] )
        y = vect[0] * math.sin( vect[1] ) * math.sin( vect[2] )
        z = vect[0] * math.cos( vect[2] )
        return [x,y,z]

    def assign( self, other ):
        self[0] = other[0]
        self[1] = other[1]
        self[2] = other[2]
        return self

    def mult( self, factor ):
        self[0] *= factor
        self[1] *= factor
        self[2] *= factor
        return self

    def add( self, other ):
        self[0] += other[0]
        self[1] += other[1]
        self[2] += other[2]
        return self
    
    def __mul__(self, factor):
        n = Vector(self)
        return n.mult(factor)

    def __rmul__(self, factor):
        n = Vector(self)
        return n.mult(factor)

    def __add__(self, other):
        n = Vector(self)
        return n.add(other)
