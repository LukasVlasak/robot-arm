# pocitam cca 6cm na joint, COM ve stredu
JOINT_L = 0.06



# pocitam s tim ze mam kruhovy prurez 35mm vnejsi a 25mm vnitrni a PALG v kg
LINK1_W = 0.485
LINK2_W = 0.173
LINK3_W = 0.093

# pocitam s nasi docasnou kinematikou v m
# COM ve stredu
LINK1_L = 0.3
LINK2_L = 0.28
LINK3_L = 0.16 # vlastne zbytecne ale nechavam

# vzdalenost link COM od osy otaceni
LINK1_R = (LINK1_L / 2) + JOINT_L
LINK2_R = JOINT_L + LINK1_L + JOINT_L + (LINK2_L / 2)
LINK3_R = JOINT_L + LINK1_L + JOINT_L + LINK2_L + JOINT_L



# vzdalenost motor COM od osy otaceni
MOTOR1_R = JOINT_L + LINK1_L + JOINT_L
MOTOR2_R = JOINT_L + LINK1_L + JOINT_L + LINK2_L + JOINT_L
MOTOR3_R = MOTOR2_R # pokud se motor 3 otáčí kolem vodorovné osy (například osy Y) a gravitace působí dolů ve směru Z, tak pro výpočet gravitačního torque potřebuješ pouze vodorovnou vzdálenost těžiště od osy motoru.
END_EFFECTOR_R = MOTOR2_R

# https://robotis.us/products/dynamixel-xm430-w350-t?srsltid=AU7gw4WdXu83MEWZ_S2w-UYNEthsW0pRe4yIigRo7nuGApWx5hD06XKj&dxl1=XM430-W350-T&dxl2=XM430-W210-R
MOTOR_W = 0.082


# 30g + jointy cca 20g na kazdy - joint u endeeffectoru, takze treba 45g => 75g
END_EFFECTOR_W = 0.03
JOINT_W = 0.02


JOINT0_R = JOINT_L / 2 # primo u motoru
JOINT1_R = MOTOR1_R - (JOINT_L / 2)
JOINT2_R = MOTOR2_R - (JOINT_L / 2)
JOINT3_R = MOTOR3_R - (JOINT_L / 2)


# R linku
R_LINK = LINK1_R * LINK1_W + LINK2_R * LINK2_W + LINK3_R * LINK3_W 
# R motoru
R_MOTOR = MOTOR1_R * MOTOR_W + MOTOR2_R * MOTOR_W + MOTOR3_R * MOTOR_W
# R jointu
R_JOINT = JOINT0_R * JOINT_W + JOINT1_R * JOINT_W + JOINT2_R * JOINT_W + JOINT3_R * JOINT_W + END_EFFECTOR_R * END_EFFECTOR_W
# celkova hmostnost
M = END_EFFECTOR_W + 4 * JOINT_W + 3 * MOTOR_W + LINK1_W + LINK2_W + LINK3_W

# COM celeho
Xcom = (R_LINK + R_MOTOR + R_JOINT) / M

print("Xcom: " + str(Xcom))


# Torque, T = F * sin(omega) * r
# r .... Xcom
# F .... m * g => M * 9.81
# omega .... 90 stupnu => sin(omega) = 1 (gravitace pusobi kolmo)
T = M * 9.81 * Xcom

print("Torque needed: " + str(T) + "Nm\n")
print("Stall torque mensiho motor: 4.1Nm\n")
print("Stall torque vetsiho motor: 7.3Nm\n")
