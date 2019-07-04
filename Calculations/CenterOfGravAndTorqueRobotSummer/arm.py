from abstract_robot_info import PositionVector
from abstract_robot_info import CartesianCoordinate
from math import pi,sqrt

class Link:
    def __init__(self, length, mass, phi, theta, centre_of_mass=None):
        self.length = length
        self.mass = mass
        self.phi = phi
        self.theta = theta

    @property
    def center_of_mass(self):
        return PositionVector(self.length/2, self.theta, self.phi).get_cartesian()

    @property
    def far_end(self):
        return PositionVector(self.length, self.theta, self.phi).get_cartesian()

class PointMass:
    def __init__(self, coord, mass):
        # absolute coordinates
        self.coord = coord
        self.mass = mass


class Arm:
    def __init__(self, x=0, y=0, z=0, theta=0,
                 primary_length=0.2666, primary_mass=0.14199, primary_phi=pi/2,
                 secondary_length=0.1334, secondary_mass=0.07, secondary_phi=pi/2,
                 claw_length=0.159, claw_mass=0.090, claw_phi=pi/2,
                 joint_1_mass=0.38, joint_2_mass=0.38, infinity_stone_mass=0.3,
                 primary_g=None, secondary_g=None, claw_g=None):
        self.base_coord = CartesianCoordinate(x, y, z)
        self.primary_link = Link(primary_length, primary_mass, primary_phi, theta, primary_g)
        self.secondary_link = Link(secondary_length, secondary_mass, secondary_phi, theta, secondary_g)
        self.claw = Link(claw_length, claw_mass, claw_phi, theta, claw_g)

        # primary_coord = CartesianCoordinate.add(self.base_coord, self.primary_link.far_end)
        primary_coord = self.primary_link.far_end
        self.primary_joint = PointMass(primary_coord, joint_1_mass)
        secondary_coord = CartesianCoordinate.add(primary_coord, self.secondary_link.far_end)
        self.secondary_joint = PointMass(secondary_coord, joint_2_mass)
        claw_tip_coord = CartesianCoordinate.add(secondary_coord, self.claw.far_end)
        self.infinity_stone_point = PointMass(claw_tip_coord, infinity_stone_mass)

        self.total_mass = self.primary_link.mass + self.secondary_link.mass \
            + self.claw.mass + self.primary_joint.mass + self.secondary_joint.mass \
            + self.infinity_stone_point.mass

    def get_centre_of_mass_relative(self):
        """ So we take each x coordinate and sum!"""
        moment_sum_x = 0
        moment_sum_y = 0
        moment_sum_z = 0

        # get primary link contribution
        primary_link_coord = self.primary_link.center_of_mass
        moment_sum_x = moment_sum_x + self.primary_link.mass*primary_link_coord.x
        moment_sum_y = moment_sum_y + self.primary_link.mass*primary_link_coord.y
        moment_sum_z = moment_sum_z + self.primary_link.mass*primary_link_coord.z

        # add secondary link contribution
        secondary_link_coord = CartesianCoordinate.add(self.primary_link.far_end, self.secondary_link.center_of_mass)
        moment_sum_x = moment_sum_x + self.secondary_link.mass*secondary_link_coord.x
        moment_sum_y = moment_sum_y + self.secondary_link.mass*secondary_link_coord.y
        moment_sum_z = moment_sum_z + self.secondary_link.mass*secondary_link_coord.z

        secondary_link_end = CartesianCoordinate.add(self.primary_link.far_end, self.secondary_link.far_end)

        # add claw
        claw_link_coord = CartesianCoordinate.add(secondary_link_end, self.claw.center_of_mass)
        moment_sum_x = moment_sum_x + self.claw.mass*claw_link_coord.x
        moment_sum_y = moment_sum_y + self.claw.mass*claw_link_coord.y
        moment_sum_z = moment_sum_z + self.claw.mass*claw_link_coord.z

        # add primary joint mass
        moment_sum_x = moment_sum_x + self.primary_joint.mass * self.primary_joint.coord.x
        moment_sum_y = moment_sum_y + self.primary_joint.mass * self.primary_joint.coord.y
        moment_sum_z = moment_sum_z + self.primary_joint.mass * self.primary_joint.coord.z

        # add secondary joint mass
        moment_sum_x = moment_sum_x + self.secondary_joint.mass * self.secondary_joint.coord.x
        moment_sum_y = moment_sum_y + self.secondary_joint.mass * self.secondary_joint.coord.y
        moment_sum_z = moment_sum_z + self.secondary_joint.mass * self.secondary_joint.coord.z

        # add infinity stone mass
        moment_sum_x = moment_sum_x + self.infinity_stone_point.mass * self.infinity_stone_point.coord.x
        moment_sum_y = moment_sum_y + self.infinity_stone_point.mass * self.infinity_stone_point.coord.y
        moment_sum_z = moment_sum_z + self.infinity_stone_point.mass * self.infinity_stone_point.coord.z

        return CartesianCoordinate(moment_sum_x/self.total_mass,
                                   moment_sum_y/self.total_mass, moment_sum_z/self.total_mass)

    def get_centre_of_mass_absolute(self):
        return CartesianCoordinate.sum(self.get_centre_of_mass_absolute(), self.base_coord)

    def get_torque_joint_2(self):
        # add secondary link contribution
        secondary_link_coord = self.secondary_link.center_of_mass
        moment_sum_x = self.secondary_link.mass * secondary_link_coord.x
        moment_sum_y = self.secondary_link.mass * secondary_link_coord.y
        moment_sum_z = self.secondary_link.mass * secondary_link_coord.z

        # add claw
        claw_link_coord = CartesianCoordinate.add(self.secondary_link.far_end, self.claw.center_of_mass)
        moment_sum_x = moment_sum_x + self.claw.mass * claw_link_coord.x
        moment_sum_y = moment_sum_y + self.claw.mass * claw_link_coord.y
        moment_sum_z = moment_sum_z + self.claw.mass * claw_link_coord.z

        # add secondary joint mass
        moment_sum_x = moment_sum_x + self.secondary_joint.mass * self.secondary_joint.coord.x
        moment_sum_y = moment_sum_y + self.secondary_joint.mass * self.secondary_joint.coord.y
        moment_sum_z = moment_sum_z + self.secondary_joint.mass * self.secondary_joint.coord.z

        # add infinity stone mass
        moment_sum_x = moment_sum_x + self.infinity_stone_point.mass * self.infinity_stone_point.coord.x
        moment_sum_y = moment_sum_y + self.infinity_stone_point.mass * self.infinity_stone_point.coord.y
        moment_sum_z = moment_sum_z + self.infinity_stone_point.mass * self.infinity_stone_point.coord.z

        mass = self.total_mass - self.primary_joint.mass + self.primary_link.mass
        x = moment_sum_x / mass
        y = moment_sum_y / mass
        return sqrt(x*x + y*y) * mass



    def change_theta(self, new_theta):
        self.primary_link.theta = new_theta
        self.secondary_link.theta = new_theta
        self.claw.theta = new_theta

        primary_coord = CartesianCoordinate.add(self.base_coord, self.primary_link.far_end)
        self.primary_joint = PointMass(primary_coord, self.primary_joint.mass)
        secondary_coord = CartesianCoordinate.add(primary_coord, self.secondary_link.far_end)
        self.secondary_joint = PointMass(secondary_coord, self.secondary_joint.mass)
        claw_tip_coord = CartesianCoordinate.add(secondary_coord, self.claw.far_end)
        self.infinity_stone_point = PointMass(claw_tip_coord, self.infinity_stone_point.mass)
