# sim_scheduler.py
# Simulador de escalonamento de processos (CPU + I/O)
# Regras:
# - Fatia de CPU = 3 ciclos
# - Fatia de I/O = 6 ciclos
# - Fila de prontos = ordenada por prioridade (menor número = mais prioritário)
# - Fila de I/O = FIFO
# - Estruturas implementadas manualmente (sem bibliotecas prontas)

# ---------------------------
# Estruturas de dados
# ---------------------------
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class FIFOQueue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, item):
        node = Node(item)
        if self.tail:
            self.tail.next = node
            self.tail = node
        else:
            self.head = self.tail = node

    def dequeue(self):
        if not self.head:
            return None
        node = self.head
        self.head = node.next
        if not self.head:
            self.tail = None
        return node.value

    def is_empty(self):
        return self.head is None

class ReadyQueue:
    def __init__(self):
        self.head = None

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

    def dequeue(self):
        if not self.head:
            return None
        node = self.head
        self.head = node.next
        return node.value

    def is_empty(self):
        return self.head is None

# ---------------------------
# Classe de processo
# ---------------------------
class Process:
    def __init__(self, pid, arrival, io_time, proc_time, priority):
        self.pid = pid
        self.arrival = arrival
        self.io_time = io_time
        self.proc_time = proc_time
        self.priority = priority
        self.termination_ready = False

# ---------------------------
# Simulação
# ---------------------------
def simulate(process_list):
    proc_by_arrival = sorted(process_list, key=lambda p: p.arrival)
    idx_next_arrival = 0
    n = len(process_list)

    ready = ReadyQueue()
    io_queue = FIFOQueue()

    cpu_proc = None
    cpu_slice = 0

    io_proc = None
    io_slice = 0

    time = 0
    completed = []

    while len(completed) < n:
        # chegada de novos processos
        while idx_next_arrival < n and proc_by_arrival[idx_next_arrival].arrival == time:
            ready.enqueue(proc_by_arrival[idx_next_arrival])
            idx_next_arrival += 1

        # CPU pega processo se estiver livre
        if cpu_proc is None and not ready.is_empty():
            cpu_proc = ready.dequeue()
            if cpu_proc.termination_ready:
                cpu_slice = 1
            else:
                if cpu_proc.proc_time >= 3:
                    cpu_slice = 3
                else:
                    cpu_slice = cpu_proc.proc_time

        # I/O pega processo se estiver livre
        if io_proc is None and not io_queue.is_empty():
            io_proc = io_queue.dequeue()
            if io_proc.io_time >= 6:
                io_slice = 6
            else:
                io_slice = io_proc.io_time

        # Executa 1 ciclo
        if cpu_proc is not None:
            if cpu_proc.termination_ready:
                cpu_slice -= 1
            else:
                cpu_proc.proc_time -= 1
                cpu_slice -= 1

        if io_proc is not None:
            io_proc.io_time -= 1
            io_slice -= 1

        time += 1

        # Verifica término CPU
        if cpu_proc is not None and cpu_slice == 0:
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

        # Verifica término I/O
        if io_proc is not None and io_slice == 0:
            if io_proc.proc_time > 0:
                ready.enqueue(io_proc)
            elif io_proc.proc_time == 0 and io_proc.io_time > 0:
                io_queue.enqueue(io_proc)
            else:
                io_proc.termination_ready = True
                ready.enqueue(io_proc)
            io_proc = None

    return sorted(completed, key=lambda x: (x[0], x[1]))

# ---------------------------
# Main
# ---------------------------
if __name__ == "__main__":
    dados = """1;1;5;12;3
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
15;28;3;14;5""".splitlines()

    processos = []
    for linha in dados:
        partes = linha.strip().split(";")
        pid = int(partes[0])
        chegada = int(partes[1])
        io = int(partes[2])
        cpu = int(partes[3])
        prio = int(partes[4])
        processos.append(Process(pid, chegada, io, cpu, prio))

    resultado = simulate(processos)

    with open("saida.txt", "w") as f:
        for tempo, pid in resultado:
            f.write(str(tempo) + ";" + str(pid) + "\n")

    print("Simulação concluída. Arquivo 'saida.txt' gerado.")
