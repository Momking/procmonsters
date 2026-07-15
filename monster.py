from dataclasses import dataclass

from species import Species


@dataclass
class Monster:
    pid: int
    name: str
    species: Species
    cpu: float

    x: float
    y: float

    vx: float
    phase: float

    def update(self, dt):
        activity = min(self.cpu / 100.0, 1.0)

        self.x += self.vx * dt

        self.phase += dt * (
            2.0 + activity * 4.0
        )
