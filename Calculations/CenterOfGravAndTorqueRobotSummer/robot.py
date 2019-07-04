from arm import Arm
from chassis import Chassis
from abstract_robot_info import CartesianCoordinate
from math import pi, sin, cos, sqrt

class Robot:
    g = 9.81

    def __init__(self, arm, chassis, angle=0):
        self.arm = arm
        self.chassis = chassis
        self.angle = angle
        self.mass = arm.total_mass + chassis.mass

    def centre_of_mass(self):
        # add moment from arm
        x_moment = self.arm.get_centre_of_mass_absolute().x * self.arm.total_mass
        y_moment = self.arm.get_centre_of_mass_absolute().y * self.arm.total_mass
        z_moment = self.arm.get_centre_of_mass_absolute().z * self.arm.total_mass
        # add moment from chassis
        x_moment = x_moment + self.chassis.centre_of_mass.x * self.chassis.mass
        y_moment = y_moment + self.chassis.centre_of_mass.y * self.chassis.mass
        z_moment = z_moment + self.chassis.centre_of_mass.z * self.chassis.mass

        return CartesianCoordinate(x_moment/self.mass, y_moment/self.mass, z_moment/self.mass)

    def check_for_tipping(self):
        mg_vector = CartesianCoordinate(cos(pi/2 - self.angle), sin(pi/2 - self.angle), 0)
        vector_length = self.centre_of_mass().y / mg_vector.y
        mg_vector.product(vector_length)

        ground_intersect = CartesianCoordinate(self.centre_of_mass(), mg_vector)
        return self._intersect_between_wheels(ground_intersect)

    def get_rear_wheel_force_needed(self, acceleration=0, mass=None, theta=None):
        if not mass:
            mass = self.mass
        if not theta:
            theta = self.angle
        F = mass*(9.81*sin(theta) +  acceleration)
        return F

    def get_torque_base_claw(self):
        # torque from claw
        x = self.arm.claw.center_of_mass.x
        z = self.arm.claw.center_of_mass.z
        horizontal_lever = sqrt(x*x + z*z)
        torque = horizontal_lever * self.arm.claw.mass * Robot.g

        # torque from infinity stone
        x = self.arm.claw.far_end.x
        z = self.arm.claw.far_end.z
        horizontal_lever = sqrt(x*x + z*z)
        return torque + horizontal_lever * self.arm.infinity_stone_point.mass * Robot.g

    def get_torque_joint_1(self):
        coord = self.arm.get_centre_of_mass_relative()
        horizontal_lever = sqrt(coord.x * coord.x + coord.y * coord.y)
        return horizontal_lever * self.arm.total_mass * Robot.g

    def get_torque_joint_2(self):
        return self.arm.get_torque_joint_2()

    def _intersect_between_wheels(self, coord):
       return self.chassis.wheel_back_left.x < coord.x < self.chassis.wheel_front_left.x \
              and self.chassis.wheel_front_left.z < coord.z < self.chassis.wheel_front_right.z