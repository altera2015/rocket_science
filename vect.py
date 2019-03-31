import math
import numpy as np
import unittest

"""
Vector class. Handles all your 3d calculations
"""
class Vector:

    """
    constructor creates a deep copy of the other parameter
    """
    def __init__(self, other = None):
        
        self._magnitude = None
        if other is None:
            self._pos = [0.0, 0.0, 0.0]
        else:
            self._pos = [
                other[0], other[1], other[2]
            ]

    def __getitem__(self, key):
        return self._pos[key]

    def __setitem__(self, key, value):
        self._magnitude = None
        self._pos[key]=value

    def __str__(self):
        return "({},{},{})".format(self._pos[0], self._pos[1], self._pos[2])

    """
    Zero out all elements.
    """
    def zero(self):
        self._magnitude = 0.0
        self._pos[0] = 0.0
        self._pos[1] = 0.0
        self._pos[2] = 0.0

    """
    Calculates the Euclidean norm
    """
    @property
    def magnitude(self):
        #if self._magnitude == None:
        self._magnitude = np.linalg.norm(self._pos)
        return self._magnitude

    """
    Calculate Theta in ISO system
    (Inclination)
    https://en.wikipedia.org/wiki/Spherical_coordinate_system#/media/File:3D_Spherical.svg
    """
    @property
    def theta(self):
        return math.acos( self._pos[2] / self.magnitude )

    """
    Calculate Theta in ISO system
    (Azimuth)
    https://en.wikipedia.org/wiki/Spherical_coordinate_system#/media/File:3D_Spherical.svg
    """
    @property
    def phi(self):
        return math.atan2( self._pos[1], self._pos[0] )

    """
    Converts the Cartesian coordinates to spherical system
    """
    @staticmethod
    def toSpherical( vect ):
        r = np.linalg.norm(vect._pos)
        theta = math.acos( vect[2] / r)
        phi = math.atan2( vect[1], vect[0] )
        return [r,theta, phi]

    """
    Converts the coordinates from spherical to Cartesian
    """
    @staticmethod
    def toCartesian( vect ):
        x = vect[0] * math.sin( vect[1] ) * math.cos( vect[2] )
        y = vect[0] * math.sin( vect[1] ) * math.sin( vect[2] )
        z = vect[0] * math.cos( vect[2] )
        return [x,y,z]

    """
    Copy of the parametes
    """
    def assign( self, other ):
        self._magnitude = None
        self[0] = other[0]
        self[1] = other[1]
        self[2] = other[2]
        return self
    
    """
    Multiply the vector with a float
    """
    def mult( self, factor ):
        self._magnitude = None
        self[0] *= factor
        self[1] *= factor
        self[2] *= factor
        return self

    """
    Add another vector to self
    """
    def add( self, other ):
        self._magnitude = None
        self[0] += other[0]
        self[1] += other[1]
        self[2] += other[2]
        return self

    """
    Subtract another vector from self
    """
    def sub( self, other):
        self._magnitude = None
        self[0] -= other[0]
        self[1] -= other[1]
        self[2] -= other[2]
        return self

    """
    Create a deepcopy of the vector
    """
    def deepcopy(self):
        return Vector(self)

    """
    Normalize the vector to length (magnitude) 1
    """
    def normalize(self):        
        self.mult( 1.0 / self.magnitude )
        self._magnitude = 1.0
        return self

    """
    Rotate the vector around axis for angle radians
    """
    def rotate(self, angle, axis):
        self._magnitude = None
        axis.normalize()

        q0 = math.cos(angle/2.0) 
        q1 = math.sin(angle/2.0) * axis[0]
        q2 = math.sin(angle/2.0) * axis[1]
        q3 = math.sin(angle/2.0) * axis[2]

        Q = np.zeros((3,3))

        q02 = q0**2
        q12 = q1**2
        q22 = q2**2
        q32 = q3**2

        Q[0,0] = q02 + q12 - q22 - q32
        Q[1,1] = q02 - q12 + q22 - q32
        Q[2,2] = q02 - q12 - q22 + q32
        
        Q[0,1] = 2.0 * ( q1*q2 - q0*q3 )
        Q[0,2] = 2.0 * ( q1*q3 + q0*q2 )

        Q[1,0] = 2.0 * ( q1*q2 + q0*q3 )
        Q[1,2] = 2.0 * ( q2*q3 - q0*q1 )

        Q[2,0] = 2.0 * ( q1*q3 - q0*q2 )
        Q[2,1] = 2.0 * ( q2*q3 + q0*q1 )

        u = np.array(self._pos)

        u2 = Q.dot( u )

        self._pos[0] = u2[0]
        self._pos[1] = u2[1]
        self._pos[2] = u2[2]

        return self

    """
    Calculate cross product. Creates a new vector without modifying current.
    """    
    def cross(self, other):
        return Vector([
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0]
        ])

    def __mul__(self, factor):
        n = Vector(self)
        return n.mult(factor)

    def __rmul__(self, factor):
        n = Vector(self)
        return n.mult(factor)

    def __add__(self, other):
        n = Vector(self)
        return n.add(other)

    def __radd__(self, other):
        n = Vector(other)
        return n.add(self)

    def __sub__(self, other):
        n = Vector(self)
        return n.sub(other)

    def __rsub__(self, other):
        n = Vector(other)
        return n.sub(self)

    def __eq__(self, other):
        if isinstance(other, Vector):
            return np.all( np.isclose(self._pos, other._pos) )
        else:
            return np.all(np.isclose(self._pos, other))

        

