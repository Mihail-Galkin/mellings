
def change_character(old, new: type, time):
    from characters.abstract_characters import MovableCharacter
    new = new(old.screen, old.position, size=old.screen.size_multiplier)

    if isinstance(new, MovableCharacter) and isinstance(old, MovableCharacter):
        new.move_direction = old.move_direction

    old.ground_checker.kill()

    new.rect.y += old.rect.height - new.rect.height
    old.kill()
    old.screen.players[new] = time
    old.screen.players.pop(old)
