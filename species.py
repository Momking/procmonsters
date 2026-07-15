from enum import Enum, auto


class Species(Enum):
    FOX = auto()
    CRAB = auto()
    SNAKE = auto()
    DRAGON = auto()
    ROBOT = auto()
    ALIEN = auto()
    SHELL = auto()

def species_for_process(name):
    name = name.lower()

    if "firefox" in name or "zen" in name:
        return Species.FOX

    if "cargo" in name or "rustc" in name:
        return Species.CRAB

    if "python" in name:
        return Species.SNAKE

    if "gcc" in name or "clang" in name:
        return Species.DRAGON

    if "code" in name or "codium" in name:
        return Species.ROBOT

    if "qemu" in name:
        return Species.ALIEN

    if name in ["bash", "zsh-bin", "fish"]:
        return Species.SHELL

    return None
