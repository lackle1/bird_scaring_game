from models.upgrades.upgrade import Upgrade


class SpawnUpgrade(Upgrade):
    def __init__(self, spawn_timer):
        super().__init__()
        self.spawn_timer = spawn_timer

    def activate(self):
        if self.spawn_timer[0] > 15:
            self.spawn_timer -= 5
        if self.spawn_timer[1] > 30:
            self.spawn_timer -= 5

    def __str__(self):
        return "Increase the bird spawning frequency"