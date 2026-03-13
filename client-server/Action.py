class Action:

    def __init__(self, name, dx, dy, shoot):
        self.name = name
        self.dx = dx
        self.dy = dy
        self.shoot = shoot  # (target_x, target_y) of None

    def get_name(self):
        return self.name

    def get_dx(self):
        return self.dx

    def get_dy(self):
        return self.dy

    def get_shoot(self):
        return self.shoot