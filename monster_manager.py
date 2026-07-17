from monster import Monster
from species import species_for_process

import random

class MonsterManager:
    def __init__(self, world_width, world_height):
        self.monsters = {}

        self.world_width = world_width
        self.world_height = world_height

    def sync(self, snapshots):
        active_pids = set()

        for snapshot in snapshots:
            species = species_for_process(snapshot.name)

            if species is None:
                continue

            active_pids.add(snapshot.pid)

            if snapshot.pid not in self.monsters:
                spawn_margin = 120.0

                monster = Monster(
                    pid=snapshot.pid,
                    name=snapshot.name,
                    species=species,
                    cpu=snapshot.cpu,
                    memory=snapshot.memory,
                    x=random.uniform(
                        spawn_margin,
                        self.world_width - spawn_margin,
                    ),
                    y=random.uniform(
                        spawn_margin,
                        self.world_height - spawn_margin,
                    ),
                    vx=random.uniform(60.0, 180.0),
                    phase=random.uniform(0.0, 6.28),
                )

                self.monsters[snapshot.pid] = monster

            else:
                monster = self.monsters[snapshot.pid]

                monster.cpu = snapshot.cpu
                monster.memory = snapshot.memory

        dead_pids = []

        for pid in self.monsters:
            if pid not in active_pids:
                dead_pids.append(pid)

        for pid in dead_pids:
            del self.monsters[pid]

    def update(self, dt):
        for monster in self.monsters.values():
            monster.update(
                dt,
                self.world_width,
            )
