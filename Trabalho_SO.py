# simulador.py
# Simulador de escalonamento de processos (CPU + Entrada/Saída)
# Regras:
# - Fatia de CPU = 3 ciclos
# - Fatia de Entrada/Saída = 6 ciclos
# - Fila de prontos = ordenada por prioridade (menor número = mais prioridade)
# - Fila de E/S = FIFO
# - Estruturas de dados feitas manualmente, sem bibliotecas prontas

# ---------------------------
# Estruturas de dados
# ---------------------------

class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class FilaFIFO:
    def __init__(self):
        self.inicio = None
        self.fim = None

    def enfileirar(self, item):
        no = No(item)
        if self.fim:
            self.fim.proximo = no
            self.fim = no
        else:
            self.inicio = self.fim = no

    def desenfileirar(self):
        if not self.inicio:
            return None
        no = self.inicio
        self.inicio = no.proximo
        if not self.inicio:
            self.fim = None
        return no.valor

    def vazia(self):
        return self.inicio is None

class FilaProntos:
    def __init__(self):
        self.inicio = None

    def enfileirar(self, processo):
        no = No(processo)
        if self.inicio is None:
            self.inicio = no
        else:
            if processo.prioridade < self.inicio.valor.prioridade:
                no.proximo = self.inicio
                self.inicio = no
            else:
                anterior = None
                atual = self.inicio
                while atual and atual.valor.prioridade <= processo.prioridade:
                    anterior = atual
                    atual = atual.proximo
                if anterior is None:
                    no.proximo = self.inicio
                    self.inicio = no
                else:
                    no.proximo = anterior.proximo
                    anterior.proximo = no

    def desenfileirar(self):
        if not self.inicio:
            return None
        no = self.inicio
        self.inicio = no.proximo
        return no.valor

    def vazia(self):
        return self.inicio is None

# ---------------------------
# Classe de Processo
# ---------------------------

class Processo:
    def __init__(self, pid, chegada, tempo_es, tempo_cpu, prioridade):
        self.pid = pid
        self.chegada = chegada
        self.tempo_es = tempo_es
        self.tempo_cpu = tempo_cpu
        self.prioridade = prioridade
        self.encerramento_pendente = False  # precisa de 1 ciclo só para encerrar

# ---------------------------
# Simulação
# ---------------------------

def simular(lista_processos):
    processos_ordenados = sorted(lista_processos, key=lambda p: p.chegada)
    proximo_idx = 0
    total = len(lista_processos)

    prontos = FilaProntos()
    fila_es = FilaFIFO()

    processo_cpu = None
    fatia_cpu = 0

    processo_es = None
    fatia_es = 0

    tempo = 0
    finalizados = []

    while len(finalizados) < total:
        # chegada de novos processos
        while proximo_idx < total and processos_ordenados[proximo_idx].chegada == tempo:
            prontos.enfileirar(processos_ordenados[proximo_idx])
            proximo_idx += 1

        # CPU pega processo
        if processo_cpu is None and not prontos.vazia():
            processo_cpu = prontos.desenfileirar()
            if processo_cpu.encerramento_pendente:
                fatia_cpu = 1
            else:
                if processo_cpu.tempo_cpu >= 3:
                    fatia_cpu = 3
                else:
                    fatia_cpu = processo_cpu.tempo_cpu

        # E/S pega processo
        if processo_es is None and not fila_es.vazia():
            processo_es = fila_es.desenfileirar()
            if processo_es.tempo_es >= 6:
                fatia_es = 6
            else:
                fatia_es = processo_es.tempo_es

        # Executa 1 ciclo
        if processo_cpu is not None:
            if processo_cpu.encerramento_pendente:
                fatia_cpu -= 1
            else:
                processo_cpu.tempo_cpu -= 1
                fatia_cpu -= 1

        if processo_es is not None:
            processo_es.tempo_es -= 1
            fatia_es -= 1

        tempo += 1

        # Verifica término da CPU
        if processo_cpu is not None and fatia_cpu == 0:
            if processo_cpu.encerramento_pendente:
                finalizados.append((tempo, processo_cpu.pid))
                processo_cpu = None
            else:
                if processo_cpu.tempo_cpu > 0 and processo_cpu.tempo_es == 0:
                    prontos.enfileirar(processo_cpu)
                elif processo_cpu.tempo_cpu > 0 and processo_cpu.tempo_es > 0:
                    fila_es.enfileirar(processo_cpu)
                elif processo_cpu.tempo_cpu == 0 and processo_cpu.tempo_es > 0:
                    fila_es.enfileirar(processo_cpu)
                else:
                    processo_cpu.encerramento_pendente = True
                    prontos.enfileirar(processo_cpu)
                processo_cpu = None

        # Verifica término da E/S
        if processo_es is not None and fatia_es == 0:
            if processo_es.tempo_cpu > 0:
                prontos.enfileirar(processo_es)
            elif processo_es.tempo_cpu == 0 and processo_es.tempo_es > 0:
                fila_es.enfileirar(processo_es)
            else:
                processo_es.encerramento_pendente = True
                prontos.enfileirar(processo_es)
            processo_es = None

    return sorted(finalizados, key=lambda x: (x[0], x[1]))

# ---------------------------
# Programa Principal
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
        tempo_es = int(partes[2])
        tempo_cpu = int(partes[3])
        prioridade = int(partes[4])
        processos.append(Processo(pid, chegada, tempo_es, tempo_cpu, prioridade))

    resultado = simular(processos)

    with open("saida.txt", "w") as f:
        for tempo, pid in resultado:
            f.write(str(tempo) + ";" + str(pid) + "\n")

    print("Simulação concluída. Arquivo 'saida.txt' gerado.")
