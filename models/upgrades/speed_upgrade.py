from models.upgrades.upgrade import Upgrade


class SpeedUpgrade(Upgrade):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def activate(self):
        self.player.speed += 2

    def __str__(self):
        return (f"Increase your speed by 5"
                f"Speed after upgrade -> {self.player.speed + 5}")