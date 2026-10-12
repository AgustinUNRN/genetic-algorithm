import random
import argparse
import copy
import time

# --- Configuración Básica ---
TAMANO_POBLACION = 6
LONGITUD_GENES = 8
GENERACIONES = 4
TAMANO_TORNEO = 3
RETARDO = 0.2  # Segundos de pausa para los sleeps

def generar_individuo():
    return [random.randint(0, 1) for _ in range(LONGITUD_GENES)]

def calcular_aptitud(individuo):
    return sum(individuo)

def generar_poblacion_inicial():
    poblacion = [{"genes": generar_individuo(), "aptitud": 0} for _ in range(TAMANO_POBLACION)]
    for ind in poblacion:
        ind["aptitud"] = calcular_aptitud(ind["genes"])
    return poblacion

# --- Tablas de Probabilidad (Ruleta - Ranking) ---

def mostrar_tabla_probabilidades(poblacion, metodo):
    if metodo == "ruleta":
        pob_ordenada = sorted(poblacion, key=lambda x: x["aptitud"], reverse=True)
        total_aptitud = sum(ind["aptitud"] for ind in poblacion)
        
        if total_aptitud == 0:
            print("  [!] Todas las aptitudes son 0. Todos tienen igual probabilidad.")
            return
            
        print("  --- TABLA DE PROBABILIDADES (RULETA) ---")
        print("  Pos | Genes    | Aptitud | Probabilidad | Acumulada | Rango Pick")
        print("  " + "-"*68)
        acumulada = 0.0
        for i, ind in enumerate(pob_ordenada):
            prob = (ind["aptitud"] / total_aptitud) * 100
            inicio_rango = acumulada
            acumulada += prob
            fin_rango = acumulada
            
            genes_str = "".join(map(str, ind["genes"]))
            rango_str = f"[{inicio_rango:5.1f}% - {fin_rango:5.1f}%]"
            
            print(f"  {i+1:3} | {genes_str} | {ind['aptitud']:7} | {prob:11.1f}% | {acumulada:8.1f}% | {rango_str}")
            time.sleep(RETARDO)
        print("")

#  --- TABLA DE PROBABILIDADES (RULETA) ---
#  Pos | Genes    | Aptitud | Probabilidad | Acumulada | Rango Pick
#  --------------------------------------------------------------------
#    1 | 11111000 |       5 |        21.7% |     21.7% | [  0.0% -  21.7%]
#    2 | 11101010 |       5 |        21.7% |     43.5% | [ 21.7% -  43.5%]
#    3 | 01001011 |       4 |        17.4% |     60.9% | [ 43.5% -  60.9%]
#    4 | 01100011 |       4 |        17.4% |     78.3% | [ 60.9% -  78.3%]
#    5 | 10001001 |       3 |        13.0% |     91.3% | [ 78.3% -  91.3%]
#    6 | 00110000 |       2 |         8.7% |    100.0% | [ 91.3% - 100.0%]


    elif metodo == "ranking":
        pob_ordenada = sorted(poblacion, key=lambda x: x["aptitud"])
        total_rangos = sum(range(1, len(poblacion) + 1))
        
        print("  --- TABLA DE PROBABILIDADES (RANKING) ---")
        print("  Pos | Genes    | Aptitud | Rango | Probabilidad | Acumulada | Rango Pick")
        print("  " + "-"*76)
        acumulada = 0.0
        for i, ind in enumerate(pob_ordenada):
            rango = i + 1
            prob = (rango / total_rangos) * 100
            inicio_rango = acumulada
            acumulada += prob
            fin_rango = acumulada
            
            genes_str = "".join(map(str, ind["genes"]))
            rango_str = f"[{inicio_rango:5.1f}% - {fin_rango:5.1f}%]"
            
            # Mostramos la posición invertida para que el mejor se vea como Pos 1
            posicion_visual = len(poblacion) - i
            print(f"  {posicion_visual:3} | {genes_str} | {ind['aptitud']:7} | {rango:5} | {prob:11.1f}% | {acumulada:8.1f}% | {rango_str}")
            time.sleep(RETARDO)
        print("")

