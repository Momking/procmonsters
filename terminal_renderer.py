from species import Species


def character_for_species(species):
    if species == Species.SNAKE:
        return "S"

    if species == Species.FOX:
        return "F"

    if species == Species.CRAB:
        return "C"

    if species == Species.DRAGON:
        return "D"

    if species == Species.ROBOT:
        return "R"

    if species == Species.ALIEN:
        return "A"

    if species == Species.SHELL:
        return "H"

    return "?"


class TerminalRenderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def render(self, monsters):
        print("\033[2J\033[H", end="")
        
        screen = []

        for _ in range(self.height):
            row = ["."] * self.width

            screen.append(row)

        for monster in monsters:
            x = int(monster.x)
            y = int(monster.y)

            character = character_for_species(
                monster.species
            )

            screen[y][x] = character

        for row in screen:
            print("".join(row))
