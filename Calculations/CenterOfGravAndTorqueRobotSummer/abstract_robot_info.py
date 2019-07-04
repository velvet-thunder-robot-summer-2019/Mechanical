from math import sin, cos
""" Abstract classes to help with robot stuff """


class CartesianCoordinate:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def add(coord, otherCoord):
        x = coord.x + otherCoord.x
        y = coord.y + otherCoord.y
        z = coord.z + otherCoord.z
        return CartesianCoordinate(x, y, z)

    def product(self, scaling_factor):
        self.x = self.x * scaling_factor
        self.y = self.y * scaling_factor
        self.z = self.z * scaling_factor


class PositionVector:
    def __init__(self, length, theta, phi):
        """
        Position vector that converts between cartesian and spherical
        :param length: in meter
        :param phi: in radians
        :param theta: in radians
        """
        self.length = length
        self.theta = theta
        self.phi = phi
        self.coords = self.get_cartesian()


    def set_theta_phi(self, theta, phi):
        self.theta = theta
        self.phi = phi
        self.coords = self.get_cartesian()

    def get_cartesian(self):
        x = self._get_x(self.theta, self.phi)
        y = self._get_y(self.theta, self.phi)
        z = self._get_z(self.theta, self.phi)
        return CartesianCoordinate(x, y, z)

    def _get_x(self, theta, phi):
        return self.length * sin(phi) * cos(theta)

    def _get_y(self, theta, phi):
        return self.length * sin(phi) * sin(theta)

    def _get_z(self, theta, phi):
        return self.length * cos(phi)