#--- TABLA DE PROBABILIDADES (RANKING) ---
#  Pos | Genes    | Aptitud | Rango | Probabilidad | Acumulada | Rango Pick
#  ----------------------------------------------------------------------------
#    6 | 01000101 |       3 |     1 |         4.8% |      4.8% | [  0.0% -   4.8%]
#    5 | 11010000 |       3 |     2 |         9.5% |     14.3% | [  4.8% -  14.3%]
#    4 | 11010001 |       4 |     3 |        14.3% |     28.6% | [ 14.3% -  28.6%]
#    3 | 01111010 |       5 |     4 |        19.0% |     47.6% | [ 28.6% -  47.6%]
#    2 | 11011001 |       5 |     5 |        23.8% |     71.4% | [ 47.6% -  71.4%]
#    1 | 10111111 |       7 |     6 |        28.6% |    100.0% | [ 71.4% - 100.0%]
#        

# --- Algoritmos de Selección ---

def seleccion_ruleta(poblacion):
    pob_ordenada = sorted(poblacion, key=lambda x: x["aptitud"], reverse=True)
    total_aptitud = sum(ind["aptitud"] for ind in pob_ordenada)
    
    if total_aptitud == 0:
        elegido = random.choice(pob_ordenada)
        print(f"      -> Ruleta (al azar por aptitud 0): Elegido individuo con aptitud {elegido['aptitud']}")
        return elegido
        
    pick = random.uniform(0, total_aptitud)
    acumulado = 0
    for ind in pob_ordenada:
        inicio = acumulado
        acumulado += ind["aptitud"]
        if acumulado >= pick:
            pick_pct = (pick / total_aptitud) * 100
            inicio_pct = (inicio / total_aptitud) * 100
            fin_pct = (acumulado / total_aptitud) * 100
            print(f"      -> Ruleta: Pick cayó en {pick_pct:.1f}%. Elegido: Genes {ind['genes']} Aptitud {ind['aptitud']}")
            return ind

def seleccion_torneo(poblacion):
    print(f"      -> Iniciando Torneo (Seleccionando K={TAMANO_TORNEO} al azar):")
    participantes = random.sample(poblacion, TAMANO_TORNEO)
    
    for i, p in enumerate(participantes):
        genes_str = "".join(map(str, p["genes"]))
        print(f"         Combatiente {i+1}: Genes {genes_str} | Aptitud: {p['aptitud']}")
        time.sleep(RETARDO / 2)
        
    ganador = max(participantes, key=lambda x: x["aptitud"])
    print(f"      -> ¡Ganador del Torneo! Elegido individuo con Aptitud {ganador['aptitud']}")
    return ganador

def seleccion_ranking(poblacion):
    pob_ordenada = sorted(poblacion, key=lambda x: x["aptitud"])
    total_rangos = sum(range(1, len(pob_ordenada) + 1))
    pick = random.uniform(0, total_rangos)
    
    acumulado = 0
    for i, ind in enumerate(pob_ordenada):
        inicio = acumulado
        acumulado += (i + 1)
        if acumulado >= pick:
            pick_pct = (pick / total_rangos) * 100
            inicio_pct = (inicio / total_rangos) * 100
            fin_pct = (acumulado / total_rangos) * 100
            print(f"      -> Ranking: Pick cayó en {pick_pct:.1f}%. Elegido: Genes {ind['genes']} Aptitud {ind['aptitud']}")
            return ind

# --- Operadores Genéticos ---

def cruzamiento(padre1, padre2):
    punto_corte = random.randint(1, LONGITUD_GENES - 1)
    hijo1_genes = padre1["genes"][:punto_corte] + padre2["genes"][punto_corte:]
    hijo2_genes = padre2["genes"][:punto_corte] + padre1["genes"][punto_corte:]
    
    print(f"      -> Punto de corte: índice {punto_corte}")
    print(f"         Padre 1: {padre1['genes'][:punto_corte]} | {padre1['genes'][punto_corte:]}")
    print(f"         Padre 2: {padre2['genes'][:punto_corte]} | {padre2['genes'][punto_corte:]}")
    print(f"         Hijo 1 : {hijo1_genes}")
    print(f"         Hijo 2 : {hijo2_genes}")
        
    return {"genes": hijo1_genes, "aptitud": 0}, {"genes": hijo2_genes, "aptitud": 0}

def mutacion(individuo, num_hijo, prob_mutacion=0.1):
    mutado = False
    for i in range(LONGITUD_GENES):
        if random.random() < prob_mutacion:
            individuo["genes"][i] = 1 - individuo["genes"][i]
            print(f"      -> ¡Hijo {num_hijo} mutó! Gen invertido en índice {i}. Nuevo: {individuo['genes']}")
            mutado = True
            time.sleep(RETARDO / 2)
    if not mutado:
        print(f"      -> Hijo {num_hijo} sin mutaciones.")

# --- Ciclo Principal ---

