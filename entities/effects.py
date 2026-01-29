class Effects:
    # Aucun effet ne devrais être de la classe Effects, seulement des classes filles
    def __init__(self, name, target, max_duration, multi=1):
        self.name = name
        self.target = target
        self.max_duration = max_duration
        self.duration = self.max_duration
        self.multi = multi


    def activate(self):
        if self not in self.target.effects_list:
            self.duration = self.max_duration
            self.target.add_effect(self)
            self.effect_on()
        else:
            self.duration = self.max_duration


    def update(self, dt):
        if self.duration > 0:
            self.duration -= dt
        else:
            self.effect_off()
            self.target.remove_effect(self)



class XSpeedModifier(Effects):
    def __init__(self, target, multi, max_duration=100):
        super().__init__("x_speed_modifier", target, max_duration, multi)


    def effect_on(self):
        self.target.set_x_speed(self.target.x_speed * self.multi)


    def effect_off(self):
        self.target.set_x_speed(self.target.x_speed * (1/self.multi))



class YSpeedModifier(Effects):
    def __init__(self, target, multi, max_duration=100):
        super().__init__("y_speed_modifier", target, max_duration, multi)


    def effect_on(self):
        self.target.set_y_speed(self.target.y_speed * self.multi)


    def effect_off(self):
        self.target.set_y_speed(self.target.y_speed * (1/self.multi))