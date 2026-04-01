from models.upgrades.upgrade import Upgrade


class SpawnUpgrade(Upgrade):
    def __init__(self, spawn_timer):
        super().__init__()
        self.spawn_timer = spawn_timer

    def activate(self):
        if self.spawn_timer[0] > 5:
            self.spawn_timer[0] -= 10
        if self.spawn_timer[1] > 10:
            self.spawn_timer[1] -= 10

        print(self.spawn_timer)

    def __str__(self):
        return "Increase the bird spawning frequency"