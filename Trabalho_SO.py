class Processo:
    def __init__(s, idp, entrada, io, proc, prio):
        s.id, s.entrada, s.io, s.proc, s.prio = int(idp), int(entrada), int(io), int(proc), int(prio)
        s.final = False

def ler_arquivo(nome):
    lista=[]
    for linha in open(nome):
        linha=linha.strip()
        if not linha: continue
        dados=linha.split(";")
        lista.append(Processo(*dados[:5]))
    return lista

def inserir_prioridade(fila,p):
    i=0
    while i<len(fila) and (fila[i].prio<p.prio or (fila[i].prio==p.prio and fila[i].id<p.id)): i+=1
    fila.insert(i,p)

def simular(proc_iniciais):
    proc_iniciais=sorted(proc_iniciais,key=lambda x:x.entrada)
    fila_cpu=[]; fila_io=[]
    t=0; i_chegada=0
    cpu=None; rest_cpu=0
    io=None; rest_io=0
    FATIA=3; FATIA_IO=FATIA*2
    saida=[]
    while True:
        while i_chegada<len(proc_iniciais) and proc_iniciais[i_chegada].entrada==t:
            inserir_prioridade(fila_cpu, proc_iniciais[i_chegada]); i_chegada+=1
        if not cpu and fila_cpu:
            cpu=fila_cpu.pop(0)
            rest_cpu = 1 if cpu.final else min(FATIA, cpu.proc if cpu.proc>0 else 1)
        if not io and fila_io:
            io=fila_io.pop(0); rest_io = min(FATIA_IO, io.io)
        if cpu:
            rest_cpu-=1
            if cpu.proc>0: cpu.proc-=1
        if io:
            rest_io-=1; io.io-=1
        if cpu and rest_cpu==0:
            p=cpu; cpu=None
            if p.final: saida.append((t+1,p.id))
            elif p.proc==0 and p.io==0: p.final=True; inserir_prioridade(fila_cpu,p)
            elif p.io>0: fila_io.append(p)
            else: inserir_prioridade(fila_cpu,p)
        if io and rest_io==0:
            p=io; io=None
            if p.proc>0: inserir_prioridade(fila_cpu,p)
            elif p.io>0: fila_io.append(p)
            else: p.final=True; inserir_prioridade(fila_cpu,p)
        if i_chegada>=len(proc_iniciais) and not fila_cpu and not fila_io and not cpu and not io:
            break
        t+=1
        if t>1000000: break
    return saida

if __name__=="__main__":
    processos = ler_arquivo("dados.txt")
    resultado = simular(processos)
    with open("saida.txt","w") as f:
        for tempo,pid in sorted(resultado): f.write(f"{tempo};{pid}\n")
    print("Simulação concluída. Veja o arquivo saida.txt")
