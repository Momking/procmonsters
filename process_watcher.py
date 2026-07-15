from dataclasses import dataclass

import psutil

@dataclass
class ProcessSnapshot:
    pid: int
    name: str
    cpu: float
    memory: int

class ProcessWatcher:
    def __init__(self):
        self.processes = {}

    def refresh(self):
        current_processes = {}

        for process in psutil.process_iter(
            ["pid", "name", "memory_info"]
        ):
            pid = process.pid

            if pid in self.processes:
                current_processes[pid] = self.processes[pid]
            else:
                process.cpu_percent(None)
                current_processes[pid] = process

        self.processes = current_processes

        snapshots = []

        for process in self.processes.values():
            try:
                cpu = process.cpu_percent(None)

                snapshot = ProcessSnapshot(
                    pid=process.pid,
                    name=process.name(),
                    cpu=cpu,
                    memory=process.memory_info().rss,
                )

                snapshots.append(snapshot)

            except psutil.NoSuchProcess:
                pass

        return snapshots
