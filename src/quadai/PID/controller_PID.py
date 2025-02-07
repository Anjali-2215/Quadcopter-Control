"""
Simple PID Controller
"""

class PID:
    def __init__(self, KP, KI, KD, saturation_max, saturation_min):
        self.kp = KP
        self.ki = KI
        self.kd = KD
        self.error_last = 0
        self.integral_error = 0
        self.saturation_max = saturation_max
        self.saturation_min = saturation_min

    def compute(self, error, dt):
        derivative_error = (error - self.error_last) / dt
        self.integral_error += error * dt
        output = self.kp * error + self.ki * self.integral_error + self.kd * derivative_error
        self.error_last = error
        if self.saturation_max is not None and output > self.saturation_max:
            output = self.saturation_max
        elif self.saturation_min is not None and output < self.saturation_min:
            output = self.saturation_min
        return output
