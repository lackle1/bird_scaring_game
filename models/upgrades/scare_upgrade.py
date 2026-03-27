from models.upgrades.upgrade import Upgrade


class ScareUpgrade(Upgrade):
    def __init__(self, player):
        super().__init__()
        self.player = player

    def activate(self):
        self.player.scare_radius += 5

    def __str__(self):
        return (f"Increase your scaring radius by 5\n"
                f"Scare radius after upgrade -> {self.player.scare_radius + 5}")