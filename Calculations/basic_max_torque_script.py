from math import sin, cos, pi

g = 9.81

# masses of stuff, 1 is base, 2 is middle, 3 is claw
m1 = 0.09981
m2 = 0.06262
m3 = 0.109
mS = 0.026 # mass of stone
mC = 0.038 # mass claw joint
mM = 0.026 + 0.01 # 0.038 # mass middle joint

# lengths
d1 = 0.1875
d2 = 0.1125
d3 = 0.16

torque_claw = 100 * g * (d3/2 * m3 + d3 * mS)
print("claw load = " + str(m3 + mS))
print("Torque wrist (N-cm): " + str(torque_claw))

torque_middle = 100 * g * (d2/2 * m2 + d2 * mC + (d2 + d3/2) * m3 + (d2 + d3) * mS)
print("Elbow load = " + str(m2 + mC + m3 + mS))
print("Torque elbow (N-cm): " + str(torque_middle))

torque_base = 100 * g * (d1/2 * m1 + d1 * mM + (d1 + d2/2) * m2 + (d1 + d2) * mC + (d1 + d2 + d3/2) * m3 + (d1 + d2 + d3) * mS)
print("Shoulder load = " + str(m1 + mM + m2 + mC + m3 + mS))
print("Torque shoulder (N-cm): " + str(torque_base))


# get flat ground
mass = 2.478 # kg
theta = 0
accel = 0.25
rear_wheel_force = mass * (9.81 * sin(theta) + accel)
print("rear_wheel_force, flat ground, 0.25 m/s^2: " + str(rear_wheel_force))

# uphill
theta = 7 * pi / 180
rear_wheel_force_uphill_no_a = mass * (9.81 * sin(theta))
rear_wheel_force_uphill_with_a = mass * (9.81 * sin(theta) + accel)

print("rear_wheel_force, uphill, 0 m/s^2: " + str(rear_wheel_force_uphill_no_a))
print("rear_wheel_force, uphill, 0.25 m/s^2: " + str(rear_wheel_force_uphill_with_a))


""" OK, so calculate tipping"""
# flat ground: f - front, l - left, r - right, g - center of grav
x_f = 237.9
y_f = 0
z_f = 137.25

x_l = 64.85
y_l = 0
z_l = 254.27

x_r = 64.85
y_r = 0
z_r = 38.24

x_g = 119.42
y_g = 79.34
z_g = 144.36

print("Where normal falls, flat: (x, y, z) = (" + str(x_g), str(0), str(z_g) + ")\n")

# slope without accel
x_f_slope = x_f*cos(7 * pi / 180)
y_f_slope = y_f*sin(7 * pi / 180)
z_f_slope = z_f

x_g_slope = x_g * cos(7 * pi / 180)
y_g_slope = y_g*sin(7 * pi / 180)
z_g_slope = z_g
