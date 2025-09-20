def le_processos(arquivo):
    p = []
    for l in open(arquivo):
        l = l.strip()
        if not l: continue
        a = l.split(";")
        p.append({"id": int(a[0]), "ent": int(a[1]), "io": int(a[2]),
                  "proc": int(a[3]), "prio": int(a[4]), "final": False})
    return p

def insere_por_prio(fila, proc):
    i = 0
    while i < len(fila):
        if proc["prio"] < fila[i]["prio"] or (proc["prio"] == fila[i]["prio"] and proc["id"] < fila[i]["id"]):
            break
        i += 1
    fila.insert(i, proc)

def simula(lista):
    lista = sorted(lista, key=lambda x: x["ent"])
    fila_cpu = []
    fila_io = []
    t = 0
    idx = 0
    cpu = None; left_cpu = 0
    io = None; left_io = 0
    SL = 3; IL = SL * 2
    saidas = []

    while True:
        while idx < len(lista) and lista[idx]["ent"] == t:
            insere_por_prio(fila_cpu, lista[idx]); idx += 1
        if cpu is None and fila_cpu:
            cpu = fila_cpu.pop(0)
            left_cpu = 1 if cpu["final"] else min(SL, cpu["proc"] if cpu["proc"]>0 else 1)
        if io is None and fila_io:
            io = fila_io.pop(0)
            left_io = min(IL, io["io"])

        if cpu:
            left_cpu -= 1
            if cpu["proc"] > 0:
                cpu["proc"] -= 1
        if io:
            left_io -= 1
            io["io"] -= 1

        if cpu and left_cpu == 0:
            p = cpu; cpu = None
            if p["final"]:
                saidas.append((t+1, p["id"]))
            elif p["proc"] == 0 and p["io"] == 0:
                p["final"] = True
                insere_por_prio(fila_cpu, p)
            elif p["io"] > 0:
                fila_io.append(p)
            else:
                insere_por_prio(fila_cpu, p)

        if io and left_io == 0:
            p = io; io = None
            if p["proc"] > 0:
                insere_por_prio(fila_cpu, p)
            elif p["io"] > 0:
                fila_io.append(p)
            else:
                p["final"] = True
                insere_por_prio(fila_cpu, p)
        if idx >= len(lista) and not fila_cpu and not fila_io and cpu is None and io is None:
            break

        t += 1
        if t > 1000000: break

    return sorted(saidas)

if __name__ == "__main__":
    procs = le_processos("dados.txt")
    res = simula(procs)
    with open("saida.txt", "w") as f:
        for tempo, pid in res:
            f.write(f"{tempo};{pid}\n")
    print("feito. veja saida.txt")
