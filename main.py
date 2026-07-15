import time

from monster_manager import MonsterManager
from process_watcher import ProcessWatcher


watcher = ProcessWatcher()
manager = MonsterManager()


last_time = time.monotonic()
last_process_refresh = 0.0


while True:
    current_time = time.monotonic()

    dt = current_time - last_time
    last_time = current_time

    if current_time - last_process_refresh >= 1.0:
        snapshots = watcher.refresh()

        manager.sync(snapshots)

        last_process_refresh = current_time

    manager.update(dt)

    for monster in manager.monsters.values():
        print(
            monster.pid,
            monster.species,
            f"x={monster.x:.2f}",
            f"cpu={monster.cpu:.1f}",
        )

    print("----------------")

    time.sleep(0.1)
