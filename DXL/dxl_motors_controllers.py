import dxl_motors

HOME_POS_MOTOR_1 = 1250
HOME_POS_MOTOR_2 = 1250
HOME_POS_MOTOR_3 = 1250
HOME_POS_MOTOR_4 = 2298
HOME_POS_MOTOR_5 = 3052

MIN_POS_MOTOR_1 = 1500
MIN_POS_MOTOR_2 = 1500
MIN_POS_MOTOR_3 = 1500
MIN_POS_MOTOR_4 = 1412
MIN_POS_MOTOR_5 = 0

MAX_POS_MOTOR_1 = 1500
MAX_POS_MOTOR_2 = 1500
MAX_POS_MOTOR_3 = 1500
MAX_POS_MOTOR_4 = 1500
MAX_POS_MOTOR_5 = 3073

HOME_POS_MOTORS = [HOME_POS_MOTOR_1, HOME_POS_MOTOR_2, HOME_POS_MOTOR_3, HOME_POS_MOTOR_4, HOME_POS_MOTOR_5]
MIN_POS_MOTORS = [MIN_POS_MOTOR_1, MIN_POS_MOTOR_2, MIN_POS_MOTOR_3, MIN_POS_MOTOR_4, MIN_POS_MOTOR_5]
MAX_POS_MOTORS = [MAX_POS_MOTOR_1, MAX_POS_MOTOR_2, MAX_POS_MOTOR_3, MAX_POS_MOTOR_4, MAX_POS_MOTOR_5]


ACTIVE_MOTORS = [4, 5]

class DXLMotorsController:
    def __init__(self):
        self.active_home_pos_motors = [HOME_POS_MOTORS[motor - 1] for motor in ACTIVE_MOTORS]
        self.active_min_pos_motors = [MIN_POS_MOTORS[motor - 1] for motor in ACTIVE_MOTORS]
        self.active_max_pos_motors = [MAX_POS_MOTORS[motor - 1] for motor in ACTIVE_MOTORS]

        self.dxlMotors = dxl_motors.DXLMotors(ACTIVE_MOTORS)
        

    def test(self, vstup):
        vstup = [2, 160]

        raw_vstup = []

        for i in range(len(vstup)):
            if vstup[i] != -1:
                raw_vstup.append(self.deg2raw(vstup[i], HOME_POS_MOTORS[i], MIN_POS_MOTORS[i], MAX_POS_MOTORS[i]))
            else:
                raw_vstup.append(-1)

    def goToHomePosition(self):
        self.dxlMotors.setMotorsGoalPos(self.active_home_pos_motors)
        print("MOTORS ARE IN HOME POSITION")

    def deg2raw(deg, home, min_pos, max_pos):
        """Převede úhel ve stupních (-180 až +180) na raw hodnotu serva."""
        # Omezení vstupu na povolený rozsah
        deg = max(-180.0, min(180.0, float(deg)))

        if deg < 0:
            # Dráha do záporu (-180° -> MIN, 0° -> HOME)
            scale = (home - min_pos) / 180.0
            raw = home + (deg * scale)
        else:
            # Dráha do kladu (0° -> HOME, +180° -> MAX)
            scale = (max_pos - home) / 180.0
            raw = home + (deg * scale)

        return int(round(raw))


    def raw2deg(raw, home, min_pos, max_pos):
        """Převede raw hodnotu ze serva na úhel ve stupních (-180 až +180)."""
        # Omezení vstupu na povolené hardwarové limity
        raw = max(min_pos, min(max_pos, int(raw)))

        if raw < home:
            # Záporný úhel
            deg = (raw - home) / ((home - min_pos) / 180.0)
        else:
            # Kladný úhel
            deg = (raw - home) / ((max_pos - home) / 180.0)

        return round(deg, 2)
        
