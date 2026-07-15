from monster import Monster
from species import species_for_process


class MonsterManager:
    def __init__(self):
        self.monsters = {}

    def sync(self, snapshots):
        active_pids = set()

        for snapshot in snapshots:
            species = species_for_process(snapshot.name)

            if species is None:
                continue

            active_pids.add(snapshot.pid)

            if snapshot.pid not in self.monsters:
                monster = Monster(
                    pid=snapshot.pid,
                    name=snapshot.name,
                    species=species,
                    cpu=snapshot.cpu,
                    x=0.0,
                    y=5.0,
                    vx=10.0,
                    phase=0.0,
                )

                self.monsters[snapshot.pid] = monster

            else:
                monster = self.monsters[snapshot.pid]

                monster.cpu = snapshot.cpu

        dead_pids = []

        for pid in self.monsters:
            if pid not in active_pids:
                dead_pids.append(pid)

        for pid in dead_pids:
            del self.monsters[pid]

    def update(self, dt):
        for monster in self.monsters.values():
            monster.update(dt)
