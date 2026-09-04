import simpy
import random

# simulacion del semaforo
def semaforo(env, verde, amarillo, rojo, tiempo_vehiculo_base, cantidad_vehiculos, resultado):
    while env.now < 70:
        
        # --- luz verde ---
        print(f"[{env.now:.1f} s] SEMAFORO -> VERDE")
        tiempo = 0
        
        # los vehiculos pasan uno por uno
        while True:
            # aplicacion de random: genera un tiempo de cruce aleatorio para este vehiculo
            # (varia entre un 20% menos y un 20% mas del tiempo base)
            tiempo_real_cruce = random.uniform(tiempo_vehiculo_base * 0.8, tiempo_vehiculo_base * 1.2)
            
            if tiempo + tiempo_real_cruce > verde or env.now + tiempo_real_cruce > 70:
                break
            
            yield env.timeout(tiempo_real_cruce)
            
            # contar vehiculo que paso
            if resultado["pasaron"] < cantidad_vehiculos:
                resultado["pasaron"] += 1
                print(f"[{env.now:.1f} s] Vehiculo {resultado['pasaron']} paso (tardo {tiempo_real_cruce:.1f} s)")
                
            tiempo += tiempo_real_cruce
            
        # esperar el tiempo exacto que le sobre a la luz verde
        tiempo_sobrante_verde = verde - tiempo
        if tiempo_sobrante_verde > 0 and env.now < 70:
            yield env.timeout(tiempo_sobrante_verde)


        # --- luz amarilla ---
        if env.now < 70:
            print(f"[{env.now:.1f} s] SEMAFORO -> AMARILLO")
            tiempo = 0
            
            # los vehiculos tambien pasan en amarillo
            while True:
                # aplicacion de random tambien para los cruces en amarillo
                tiempo_real_cruce = random.uniform(tiempo_vehiculo_base * 0.8, tiempo_vehiculo_base * 1.2)
                
                if tiempo + tiempo_real_cruce > amarillo or env.now + tiempo_real_cruce > 70:
                    break
                
                yield env.timeout(tiempo_real_cruce)
                
                # contar vehiculo que paso
                if resultado["pasaron"] < cantidad_vehiculos:
                    resultado["pasaron"] += 1
                    print(f"[{env.now:.1f} s] Vehiculo {resultado['pasaron']} paso en amarillo (tardo {tiempo_real_cruce:.1f} s)")
                    
                tiempo += tiempo_real_cruce
                
            # esperar el tiempo exacto que le sobre a la luz amarilla
            tiempo_sobrante_amarillo = amarillo - tiempo
            if tiempo_sobrante_amarillo > 0 and env.now < 70:
                yield env.timeout(tiempo_sobrante_amarillo)


        # --- luz roja ---
        if env.now < 70:
            print(f"[{env.now:.1f} s] SEMAFORO -> ROJO")
            # en rojo nadie pasa, solo transcurre el tiempo completo
            yield env.timeout(rojo)


# ===== datos de entrada =====
print("===== SIMULACION DE SEMAFORO =====")

cantidad_vehiculos = int(input("Cantidad de vehiculos en la fila: "))
verde = float(input("Duracion del VERDE (segundos): "))
amarillo = float(input("Duracion del AMARILLO (segundos): "))
rojo = float(input("Duracion del ROJO (segundos): "))
tiempo_vehiculo_base = float(input("Tiempo PROMEDIO que tarda un vehiculo en pasar (segundos): "))

# resultado
resultado = { "pasaron": 0 }

# crear entorno de simulacion
env = simpy.Environment()

# iniciar proceso del semaforo
env.process(semaforo(env, verde, amarillo, rojo, tiempo_vehiculo_base, cantidad_vehiculos, resultado))

print("\nIniciando simulacion...\n")

# simulacion de 70 segundos
env.run(until=70)

# vehiculos que no alcanzaron a pasar
no_pasaron = cantidad_vehiculos - resultado["pasaron"]

# ===== resultados =====
print("\n===== RESULTADOS =====")
print(f"Vehiculos en la fila inicial: {cantidad_vehiculos}")
print(f"Vehiculos que lograron pasar: {resultado['pasaron']}")
print(f"Vehiculos que NO pasaron (se quedaron esperando): {no_pasaron}")
print(f"Tiempo de simulacion transcurrido: 70 segundos")
