from entities.npc import NPC

class Companion(NPC):
    def __init__(self, npc_id, name, race, gender, profession, personality):
        super().__init__(npc_id, name, race, gender, profession, personality)
        self.loyalty = 50
        self.morale = 50
        self.combat_skill = 5