def ejecutar_algoritmo_genetico(poblacion_inicial, metodo_seleccion):
    print(f"\n{'='*75}")
    print(f" INICIANDO EVOLUCIÓN - MÉTODO DE SELECCIÓN: {metodo_seleccion.upper()}")
    print(f"{'='*75}")
    time.sleep(RETARDO)
    
    funciones_seleccion = {
        "ruleta": seleccion_ruleta,
        "torneo": seleccion_torneo,
        "ranking": seleccion_ranking
    }
    
    funcion_seleccionar = funciones_seleccion[metodo_seleccion]
    poblacion = copy.deepcopy(poblacion_inicial)
    
    for generacion in range(GENERACIONES):
        print(f"\n\n{'='*25} GENERACIÓN {generacion + 1} {'='*25}")
        mejor_ind = max(poblacion, key=lambda x: x["aptitud"])
        print(f"Mejor individuo actual -> Aptitud: {mejor_ind['aptitud']} | Genes: {mejor_ind['genes']}\n")
        time.sleep(RETARDO)
        
        if metodo_seleccion in ["ruleta", "ranking"]:
            mostrar_tabla_probabilidades(poblacion, metodo_seleccion)
            time.sleep(RETARDO)
        
        nueva_poblacion = []
        contador_pares = 1
        
        while len(nueva_poblacion) < TAMANO_POBLACION:
            print(f"  [+] Creando par de hijos {contador_pares} de {TAMANO_POBLACION//2}:")
            
            print("    [SELECCIÓN PADRE 1]")
            time.sleep(RETARDO / 2)
            padre1 = funcion_seleccionar(poblacion)
            time.sleep(RETARDO)
            
            print("\n    [SELECCIÓN PADRE 2]")
            time.sleep(RETARDO / 2)
            padre2 = funcion_seleccionar(poblacion)
            time.sleep(RETARDO)
            
            print("\n    [CRUZAMIENTO]")
            time.sleep(RETARDO / 2)
            hijo1, hijo2 = cruzamiento(padre1, padre2)
            time.sleep(RETARDO)
            
            print("\n    [MUTACIÓN]")
            time.sleep(RETARDO / 2)
            mutacion(hijo1, num_hijo=1)
            mutacion(hijo2, num_hijo=2)
            
            hijo1["aptitud"] = calcular_aptitud(hijo1["genes"])
            hijo2["aptitud"] = calcular_aptitud(hijo2["genes"])
            
            nueva_poblacion.extend([hijo1, hijo2])
            contador_pares += 1
            print("-" * 50)
            time.sleep(RETARDO)
            
        poblacion = nueva_poblacion

    print(f"\n\n{'='*75}")
    print(" ALGORITMO FINALIZADO - ESTADO DE LA POBLACIÓN FINAL")
    print(f"{'='*75}")
    time.sleep(RETARDO)

    poblacion_ordenada = sorted(poblacion, key=lambda x: x["aptitud"], reverse=True)
    for i, ind in enumerate(poblacion_ordenada):
        print(f"  Individuo {i+1:2}: Aptitud {ind['aptitud']:2} | Genes: {ind['genes']}")
        time.sleep(RETARDO)

    mejor_final = poblacion_ordenada[0]
    print("\n" + "*"*75)
    print(f" MEJOR INDIVIDUO ENCONTRADO: Aptitud {mejor_final['aptitud']} | Genes: {mejor_final['genes']}")
    print("*"*75 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Algoritmos Genéticos")
    parser.add_argument(
        '-s', '--seleccion', 
        choices=['ruleta', 'torneo', 'ranking'], 
        help="Método de selección a utilizar"
    )
    args = parser.parse_args()

    poblacion_base = generar_poblacion_inicial()
    
    print("=== POBLACIÓN INICIAL GLOBAL ===")
    for i, ind in enumerate(poblacion_base):
        print(f"  Individuo {i+1:2}: Aptitud {ind['aptitud']:2} | Genes: {ind['genes']}")
    
    if args.seleccion:
        ejecutar_algoritmo_genetico(poblacion_base, args.seleccion)
    else:
        print("\nNo se especificó un método por terminal.")
        while True:
            opcion = input("Elige el método de selección (ruleta, torneo, ranking) o 'salir': ").lower().strip()
            if opcion == 'salir':
                break
            if opcion in ['ruleta', 'torneo', 'ranking']:
                ejecutar_algoritmo_genetico(poblacion_base, opcion)
            else:
                print("Opción no válida. Por favor, intenta de nuevo.")