import time

from cairo_renderer import CairoRenderer
from monster_manager import MonsterManager
from process_watcher import ProcessWatcher


watcher = ProcessWatcher()

renderer = CairoRenderer(
    width=1280,
    height=720,
)

manager = MonsterManager(
    world_width=renderer.width,
    world_height=renderer.height,
)


last_time = time.monotonic()
last_process_refresh = 0.0

frame = 0


while frame < 120:
    current_time = time.monotonic()

    dt = current_time - last_time
    last_time = current_time

    if current_time - last_process_refresh >= 1.0:
        snapshots = watcher.refresh()

        manager.sync(snapshots)

        last_process_refresh = current_time

    manager.update(dt)

    renderer.render(
        manager.monsters.values()
    )

    renderer.write_to_png(
        f"frame-{frame:04d}.png"
    )

    frame += 1

    time.sleep(1.0 / 30.0)
