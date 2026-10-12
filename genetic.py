import random
import matplotlib.pyplot as plt


class Individuo:
    def __init__(self, genes, nombre):
        self.genes = genes
        self.nombre = nombre
        self.fitness = self.calcular_fitness()

    def calcular_fitness(self):
        # Objetivo: maximizar la cantidad de unos
        return sum(self.genes)

    def copiar(self, nuevo_nombre=None):
        return Individuo(
            self.genes.copy(),
            nuevo_nombre if nuevo_nombre else self.nombre
        )

    def __str__(self):
        return (
            f"{self.nombre} | "
            f"Genes: {self.genes} | "
            f"Fitness: {self.fitness}"
        )

    def __repr__(self):
        return self.__str__()


# --------------------------------------------------
# Crear población inicial
# --------------------------------------------------

def crear_poblacion(tamano, longitud_genes):
    poblacion = []

    for i in range(tamano):
        genes = [
            random.randint(0, 1)
            for _ in range(longitud_genes)
        ]

        individuo = Individuo(genes, f"I{i + 1}")
        poblacion.append(individuo)

    return poblacion


# --------------------------------------------------
# Convertir aptitudes en probabilidades
# --------------------------------------------------

def calcular_probabilidades(poblacion):
    total_fitness = sum(
        individuo.fitness for individuo in poblacion
    )

    if total_fitness == 0:
        # Si todos tienen fitness 0, todos tienen la misma probabilidad
        probabilidad = 1 / len(poblacion)
        return [probabilidad] * len(poblacion)

    probabilidades = [
        individuo.fitness / total_fitness
        for individuo in poblacion
    ]

    return probabilidades


# --------------------------------------------------
# Selección por ruleta
# --------------------------------------------------

def rouletteSelection(population, mostrar_ruleta=True):
    if not population:
        raise ValueError("La población está vacía")

    # 1. Calcular el fitness total
    totalFitness = sum(
        individuo.fitness
        for individuo in population
    )

    # Si todos tienen fitness 0, todos tienen la misma probabilidad
    if totalFitness == 0:
        return random.choice(population)

    # 2. Convertir cada fitness en probabilidad
    probabilidades = [
        individuo.fitness / totalFitness
        for individuo in population
    ]

    # 3. Girar la ruleta
    valorRuleta = random.random()  # Valor entre 0.0 y 1.0

    acumulado = 0

    if mostrar_ruleta:
        print("\nRuleta:")

    # 4. Buscar en qué intervalo cayó el valor
    for individuo, probabilidad in zip(
        population,
        probabilidades
    ):
        limiteAnterior = acumulado
        acumulado += probabilidad

        if mostrar_ruleta:
            print(
                f"{individuo.nombre}: "
                f"{probabilidad:.2%} | "
                f"intervalo: "
                f"{limiteAnterior:.4f} - {acumulado:.4f}"
            )

        if valorRuleta <= acumulado:
            if mostrar_ruleta:
                print(
                    f"Valor obtenido: {valorRuleta:.4f}"
                )
                print(
                    f"Seleccionado: {individuo.nombre}"
                )

            return individuo

    # Protección contra errores de redondeo
    return population[-1]



# --------------------------------------------------
# Cruce de un punto
# --------------------------------------------------

def cruce(padre1, padre2):
    longitud = len(padre1.genes)

    punto = random.randint(1, longitud - 1)

    genes_hijo1 = (
        padre1.genes[:punto] +
        padre2.genes[punto:]
    )

    genes_hijo2 = (
        padre2.genes[:punto] +
        padre1.genes[punto:]
    )

    hijo1 = Individuo(genes_hijo1, "Hijo")
    hijo2 = Individuo(genes_hijo2, "Hijo")

    return hijo1, hijo2


# --------------------------------------------------
# Mutación
# --------------------------------------------------

def mutacion(individuo, probabilidad_mutacion):
    for i in range(len(individuo.genes)):
        if random.random() < probabilidad_mutacion:
            # Cambia 0 por 1 o 1 por 0
            individuo.genes[i] = 1 - individuo.genes[i]

    # Se recalcula el fitness después de mutar
    individuo.fitness = individuo.calcular_fitness()

    return individuo


# --------------------------------------------------
# Crear nueva generación
# --------------------------------------------------

def crear_nueva_generacion(
    poblacion,
    tasa_mutacion=0.01,
    elitismo=True
):
    nueva_poblacion = []

    # Conservamos al mejor individuo
    if elitismo:
        mejor = max(
            poblacion,
            key=lambda individuo: individuo.fitness
        )

        nueva_poblacion.append(
            mejor.copiar("Elite")
        )

    while len(nueva_poblacion) < len(poblacion):
        padre1 = rouletteSelection(poblacion)
        padre2 = rouletteSelection(poblacion)

        hijo1, hijo2 = cruce(padre1, padre2)

        hijo1 = mutacion(hijo1, tasa_mutacion)
        hijo2 = mutacion(hijo2, tasa_mutacion)

        nueva_poblacion.append(hijo1)

        if len(nueva_poblacion) < len(poblacion):
            nueva_poblacion.append(hijo2)

    return nueva_poblacion


# --------------------------------------------------
# Algoritmo genético completo
# --------------------------------------------------

def algoritmo_genetico(
    tamano_poblacion=10,
    longitud_genes=8,
    generaciones=30,
    tasa_mutacion=0.05
):
    poblacion = crear_poblacion(
        tamano_poblacion,
        longitud_genes
    )
    print("\nPoblación inicial:")

    for individuo in poblacion:
        print(individuo)

    mejores_fitness = []

    for generacion in range(generaciones):
        mejor = max(
            poblacion,
            key=lambda individuo: individuo.fitness
        )

        mejores_fitness.append(mejor.fitness)

        print(
            f"Generación {generacion + 1}: "
            f"mejor fitness = {mejor.fitness}, "
            f"genes = {mejor.genes}"
        )

        poblacion = crear_nueva_generacion(
            poblacion,
            tasa_mutacion,
            elitismo=True
        )

    return poblacion, mejores_fitness


# --------------------------------------------------
# Ejecutar
# --------------------------------------------------

poblacion_final, historial = algoritmo_genetico(
    tamano_poblacion=10,
    longitud_genes=8,
    generaciones=30,
    tasa_mutacion=0.05
)


# --------------------------------------------------
# Mostrar población final
# --------------------------------------------------

print("\nPoblación final:")

for individuo in poblacion_final:
    print(individuo)


# --------------------------------------------------
# Graficar la mejor aptitud de cada generación
# --------------------------------------------------

plt.plot(
    range(1, len(historial) + 1),
    historial,
    marker="o"
)

plt.title("Evolución de la mejor aptitud")
plt.xlabel("Generación")
plt.ylabel("Mejor fitness")
plt.grid(True)
plt.show()

