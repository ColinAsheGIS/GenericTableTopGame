import pytest

from characters import NPCharacterBuilder, PhysicalStats, CharacterSize, Alignment, Lawfulness, Goodness, \
    BaseStats, Speed, AbilityScores, SavingThrows, Skills, DamageType, \
    DamageModifiers, Senses, Sense, Challenge, Languages, Language, Traits, Trait, \
    physical_stats_by_id, alignment_by_id, base_stats_by_id, ability_scores_by_id, saving_throws_by_id, skills_by_id, \
    immunities_by_id, senses_by_id


class TestBuilders:

    @pytest.fixture(scope='class')
    def physical_stats(self) -> PhysicalStats:
        return PhysicalStats(
            size=CharacterSize.TINY,
            type="beast",
            tags='orcish'
        )

    @pytest.fixture(scope='class')
    def alignment(self) -> Alignment:
        return Alignment(
            lawfulness=Lawfulness.CHAOTIC,
            goodness=Goodness.EVIL
        )

    @pytest.fixture(scope='class')
    def base_stats(self) -> BaseStats:
        return BaseStats(
            armor_class=15,
            hit_points=12,
            speed=Speed(
                walk=30,
                burrow=0,
                climb=10,
                fly=60,
                swim=30
            )
        )

    @pytest.fixture(scope='class')
    def ability_scores(self) -> AbilityScores:
        return AbilityScores(
            strength=11,
            dexterity=15,
            wisdom=8,
            constitution=21,
            intelligence=4,
            charisma=6
        )

    @pytest.fixture(scope='class')
    def saving_throws(self) -> SavingThrows:
        return SavingThrows(
            strength=True,
            dexterity=False,
            wisdom=False,
            constitution=False,
            intelligence=False,
            charisma=False
        )

    @pytest.fixture(scope='class')
    def skills(self) -> Skills:
        return Skills(
            1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8
        )

    @pytest.fixture(scope='class')
    def damage_modifiers(self) -> DamageModifiers:
        return DamageModifiers(
            immunities={DamageType.ACID},
            resistances=set(),
            vulnerabilities={DamageType.COLD, DamageType.FIRE}
        )

    @pytest.fixture(scope='class')
    def senses(self) -> Senses:
        return Senses(
            passive_perception=4,
            senses={Sense.DARKVISION, Sense.TREMORSENSE}
        )

    @pytest.fixture(scope='class')
    def challenge_rating(self) -> Challenge:
        return Challenge(4)

    @pytest.fixture(scope='class')
    def languages(self) -> Languages:
        return Languages(
            True,
            {Language.HUMAN, Language.GOBLIN}
        )

    @pytest.fixture(scope='class')
    def traits(self) -> Traits:
        return Traits(
            {Trait.SPELLCASTING}
        )

    def test_np_character_builder(
            self,
            physical_stats,
            alignment,
            base_stats,
            ability_scores,
            saving_throws,
            skills,
            damage_modifiers,
            senses,
            challenge_rating,
            languages,
            traits
    ):
        np_character = NPCharacterBuilder()

        np_character = np_character \
            .build_physical_stats(physical_stats) \
            .build_behaviours(alignment) \
            .build_base_stats(base_stats) \
            .build_ability_scores(ability_scores) \
            .build_saving_throws(saving_throws) \
            .build_skills(skills) \
            .build_immunities(damage_modifiers) \
            .build_senses(senses) \
            .build_challenge(challenge_rating) \
            .build_language(languages) \
            .build_traits(traits) \
            .build_meta()

        output_character = np_character.character

        # Once character is assigned to a variable, it is freed from
        # character prop of NPCharacterBuilder instance and process can start over.
        assert np_character.character == NPCharacterBuilder().character

        assert output_character.physical_stats == physical_stats
        assert output_character.alignment == alignment
        assert output_character.base_stats.armor_class == 15
        assert output_character.base_stats.speed.climb == 10
        assert output_character.ability_scores.strength.value == 11
        assert output_character.saving_throws.wisdom == False
        assert output_character.skills
        assert output_character.damage_modifiers.resistances == set()
        assert output_character.damage_modifiers.vulnerabilities == {DamageType.COLD, DamageType.FIRE}
        assert output_character.traits.traits == {Trait.SPELLCASTING}


class TestSQLQueries:

    def test_physical_stats_by_id(self):
        goblin_id = 340
        hobgoblin_id = 368

        goblin_query = physical_stats_by_id(goblin_id)
        assert goblin_query.size == "small"
        assert goblin_query.type == "humanoid"

        hobgoblin_query = physical_stats_by_id(hobgoblin_id)
        assert hobgoblin_query.size == "medium"
        assert hobgoblin_query.type == "humanoid"
        assert isinstance(hobgoblin_query, PhysicalStats)

    def test_alignment_by_id(self):
        goblin_id = 340

        goblin_alignment = Alignment(**{
            "lawfulness": "neutral",
            "goodness": "evil"
        })

        goblin_query = alignment_by_id(goblin_id)
        assert goblin_query == goblin_alignment

    def test_base_stats_by_id(self):
        goblin_id = 340

        goblin_base_stats = BaseStats(**{
            "armor_class": 15,
            "hit_points": 7,
            "speed": Speed(**{
                "burrow": 0,
                "climb": 0,
                "fly": 0,
                "swim": 0,
                "walk": 30
            })
        })

        goblin_query = base_stats_by_id(goblin_id)
        assert goblin_base_stats == goblin_query

    def test_ability_scores_by_id(self):
        goblin_id = 340

        goblin_scores = AbilityScores(**{
            "strength": 8,
            "dexterity": 14,
            "wisdom": 8,
            "constitution": 10,
            "intelligence": 10,
            "charisma": 8
        })

        goblin_query = ability_scores_by_id(goblin_id)
        assert goblin_scores == goblin_query

    def test_saving_throws_by_id(self):
        goblin_id = 340

        goblin_saves = SavingThrows(**{
            "strength": False,
            "dexterity": False,
            "wisdom": False,
            "constitution": False,
            "charisma": False,
            "intelligence": False
        })

        goblin_query = saving_throws_by_id(goblin_id)

        assert goblin_saves == goblin_query

    def test_skills_by_id(self):
        goblin_id = 340

        goblin_skills = Skills(
            **{'intimidation': 0, 'perception': 0, 'investigation': 0, 'acrobatics': 0, 'animal_handling': 0,
               'religion': 0, 'insight': 0, 'survival': 0, 'arcana': 0, 'medicine': 0, 'history': 0,
               'sleight_of_hand': 0,
               'athletics': 0, 'nature': 0, 'persuasion': 0, 'stealth': 1, 'performance': 0, 'deception': 0}
        )

        goblin_query = skills_by_id(goblin_id)
        assert goblin_query == goblin_skills

    def test_immunities_by_id(self):
        goblin_id = 340

        goblin_immunities = DamageModifiers(**{
            "immunities": set(),
            "resistances": set(),
            "vulnerabilities": set()
        })

        goblin_query = immunities_by_id(goblin_id)
        assert goblin_query == goblin_immunities

    def test_senses_by_id(self):
        goblin_id = 340

        goblin_senses = Senses(**{
            "passive_perception": -1,
            "senses": {'darkvision'}
        })

        goblin_query = senses_by_id(goblin_id)
        assert goblin_query == goblin_senses

