from app.app import ma
from app.models import Spell, SpellClasses, SpellRaces


class SpellClassesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpellClasses
        include_fk = True

class SpellRacesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpellRaces
        include_fk = True

class SpellSchema(ma.SQLAlchemyAutoSchema):
    classes = ma.Nested(SpellClassesSchema, many=True)
    races = ma.Nested(SpellRacesSchema, many=True)

    class Meta:
        model = Spell
        include_fk = True

spells_schema = SpellSchema(many=True)
