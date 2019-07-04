from chassis import Chassis
from arm import Arm
from robot import Robot
from math import pi

def get_robot_1():
    chassis = Chassis(mass=3.333, radius=1.5*2.56*0.01, xg=0.150, yg=0.053, zg=0.139,
                      x1=0.20955, z1=0.1953, x2=0.20955, z2=0.260, x3=0.06985, z3=0.01953, x4=0.06985, z4=260)
    arm = Arm(x=0.14354, y=0.13172, z=0.13833, theta=0)
    return Robot(arm, chassis)


def output_torques():
    robot_1 = get_robot_1()
    # chassis_mass = 2
    # arm_mass = 0.96
    #mass = chassis_mass + arm_mass
    mass = 3
    print("Force needed on flat ground, accel = 1 m/s^2: " + str(robot_1.get_rear_wheel_force_needed(acceleration=1, mass=mass, theta=0)) + " N")
    angle = 7 * pi / 180
    print("Force on 7 degree incline, no accel: " + str(robot_1.get_rear_wheel_force_needed(acceleration=0, mass=mass, theta=angle)) + " N")
    print("Force on 7 degree incline, accel = 0.5 m/s^2: " + str(robot_1.get_rear_wheel_force_needed(acceleration=0.5, mass=mass, theta=angle)) + " N")

def claw_torque():
    robot = get_robot_1()
    print("Max torque on claw (rotation): " + str(robot.get_torque_base_claw() * 100) + " N-cm")
    print("Max torque on claw middle join: " + str(robot.get_torque_joint_2() * 100) + " N-cm")
    print("Max torque on base of arm: " + str(robot.get_torque_joint_1() * 100) + " N-cm")

def main():
    output_torques()
    # claw_torque()

if __name__=='__main__':
    main()