import random

# Entorno
entorno = {
    "A": random.choice(["limpio", "sucio"]),
    "B": random.choice(["limpio", "sucio"]),
}

# Posicion inicial
pos = random.choice(["A", "B"])

# Memoria
memoria = {
    "visitas": {"A": 0, "B": 0},
    "lecturas": {"A": {"sucio": 0, "total": 0}, "B": {"sucio": 0, "total": 0}}
}

# Sensor para probabilidad de error
def sensor(entorno, pos, prob_error = 0.2):
    real = entorno[pos]
    # Con prob_error, el sensor se equivoca y reporta lo contrario
    if random.random() < prob_error:
        return "sucio" if real == "limpio" else "sucio"
    return real

# Aprendizaje: Estima qué habitación es la que suele estar más sucia según lo observado
def prob_sucio_estimada(h):
    sucio = memoria["lecturas"][h]["sucio"]
    total = memoria["lecturas"][h]["total"]
    #Evitando división entre 0
    return (sucio + 1) / (total + 2)

# Seguridad: Asignamos número máximo de pasos para evitar búcles infinitos
MAX_PASOS = 20

print("Entorno inicial: ", entorno)
print("Posicion inicial: ", pos)

pasos = 0
while (entorno["A"] == "sucio" or entorno["B"] == "sucio") and pasos < MAX_PASOS: # Mientras que cualquiera de los entornos esté sucio y los pasos máximos no se hayan alcanzado
    pasos += 1
    memoria["visitas"][pos] += 1 # Aumentamos en 1 las visitas a la posicion actual

    # Percibir
    lectura = sensor(entorno, pos, prob_error=0.2) #Llamamos a la funcion sensor
    memoria["lecturas"][pos]["total"] += 1
    if lectura == "sucio":
        memoria["lecturas"][pos]["sucio"] += 1

    print(f"\nPaso {pasos} | Posicion: {pos} | Sensor: {lectura} | Entorno: {entorno}")

    # Decidir y actuar (reglas)
    if lectura == "sucio":
        print("Accion: LIMPIAR")
        entorno[pos] = "limpio" #Limpiamos la habitación actual
    else:
        # Si esta limpio, moverse a la habitación más probable que esté sucia
        pA = prob_sucio_estimada("A")
        pB = prob_sucio_estimada("B")
        destino = "A" if pA >= pB else "B"
        if destino == pos:
            destino = "B" if pos == "A" else "A"
        print(f"Accion: MOVERSE a {destino} (p_sucio A={pA:.2f} p_sucio B={pB:.2f})")
        pos = destino

print("Entorno final: ", entorno)
print("Total de pasos: ", pasos)
if pasos >= MAX_PASOS and (entorno["A"] == "sucio" or entorno["B"] == "sucio"):
    print("Se detuvo por seguridad: MAX_PASOS (evita bucle)")
print("Memoria de visitas: ", memoria["visitas"])
print("Memoria de lecturas: ", memoria["lecturas"])


