import math
from game_specific import *

class Robot:
    def __init__(self):
        self.mode

        self.cameras = []
        self.motor_boards = []
        self.power_boards = []
        self.servo_boards = []

        self.camera = self.cameras[0]
        self.motor_board = self.motor_boards[0]
        self.power_board = self.power_boards[0]
        self.servo_board = self.servo_boards[0]
