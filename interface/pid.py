class PID:
    def __init__(self, Kp, Kd, Ki, integral_limit, target):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.integral_limit = integral_limit
        self.target = target

    def set_pid_constants(self, Kp, Kd, Ki):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
    
    def set_target(self, new_target):
        self.target = new_target

    def pid_calc(self, measure):
        error = self.target - measure
        pout = self.Kp * error

        self.integral += error
        if self.integral > self.integral_limit:
            self.integral = self.integral_limit
        elif self.integral < -(self.integral_limit):
            self.integral = -(self.integral_limit) 
        iout = self.Ki * self.integral

        dout =  self.Kd * (error - self.last_error)

        output = pout + iout + dout
        self.last_error = error
        return output