class VectorUnitTest(unittest.TestCase):

    def test_equals(self):
        a = Vector([1.1, 1.2, 1.3])
        b = Vector([11.0, 12.0, 13.0])
        b.mult(0.1)
        self.assertTrue( a == b )

    def test_assign(self):
        a = Vector([1.0, 2.0, 3.0])        
        b = Vector()
        b.assign(a)
        self.assertTrue( a == b )
        c = b
        d = b.deepcopy()
        b.mult(2.0)
        self.assertFalse( a == b )
        self.assertFalse( a == c )
        self.assertTrue( a == d )

    def test_add(self):
        a = Vector([1.1, 1.2, 1.3])
        b = Vector([2.0, 3.0, 4.0])
        c = Vector([3.1, 4.2, 5.3])
        d = a + b
        self.assertTrue( d == c )
        self.assertTrue( a == Vector([1.1, 1.2, 1.3]) )
        self.assertTrue( b == Vector([2.0, 3.0, 4.0]) )

    def test_sub(self):
        a = Vector([1.1, 1.2, 1.3])
        b = Vector([2.0, 3.0, 4.0])
        c = Vector([-0.9, -1.8, -2.7])
        d = a - b
        self.assertTrue( d == c )
        self.assertTrue( a == Vector([1.1, 1.2, 1.3]) )
        self.assertTrue( b == Vector([2.0, 3.0, 4.0]) )


    def test_mult(self):
        a = Vector([1.1, 1.2, 1.3])        
        b = Vector([2.2, 2.4, 2.6])
        c = a * 2.0
        self.assertTrue( b == c )
        self.assertTrue( a == Vector([1.1, 1.2, 1.3]) )
        c = 2.0 * a
        self.assertTrue( b == c )

    def test_magnitude(self):
        a = Vector([1.0, 2.0, 3.0])        
        self.assertTrue( a.magnitude == math.sqrt(14.0) )
        a = a * 2.0
        self.assertTrue( a.magnitude == math.sqrt(56.0) )

    def test_rotate1(self):

        axis = Vector([0.0,0.0,1.0])
        a = Vector([1.0,0.0,0.0])
        b = Vector([0.0,1.0,0.0])

        a.rotate( 90 * math.pi / 180.0, axis)
        self.assertTrue(a==b)

    def test_rotate2(self):

        axis = Vector([0.0,0.0,1.0])
        a = Vector([1.0,0.0,0.0])
        b = Vector([0.0,-1.0,0.0])

        a.rotate( -90 * math.pi / 180.0, axis)
        self.assertTrue(a==b)


    def test_rotate3(self):

        axis = Vector([0.0,1.0,0.0])
        a = Vector([1.0,0.0,0.0])
        b = Vector([0.0,0.0,-1.0])

        a.rotate( 90 * math.pi / 180.0, axis)
        self.assertTrue(a==b)

    def test_rotate4(self):

        axis = Vector([1.0,0.0,0.0])
        a = Vector([0.0,1.0,0.0])
        b = Vector([0.0,0.0,1.0])

        a.rotate( 90 * math.pi / 180.0, axis)
        self.assertTrue(a==b)

    def test_rotate5(self):

        axis = Vector([1.0,1.0,1.0])
        a = Vector([1.0,0.0,0.0])
        b = Vector([0.33333333333333337,0.9106836025229592,-0.24401693585629242])        
        a.rotate( 90 * math.pi / 180.0, axis)        
        self.assertTrue(a==b)

    def test_perpendicular1(self):
        
        a = Vector([1.0,0.0,0.0])
        b = Vector([0.0,1.0,0.0])
        c = Vector([0.0,0.0,1.0])
        d = a.cross(b)
        self.assertTrue(c == d)


    def test_perpendicular2(self):
        
        a = Vector([0.0,0.0,1.0])
        b = Vector([0.0,1.0,0.0])
        c = Vector([-1.0,0.0,0.0])
        d = a.cross(b)
        self.assertTrue(c == d)



if __name__ == '__main__':
    unittest.main()