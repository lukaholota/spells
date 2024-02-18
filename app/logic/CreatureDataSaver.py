from app.logic.CreaturesForm import CreaturesForm
from app.models import Creature, db


class CreatureDataSaver:
    def custom_init(self, data, form: CreaturesForm):
        self.name = data.get('name', '')
        self.name_eng = data.get('name_eng', '')
        self.size = data.get('size', '')
        self.type = data.get('type', '')
        self.alignment = data.get('alignment', '')
        self.source = data.get('source', '')
        self.ac = data.get('ac', '')
        self.hp = data.get('hp', '')
        self.speed = data.get('speed', '')
        self.strength = data.get('strength', '')
        self.dexterity = data.get('dexterity', '')
        self.constitution = data.get('constitution', '')
        self.intelligence = data.get('intelligence', '')
        self.wisdom = data.get('wisdom', '')
        self.charisma = data.get('charisma', '')
        self.skills = data.get('skills', '')
        self.senses = data.get('senses', '')
        self.languages = data.get('languages', '')
        self.challenge = data.get('challenge', '')
        self.damage_immunity = data.get('damage_immunity', '')
        self.damage_resistance = data.get('damage_resistance', '')
        self.condition_immunity = data.get('condition_immunity', '')
        self.saving_throws = data.get('saving_throws', '')
        self.special_abilities = data.get('special_abilities', '')
        self.actions = data.get('actions', '')
        self.reactions = data.get('reactions', '')
        self.legendary_actions = data.get('legendary_actions', '')
        self.description = data.get('description', '')
        self.lair_info = data.get('lair_info', '')
        self.lair_actions = data.get('lair_actions', '')
        self.region_effects = data.get('region_effects', '')

        self.xp = form.challenge_rating_to_xp[self.challenge]
        self.proficiency_bonus = data.get('proficiency_bonus', form.challenge_rating_to_proficiency_bonus[self.challenge])

    def add_new_creature(self):
        creature = Creature(
            name=self.name,
            name_eng=self.name_eng,
            size=self.size,
            type=self.type,
            alignment=self.alignment,
            source=self.source,
            ac=self.ac,
            hp=self.hp,
            speed=self.speed,
            strength=self.strength,
            dexterity=self.dexterity,
            constitution=self.constitution,
            intelligence=self.intelligence,
            wisdom=self.wisdom,
            charisma=self.charisma,
            skills=self.skills,
            senses=self.senses,
            languages=self.languages,
            challenge=self.challenge,
            damage_immunity=self.damage_immunity,
            damage_resistance=self.damage_resistance,
            condition_immunity=self.condition_immunity,
            saving_throws=self.saving_throws,
            special_abilities=self.special_abilities,
            actions=self.actions,
            reactions=self.reactions,
            legendary_actions=self.legendary_actions,
            description=self.description,
            lair_info=self.lair_info,
            lair_actions=self.lair_actions,
            region_effects=self.region_effects,
            proficiency_bonus=self.proficiency_bonus,
            xp=self.xp
        )

        db.session.add(creature)
        db.session.commit()

        self.creature_id = creature.creature_id

    def get_creature(self, id):
        self.creature = Creature.query.get_or_404(id)
        return self.creature

    def edit_creature(self):
        self.creature.name = self.name,
        self.creature.name_eng = self.name_eng,
        self.creature.size = self.size,
        self.creature.type = self.type,
        self.creature.alignment = self.alignment,
        self.creature.source = self.source,
        self.creature.ac = self.ac,
        self.creature.hp = self.hp,
        self.creature.speed = self.speed,
        self.creature.strength = self.strength,
        self.creature.dexterity = self.dexterity,
        self.creature.constitution = self.constitution,
        self.creature.intelligence = self.intelligence,
        self.creature.wisdom = self.wisdom,
        self.creature.charisma = self.charisma,
        self.creature.skills = self.skills,
        self.creature.senses = self.senses,
        self.creature.languages = self.languages,
        self.creature.challenge = self.challenge,
        self.creature.damage_immunity = self.damage_immunity,
        self.creature.damage_resistance = self.damage_resistance,
        self.creature.condition_immunity = self.condition_immunity,
        self.creature.saving_throws = self.saving_throws,
        self.creature.special_abilities = self.special_abilities,
        self.creature.actions = self.actions,
        self.creature.reactions = self.reactions,
        self.creature.legendary_actions = self.legendary_actions,
        self.creature.description = self.description,
        self.creature.lair_info = self.lair_info,
        self.creature.lair_actions = self.lair_actions,
        self.creature.region_effects = self.region_effects,
        self.creature.proficiency_bonus = self.proficiency_bonus,
        self.creature.xp = self.xp

        db.session.commit()
