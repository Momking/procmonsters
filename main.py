import time

from process_watcher import ProcessWatcher


watcher = ProcessWatcher()


while True:
    watcher.refresh()

    print("----------------")

    time.sleep(1)
