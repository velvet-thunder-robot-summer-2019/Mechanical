from math import cos, sin
import collections


class Wheel:
    def __init__(self, x, y, z):
        """

        :param x1: x position of wheel 1
        :param x2: x position of wheel 2
        :param y: y position of wheels (assumed to be along this axis)
        """
        self.x = x
        self.y = y
        self.z = z

class RobotBasicModel:
    def __init__(self, center_of_gravity, back_wheels, front_wheels):
        self.center_of_gravity = center_of_gravity
        self.back_wheels = back_wheels # list, first is left, second is right
        self.front_wheels = front_wheels

    def moment_front_wheels(self):
        """ Gravity is in the y direction, axis between wheels z direction
            Therefore the moment is in the z direction
            Positive number if center of gravity x is smaller than wheel x
            Tips if returns a negative number
         """
        x_diff = self.front_wheels[0].x - self.center_of_gravity.coordinate.x
        return self.center_of_gravity.mass*x_diff

    def moment_back_wheels(self):
        """ Tips if returns is positive"""
        x_diff = self.back_wheels[0].x - self.center_of_gravity.coordinate.x
        return self.center_of_gravity.mass*x_diff

    def moment_left(self):
        """ Tips if negative number returned """
        z_diff = self.center_of_gravity.coordinate.z - self.front_wheels[0].z
        return self.center_of_gravity.mass*z_diff

    def moment_right(self):
        """ Tips if negative number returned"""
        z_diff = self.center_of_gravity.coordinate.z - self.front_wheels[1].z
        return self.center_of_gravity.mass*z_diff

    def check_against_tipping(self):
        moment_back = self.moment_back_wheels()
        assert moment_back < 0, "moment back was: " + str(moment_back)
        moment_forward = self.moment_front_wheels()
        assert moment_forward > 0, "moment forward was: " + str(moment_forward)
        moment_left = self.moment_left()
        assert moment_left > 0, "moment left was: " + str(moment_left)
        moment_right = self.moment_right()
        assert moment_right < 0, "moment right was: " + str(moment_right)


front_wheels = [Wheel(149.92, 156.57, 100.2), Wheel(149.42, 156.57, 340.37)]
back_wheels = [Wheel(9.72, 156.57, 100.2), Wheel(9.72, 156.57, 340.37)]


Coordinate = collections.namedtuple('Coordinate', 'x y z')
CenterOfGrav = collections.namedtuple('CenterOfGrav', 'mass coordinate')
coord = Coordinate(x=114.04, y=168.7, z=218.24)
center_of_gravity = CenterOfGrav(mass=13885.76, coordinate=coord)
robot = RobotBasicModel(center_of_gravity, back_wheels, front_wheels)
robot.check_against_tipping()











class Chassis:
    def __init__(self, x, y, z):
        """
        Software representation of our chassis
        :param x: x coordinate of centre of gravity
        :param y: y coordinate of centre of gravity
        :param z: z coordinate of centre of gravity
        """
        self.x_bar = x
        self.y_bar = y
        self.z_bar = z


class Arm:

    def __init__(self, x, y, z, theta, base_weight, weight_1_joint, weight_2_joint, weight_claw_tip, length_arm_1, arm_1_weight, phi_arm_1, length_arm_2, arm_2_weight, phi_arm_2, length_claw, claw_weight, phi_claw):
        """

        :param x:
        :param y:
        :param z:
        :param w_base1:
        :param w_base_2:
        :param w_base_3:
        :param l_arm1:
        :param w_arm1:
        :param angle_arm1:
        :param l_arm2:
        :param w_arm2:
        :param angle_arm2:
        :param l_claw:
        :param w_claw:
        :param angle_claw:
        """

        self.Coordinate = collections.namedtuple('Coordinate', 'x y z')
        self.CenterOfGrav = collections.namedtuple('CenterOfGrav', 'mass coordinate')

        self.x_base = x
        self.y_base = y
        self.z_base = z

        self.length_arm_1 = length_arm_1
        self.length_arm_2 = length_arm_2
        self.length_claw = length_claw

        self.base_weight = base_weight
        self.joint_1_weight = weight_1_joint
        self.joint_2_weight = weight_2_joint
        self.weight_claw_tip = weight_claw_tip

        self.arm_1_weight = arm_1_weight
        self.arm_2_weight = arm_2_weight
        self.claw_weight = claw_weight

        self.joint_1 = None
        self.joint_2 = None
        self.claw_tip = None

        self.update_coordinates(theta, phi_arm_1, phi_arm_2, phi_claw)


    def get_centre_of_gravity(self):
        pass

    def update_coordinates(self, theta, phi_arm_1, phi_arm_2, phi_claw):
        self.base = self.Coordinate(x=x, y=y, z=z)

        tmp_x = self.x + self.length_arm_1*sin(phi_arm_1)*cos(theta)
        tmp_y = self.y + self.length_arm_1*sin(phi_arm_1)*sin(theta)
        tmp_z = self.z + self.length_arm_1*cos(phi_arm_1)
        self.joint_1 = self.Coordinate(x=tmp_x, y=tmp_y, z=tmp_z)

        tmp_x = self.joint_1.x + self.length_arm_2*sin(phi_arm_2)*cos(theta)
        tmp_y = self.joint_1.y + self.length_arm_2*sin(phi_arm_2)*sin(theta)
        tmp_z = self.joint_1.z + self.length_arm_2cos(phi_arm_2)



class RobotPhysicalModel:

    def __init__(self,chassis, arm, x_wheel1, x_wheel2, ):
        """ Current assumption is that the arms have uniform density throughout, center of grav is at middle """
        self.chassis = chassis
