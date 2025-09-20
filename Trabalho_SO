# sim_scheduler.py
from dataclasses import dataclass
from typing import Optional

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class FIFOQueue:
    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size = 0

    def enqueue(self, item):
        node = Node(item)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = self.tail = node
        self._size += 1

    def dequeue(self):
        if not self.head:
            return None
        node = self.head
        self.head = node.next
        if not self.head:
            self.tail = None
        self._size -= 1
        return node.value

    def is_empty(self):
        return self.head is None

class ReadyQueue:
    def __init__(self):
        self.head: Optional[Node] = None
        self._size = 0

    def enqueue(self, proc):
        node = Node(proc)
        if self.head is None:
            self.head = node
        else:
            if proc.priority < self.head.value.priority:
                node.next = self.head
                self.head = node
            else:
                prev = None
                cur = self.head
                while cur and cur.value.priority <= proc.priority:
                    prev = cur
                    cur = cur.next
                if prev is None:
                    node.next = self.head
                    self.head = node
                else:
                    node.next = prev.next
                    prev.next = node
        self._size += 1

    def dequeue(self):
        if not self.head:
            return None
        node = self.head
        self.head = node.next
        self._size -= 1
        return node.value

    def is_empty(self):
        return self.head is None

@dataclass
class Process:
    pid: int
    arrival: int
    io_time: int
    proc_time: int
    priority: int
    termination_ready: bool = False
    started: bool = False

def simulate(process_list):
    proc_by_arrival = sorted(process_list, key=lambda p: p.arrival)
    idx_next_arrival = 0
    n = len(process_list)

    ready = ReadyQueue()
    io_queue = FIFOQueue()

    cpu_proc: Optional[Process] = None
    cpu_remaining_slice = 0

    io_proc: Optional[Process] = None
    io_remaining_slice = 0

    time = 0
    completed = []

    while len(completed) < n:
        while idx_next_arrival < n and proc_by_arrival[idx_next_arrival].arrival == time:
            p = proc_by_arrival[idx_next_arrival]
            ready.enqueue(p)
            idx_next_arrival += 1

        if cpu_proc is None and not ready.is_empty():
            cpu_proc = ready.dequeue()
            if cpu_proc.termination_ready:
                cpu_remaining_slice = 1
            else:
                cpu_remaining_slice = min(3, cpu_proc.proc_time)
            cpu_proc.started = True

        if io_proc is None and not io_queue.is_empty():
            io_proc = io_queue.dequeue()
            io_remaining_slice = min(6, io_proc.io_time)

        if cpu_proc is not None:
            if cpu_proc.termination_ready:
                cpu_remaining_slice -= 1
            else:
                cpu_proc.proc_time -= 1
                cpu_remaining_slice -= 1

        if io_proc is not None:
            io_proc.io_time -= 1
            io_remaining_slice -= 1

        time += 1

        if cpu_proc is not None and cpu_remaining_slice == 0:
            if cpu_proc.termination_ready:
                completed.append((time, cpu_proc.pid))
                cpu_proc = None
            else:
                if cpu_proc.proc_time > 0 and cpu_proc.io_time == 0:
                    ready.enqueue(cpu_proc)
                elif cpu_proc.proc_time > 0 and cpu_proc.io_time > 0:
                    io_queue.enqueue(cpu_proc)
                elif cpu_proc.proc_time == 0 and cpu_proc.io_time > 0:
                    io_queue.enqueue(cpu_proc)
                else:
                    cpu_proc.termination_ready = True
                    ready.enqueue(cpu_proc)
                cpu_proc = None

        if io_proc is not None and io_remaining_slice == 0:
            if io_proc.proc_time > 0:
                ready.enqueue(io_proc)
            elif io_proc.proc_time == 0 and io_proc.io_time > 0:
                io_queue.enqueue(io_proc)
            else:
                io_proc.termination_ready = True
                ready.enqueue(io_proc)
            io_proc = None

    completed_sorted = sorted(completed, key=lambda x: (x[0], x[1]))
    return completed_sorted

if __name__ == "__main__":
    raw = """1;1;5;12;3
2;2;4;8;2
3;4;3;15;1
4;6;0;7;4
5;8;6;10;5
6;10;2;14;3
7;12;8;7;2
8;14;5;11;4
9;16;3;13;1
10;18;6;9;5
11;20;4;12;2
12;22;7;8;3
13;24;2;15;4
14;26;5;10;1
15;28;3;14;5""".strip().splitlines()

    processes = []
    for line in raw:
        parts = line.strip().split(";")
        pid = int(parts[0])
        arrival = int(parts[1])
        io_time = int(parts[2])
        proc_time = int(parts[3])
        priority = int(parts[4])
        processes.append(Process(pid, arrival, io_time, proc_time, priority))

    result = simulate(processes)

    with open("saida.txt", "w") as f:
        for t, pid in result:
            f.write(f"{t};{pid}\n")

    print("Arquivo 'saida.txt' gerado com sucesso.")
