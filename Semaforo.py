import simpy

# Simulación del semáforo
def semaforo(env, verde, amarillo, rojo, tiempo_vehiculo, cantidad_vehiculos, resultado):
    while env.now < 70:
        
        # --- LUZ VERDE ---
        print(f"[{env.now:.1f} s] SEMÁFORO → VERDE")
        tiempo = 0
        
        # Los vehículos pasan uno por uno
        while tiempo + tiempo_vehiculo <= verde:
            if env.now + tiempo_vehiculo > 70:
                break
            
            yield env.timeout(tiempo_vehiculo)
            
            # Contar vehículo que pasó
            if resultado["pasaron"] < cantidad_vehiculos:
                resultado["pasaron"] += 1
                print(f"[{env.now:.1f} s] Vehículo {resultado['pasaron']} pasó")
                
            tiempo += tiempo_vehiculo
            
        # Esperar el tiempo exacto que le sobre a la luz verde
        tiempo_sobrante_verde = verde - tiempo
        if tiempo_sobrante_verde > 0 and env.now < 70:
            yield env.timeout(tiempo_sobrante_verde)


        # --- LUZ AMARILLA ---
        if env.now < 70:
            print(f"[{env.now:.1f} s] SEMÁFORO → AMARILLO")
            tiempo = 0
            
            # Los vehículos también pasan en amarillo
            while tiempo + tiempo_vehiculo <= amarillo:
                if env.now + tiempo_vehiculo > 70:
                    break
                
                yield env.timeout(tiempo_vehiculo)
                
                # Contar vehículo que pasó
                if resultado["pasaron"] < cantidad_vehiculos:
                    resultado["pasaron"] += 1
                    print(f"[{env.now:.1f} s] Vehículo {resultado['pasaron']} pasó (en amarillo)")
                    
                tiempo += tiempo_vehiculo
                
            # Esperar el tiempo exacto que le sobre a la luz amarilla
            tiempo_sobrante_amarillo = amarillo - tiempo
            if tiempo_sobrante_amarillo > 0 and env.now < 70:
                yield env.timeout(tiempo_sobrante_amarillo)


        # --- LUZ ROJA ---
        if env.now < 70:
            print(f"[{env.now:.1f} s] SEMÁFORO → ROJO")
            # En rojo nadie pasa, solo transcurre el tiempo completo
            yield env.timeout(rojo)


# ===== DATOS DE ENTRADA =====
print("===== SIMULACIÓN DE SEMÁFORO =====")

cantidad_vehiculos = int(input("Cantidad de vehículos: "))
verde = float(input("Duración del VERDE (segundos): "))
amarillo = float(input("Duración del AMARILLO (segundos): "))
rojo = float(input("Duración del ROJO (segundos): "))
tiempo_vehiculo = float(input("Tiempo que tarda cada vehículo en pasar (segundos): "))

# Resultado
resultado = { "pasaron": 0 }

# Crear entorno de simulación
env = simpy.Environment()

# Iniciar proceso del semáforo
env.process(semaforo(env, verde, amarillo, rojo, tiempo_vehiculo, cantidad_vehiculos, resultado))

print("\nIniciando simulación...\n")

# Simulación de 70 segundos
env.run(until=70)

# Vehículos que no alcanzaron a pasar
no_pasaron = cantidad_vehiculos - resultado["pasaron"]

# ===== RESULTADOS =====
print("\n===== RESULTADOS =====")
print(f"Vehículos disponibles: {cantidad_vehiculos}")
print(f"Vehículos que pasaron: {resultado['pasaron']}")
print(f"Vehículos que NO pasaron: {no_pasaron}")
print(f"Tiempo de simulación: 70 segundos")