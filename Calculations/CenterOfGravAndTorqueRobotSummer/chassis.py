from abstract_robot_info import CartesianCoordinate

class Chassis:
    def __init__(self, mass=2, radius=1.5*2.56*0.01, xg=0.15, yg=0.05, zg=0.14, x1=210, x2=210, x3=70, x4=70, z1=0.025, z2=210, z3=0.025, z4=70, y1=0, y2=0, y3=0, y4=0):
        self.mass = mass
        self.radius = radius
        self.centre_of_mass = CartesianCoordinate(xg, yg, zg)
        self.wheel_front_left = CartesianCoordinate(x1, y1, z1)
        self.wheel_front_right = CartesianCoordinate(x2, y2, z2)
        self.wheel_back_left = CartesianCoordinate(x3, y3, z3)
        self.wheel_back_right = CartesianCoordinate(x4, y4, z4)