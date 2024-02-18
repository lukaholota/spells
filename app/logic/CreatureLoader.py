from app.models import Creature


class CreatureLoader:
    def __init__(self, id):
        self.creature = Creature.query.get_or_404(id)
