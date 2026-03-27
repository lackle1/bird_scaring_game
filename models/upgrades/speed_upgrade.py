from models.upgrades.upgrade import Upgrade


class SpeedUpgrade(Upgrade):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def activate(self):
        self.player.speed += 1

    def __str__(self):
        return "Increase your speed by 1"