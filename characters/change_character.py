from characters.abstract_characters import StaticCharacter, MovableCharacter
from characters.default import DefaultCharacter


def change_character(old: StaticCharacter, new: type[StaticCharacter], time):
    new = new(old.screen, old.position, size=old.screen.size_multiplier)

    if isinstance(new, MovableCharacter):
        new.move_direction = old.move_direction

    old.ground_checker.kill()

    new.rect.y += old.rect.height - new.rect.height
    old.kill()
    old.screen.players[new] = time
    old.screen.players.pop(old)


