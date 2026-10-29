import math

# Iz = m*r^2 - moment setrvacnosti kolem osy Z -> otaceni robotem doleva doprava
# potrebne zrcyhleni 
# 90stupnu za sekundu => pi/2 a potom brzdi
alpha = math.pi / 2 # m/s^2 


# pocitam cca 6cm na joint, COM ve stredu
JOINT_L = 0.06


# pocitam s tim ze mam kruhovy prurez 35mm vnejsi a 25mm vnitrni a PALG v kg
LINK1_W = 0.175
LINK2_W = 0.164
LINK3_W = 0.093

# vnejsi a vnitrni prumer kruhoveho linku
LINK_R = 0.035 / 2
LINK_r = 0.025 / 2

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


MOTOR_W = 0.082
END_EFFECTOR_W = 0.03
JOINT_W = 0.02

JOINT0_R = JOINT_L / 2 # primo u motoru
JOINT1_R = MOTOR1_R - (JOINT_L / 2)
JOINT2_R = MOTOR2_R - (JOINT_L / 2)
JOINT3_R = MOTOR3_R - (JOINT_L / 2)


# Iz motoru
MOTOR1_Iz = MOTOR_W*MOTOR1_R**2
MOTOR2_Iz = MOTOR_W*MOTOR2_R**2
MOTOR3_Iz = MOTOR_W*MOTOR3_R**2

# Iz JOINTU
JOINT0_Iz = JOINT_W*JOINT0_R**2
JOINT1_Iz = JOINT_W*JOINT1_R**2
JOINT2_Iz = JOINT_W*JOINT2_R**2
JOINT3_Iz = JOINT_W*JOINT3_R**2
END_EFFECTOR_Iz = END_EFFECTOR_W*END_EFFECTOR_R**2

# Iz Linku - lepsi vzorec
# TODO: vynechavam z vypoctu LINK0 -> ten ma take nejaky prispevek ale dost maly
LINK1_Iz = LINK1_W * (
    LINK1_R**2
    + LINK1_L**2 / 12
    + (LINK_R**2 + LINK_r**2) / 4
)
LINK2_Iz = LINK2_W * (
    LINK2_R**2
    + LINK2_L**2 / 12
    + (LINK_R**2 + LINK_r**2) / 4
)
LINK3_Iz = 1/2 * LINK3_W * (LINK_R**2 + LINK_r**2)

Robot_Iz = MOTOR1_Iz + MOTOR2_Iz + MOTOR3_Iz + JOINT0_Iz + JOINT1_Iz + JOINT2_Iz + JOINT3_Iz + END_EFFECTOR_Iz + LINK1_Iz + LINK2_Iz + LINK3_Iz

T = Robot_Iz * alpha

print("Potrebne zrychleni: " + str(round(T, 2)) + "Nm")

LINK2_F = LINK2_W * alpha * LINK2_R
print("Sila ohybajici LINK2 do strany: " + str(round(LINK2_F, 2)) + "N")

# M / I = o / y
# o = My / I - N / m^2