# Algoritmos Genéticos con Canonical Workshop 🧬

Este proyecto es una herramienta interactiva diseñada para ejecutarse dentro de **Canonical Workshop** (un entorno contenedorizado basado en Ubuntu). Su objetivo principal es visualizar paso a paso cómo funcionan los Algoritmos Genéticos, con un enfoque especial en los diferentes métodos de selección de individuos.

## 🎯 El Problema: OneMax

El algoritmo resuelve un problema clásico y sencillo llamado **OneMax**.
El objetivo es maximizar la cantidad de unos (`1`) en una cadena binaria (cromosoma) de una longitud determinada.

* **Genes:** Cada individuo tiene 8 genes compuestos por `0`s y `1`s (ej. `[0, 1, 1, 0, 0, 1, 1, 1]`).
* **Aptitud (Fitness):** Se calcula sumando todos los genes. El individuo perfecto tendría genes puros de `1`s y su aptitud sería `8`.

## 🚀 Características del Proyecto

1. **Población Base Constante:** Al iniciar el script, se genera una población inicial que se mantiene igual para todas las pruebas. Esto permite comparar de manera justa cómo cada algoritmo procesa los mismos datos.
2. **Tablas de Probabilidad:** Para Ruleta y Ranking, se imprimen tablas detalladas mostrando el porcentaje de probabilidad y el "Rango Pick".
3. **Paso a Paso Animado:** El script incluye pausas y describe en detalle cada fase: Selección (Padre 1 y 2), Cruzamiento (punto de corte) y Mutación (gen por gen).

## 📂 Estructura del Proyecto

```text
.
├── algoritmo_genetico.py            # Código principal del algoritmo
└── .workshop/
    └── algoritmos-geneticos.yaml    # Configuración del entorno Canonical Workshop
```

## 🛠️ Cómo Ejecutar en Canonical Workshop

Utiliza los siguientes comandos en tu terminal anfitriona para interactuar con el contenedor de Canonical Workshop:

### Gestión del Entorno

* **Lanzar el workshop:**
  ```bash
  workshop launch
  ```
* **Detener el workshop:**
  ```bash
  workshop stop algoritmos-geneticos
  ```

### Ejecución de los Algoritmos (Acciones)

Puedes ejecutar el proyecto de forma interactiva o llamar directamente a un método de selección utilizando las acciones definidas en el entorno:

* **Modo Interactivo (Menú):**
  Muestra la población y te pide ingresar el método por teclado.
  ```bash
  workshop run algoritmos-geneticos inicio
  ```
  *(También puedes usar simplemente `workshop run algoritmos-geneticos`)*

* **Ejecutar Selección por Ruleta:**
  ```bash
  workshop run algoritmos-geneticos ruleta
  ```

* **Ejecutar Selección por Ranking:**
  ```bash
  workshop run algoritmos-geneticos ranking
  ```

* **Ejecutar Selección por Torneo:**
  ```bash
  workshop run algoritmos-geneticos torneo
  ```

## 🧠 Fases del Algoritmo Explicadas

### 1. Métodos de Selección
* **Ruleta:** Cada individuo recibe un trozo de la ruleta proporcional a su aptitud (fitness).
* **Ranking:** Los individuos se ordenan del peor al mejor. La ruleta se arma en base a esta *posición* (1, 2, 3...) y no en su aptitud real, evitando que los "superdotados" acaparen todas las selecciones.
* **Torneo:** Se seleccionan *K* combatientes al azar de la población. Compiten entre ellos y el de mayor aptitud gana el derecho a ser padre.

### 2. Cruzamiento (Crossover)
Se utiliza el método de **Cruce de un punto**. Se elige un punto al azar en el cromosoma, se cortan los genes de ambos padres en ese punto y se intercambian las mitades para generar dos nuevos hijos.

### 3. Mutación
Ocurre inmediatamente después de que nacen los hijos. El algoritmo evalúa **gen por gen** lanzando un dado virtual (10% de probabilidad por defecto). Si el dado acierta, ese gen específico se invierte (de `0` a `1`, o viceversa).