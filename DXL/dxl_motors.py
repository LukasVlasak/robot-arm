import dynamixel_sdk as dxl
import numpy as np
from adatools import utils
import time

# This example shows how to use the Dynamixel SDK send and receive joint positions.
# The example uses the Dynamixel SDK's GroupSyncWrite and GroupSyncRead functions to send and receive data to and from the servos.

class DXLMotors:
    def __init__(self,dxl_ids=[1,2,3,4,5],port='/dev/ttyUSB0', baudrate=57600):
        # Define some constants
        self.addr_torque_enable          = 64
        self.addr_goal_position          = 116
        self.len_goal_position           = 4         # data byte length
        self.addr_present_position       = 132
        self.len_present_position        = 4         # data byte length
        self.baudrate                    = baudrate
        self.addr_is_moving              = 122
        self.protocol_version            = 2.0
        self.addr_operating_mode         = 11
        self.addr_profile_velocity       = 112  
        self.len_profile_velocity        = 4
        self.port                        = port  # <-- you may need to change the port where the u2d2 is connected
        self.dxl_ids                     = dxl_ids  # [1, 2, 3, 4, 5]

        self.__init()

    def __init(self):
        # init port & packet hanler
        self.portHandler = dxl.PortHandler(self.port)
        self.packetHandler = dxl.PacketHandler(self.protocol_version) 

        # rdy to communicate
        self.__open_port()
        self.__setBaudRate(self.baudrate)
        
        # group readers/writers
        self.presentPositionReader = dxl.GroupSyncRead(self.portHandler, self.packetHandler, self.addr_present_position, self.len_present_position)
        self.goalPositionWriter = dxl.GroupSyncWrite(self.portHandler, self.packetHandler, self.addr_goal_position, self.len_goal_position)
        self.profileVelocityWriter = dxl.GroupSyncWrite(self.portHandler, self.packetHandler, self.addr_profile_velocity, self.len_profile_velocity)

        # initial settings
        self.setDXLTorqueEnabled(True)
        self.slowAllMotors()

    def __open_port(self):
        if self.portHandler.openPort():
            print("Succeeded to open the port")
        else:  
            print("Failed to open the port")
            quit()

    def __setBaudRate(self, baudrate):
        if self.portHandler.setBaudRate(baudrate):
            print("Succeeded to change the baudrate")
        else:
            print("Failed to change the baudrate")
            quit()

    def setDXLTorqueEnabled(self, enable):
        for id in self.dxl_ids:
            dxl_comm_result, dxl_error = self.packetHandler.write1ByteTxRx(self.portHandler, id, self.addr_torque_enable, 1 if enable == True else 0)
            self.__checkRWResult(dxl_comm_result, dxl_error, "Torque enabled")


    def slowAllMotors(self):
        self.profileVelocityWriter.clearParam()

        param_velocity_43 = utils.to4bytes(43) # HARD CODED -> observe when testing

        for dxl_id in self.dxl_ids:
            self.profileVelocityWriter.addParam(dxl_id, param_velocity_43)

        dxl_comm_result = self.profileVelocityWriter.txPacket()
        self.__checkRWResult(dxl_comm_result)

        self.profileVelocityWriter.clearParam()

    def getIsMoving(self, id):
        self.__checkID(id)

        is_moving, dxl_comm_result, dxl_error = self.packetHandler.read1ByteTxRx(self.portHandler, id, self.addr_is_moving)

        self.__checkRWResult(dxl_comm_result, dxl_error)
        return is_moving == 1

    def getSingleMotorPos(self, id):
        self.__checkID(id)
        
        position, dxl_comm_result, dxl_error = self.packetHandler.read4ByteTxRx(self.portHandler, id, self.addr_present_position)
        self.__checkRWResult(dxl_comm_result, dxl_error)

        return position
    
    def getMotorsPos(self, ids=None):
        result = []
        if ids is None:
            ids = self.dxl_ids

        self.presentPositionReader.clearParam()
        for id in ids:
            self.presentPositionReader.addParam(id)

        dxl_comm_result = self.presentPositionReader.txRxPacket()
        self.__checkRWResult(dxl_comm_result)

        for id in ids:
            is_available = self.presentPositionReader.isAvailable(id, self.addr_present_position, self.len_present_position)

            if not is_available:
                raise RuntimeError("Data for group reading not available")

            pos = self.presentPositionReader.getData(id, self.addr_present_position, self.len_present_position)
            result.append(pos)

        return result

    def setMotorsGoalPos(self, pos):
        """
            Pri zadani -1 motor zustane a ostatni se pohnou
            Funguje i pri zadani mene motoru - napr. 3 kdyz mam 5 - tak proste vezme prvni 3
        """
        if len(pos) > len(self.dxl_ids) or len(pos) == 0:
            print("DEMENTE TOLIK MOTORU NEMAS")
            return

        self.goalPositionWriter.clearParam()
        goal_pos = utils.to4bytes(pos)

        for i in range(len(goal_pos)):
            if int(pos[i]) != -1:
                self.goalPositionWriter.addParam(self.dxl_ids[i], goal_pos[i])

        dxl_comm_result = self.goalPositionWriter.txPacket()
        self.__checkRWResult(dxl_comm_result)

        # 4. ČIŠTĚNÍ PO ODESLÁNÍ (Doporučená praxe pro vyčištění paměti)
        self.goalPositionWriter.clearParam()

    def setSingleMotorGoalPos(self, pos, id):
        self.__checkID(id)
        
        dxl_comm_result, dxl_error = self.packetHandler.write4ByteTxRx(self.portHandler, id, self.addr_goal_position, int(pos))
        self.__checkRWResult(dxl_comm_result, dxl_error)



    def __checkID(self, id):
        if id not in self.dxl_ids:
            raise ValueError("ID is not in available IDs")

    def __checkRWResult(self, dxl_comm_result, dxl_error=None, success_msg=None):
        if dxl_comm_result != dxl.COMM_SUCCESS:
            err_msg = self.packetHandler.getTxRxResult(dxl_comm_result)
            raise RuntimeError(f"[COMM ERROR] {err_msg}")

        if dxl_error is not None and dxl_error != 0:
            err_msg = self.packetHandler.getRxPacketError(dxl_error)
            raise RuntimeError(f"[HARDWARE ERROR] {err_msg}")

        if success_msg is not None:
            print(success_msg)

    
    