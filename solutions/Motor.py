class Motor:
    def __init__(self, id, offset, packet_handler):
        self.id = id
        self.offset = offset
        self.packet_handler = packet_handler

        self.packet_handler.ServoMode(self.id)
        self.packet_handler.change_hold(self.id, 0)
        self.packet_handler.set_max_angle(self.id, 0)
        self.packet_handler.set_min_angle(self.id, 0)
        self.packet_handler.set_multiturn(self.id)
        

    def shutdown(self):
        self.packet_handler.change_hold(self.id, 0)
        print(f"Motor {self.id} shutdown")

    def get_position_raw(self):
        position, _, _, _ = self.packet_handler.ReadPosSpeed(self.id)
        return position - 4096 + self.offset 
    
    def get_position(self):
        position_raw = self.get_position_raw()
        return -position_raw * 2 * 3.141592653589793 / 4096
    
    def get_speed(self):
        _, speed, _, _ = self.packet_handler.ReadPosSpeed(self.id)
        return speed
    
    def set_position(self, position, speed=1000):
        position_raw = int(-position * 4096 / (2 * 3.141592653589793) + 4096 - self.offset)
        self.set_position_raw(position_raw, speed)

    def set_position_raw(self, position, speed=1000):
        if position < 0:
            position = -32768 - position
        self.packet_handler.WritePosEx(self.id, position, int(speed), 0)
