import psutil


class ProcessWatcher:
    def __init__(self):
        self.processes = {}

    def refresh(self):
        current_processes = {}

        for process in psutil.process_iter(
            ["pid", "name"]
        ):
            pid = process.pid

            if pid in self.processes:
                current_processes[pid] = self.processes[pid]
            else:
                process.cpu_percent(None)
                current_processes[pid] = process

        self.processes = current_processes

        for process in self.processes.values():
            try:
                cpu = process.cpu_percent(None)

                if cpu >= 1.0:
                    print(
                        process.pid,
                        process.name(),
                        cpu,
                    )

            except psutil.NoSuchProcess:
                pass
