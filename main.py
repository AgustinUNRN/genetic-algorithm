import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--selection",
    choices=["roulette", "ranking"],
    help="Método de selección",
)
parser.add_argument(
    "--stage",
    choices=["setup", "selection", "crossover", "mutation", "replacement", "summary"],
    help="Etapa que querés mostrar",
)

args = parser.parse_args()

# Si solo pasás --selection, muestra ese método.
# Si no pasás argumentos, muestra setup.
stage = args.stage or ("selection" if args.selection else "setup")

if stage == "selection":
    if not args.selection:
        parser.error("Para la etapa selection, indicá --selection roulette o --selection ranking")
    print(f"Etapa: selección por {args.selection}")
else:
    print(f"Etapa: {stage}")
