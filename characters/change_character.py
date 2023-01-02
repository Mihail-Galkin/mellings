from characters.abstract_characters import StaticCharacter, MovableCharacter


def change_character(old: StaticCharacter, new: type, time):
    new: StaticCharacter = new(old.screen, old.position)
    if isinstance(new, MovableCharacter) and isinstance(old, MovableCharacter):
        new.move_direction = old.move_direction
        new.velocities = old.velocities
        new.forces = old.forces
    if isinstance(old, MovableCharacter):
        old.ground_checker.kill()
    old.kill()
    old.screen.players[new] = -1
    old.screen.players.pop(old)