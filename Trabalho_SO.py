class Processo:
    def __init__(self, pid, entrada, io, proc, prioridade):
        self.pid = pid
        self.entrada = entrada
        self.io = io
        self.proc = proc
        self.prioridade = prioridade
        self.quantum_cpu_restante = 3  
        self.quantum_io = 6            
        self.finalizado = False
        self.termino = None

    def __str__(self):
        return f"Processo(id={self.pid}, entrada={self.entrada}, io={self.io}, proc={self.proc}, prioridade={self.prioridade})"
    
    def executar_cpu(self):
        if self.proc > 0:
            self.proc -= 1
            self.quantum_cpu_restante -= 1

    def cpu_terminou(self):
        return self.proc == 0

    def quantum_cpu_acabou(self):
        return self.quantum_cpu_restante == 0

    def resetar_quantum_cpu(self):
        self.quantum_cpu_restante = 3

    def executar_io(self):
        if self.io > 0:
            self.io -= 1
            self.quantum_io -= 1

    def io_terminou(self):
        return self.io == 0

    def quantum_io_acabou(self):
        return self.quantum_io == 0

    def resetar_quantum_io(self):
        self.quantum_io = 6


def simular(processos):
    tempo = 0
    fila_prontos = []
    fila_io = []
    cpu = None
    io = None
    finalizados = []

    while len(finalizados) < len(processos):
        for p in processos:
            if p.entrada == tempo:
                fila_prontos.append(p)

        fila_prontos.sort(key=lambda p: p.prioridade)

        if cpu is None and fila_prontos:
            cpu = fila_prontos.pop(0)
            cpu.resetar_quantum_cpu()

        if io is None and fila_io:
            io = fila_io.pop(0)
            io.resetar_quantum_io()

        if cpu:
            cpu.executar_cpu()

        if io:
            io.executar_io()

        tempo += 1 

        if cpu:
            if cpu.cpu_terminou() and cpu.io == 0:
                cpu.finalizado = True
                cpu.termino = tempo
                finalizados.append(cpu)
                cpu = None
            elif cpu.cpu_terminou() and cpu.io > 0:
                fila_io.append(cpu)
                cpu = None
            elif cpu.quantum_cpu_acabou():
                fila_prontos.append(cpu)
                cpu = None

        if io:
            if io.io_terminou() and not io.cpu_terminou():
                fila_prontos.append(io)
                io = None
            elif io.io_terminou() and io.cpu_terminou():
                io.finalizado = True
                io.termino = tempo
                finalizados.append(io)
                io = None
            elif io.quantum_io_acabou():
                fila_io.append(io)
                io = None

    return finalizados


if __name__ == "__main__":
    # dados fixos
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
        pid, entrada, io, proc, prioridade = map(int, linha.split(";"))
        processos.append(Processo(pid, entrada, io, proc, prioridade))

    finalizados = simular(processos)

    # salvar saída
    with open("saida.txt", "w") as f:
        for p in sorted(finalizados, key=lambda x: (x.termino, x.pid)):
            f.write(f"{p.termino};{p.pid}\n")

    print("Simulação concluída! Arquivo 'saida.txt' gerado.")
