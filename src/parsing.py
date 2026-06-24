import re
from src.classi import Map, Drone, Connection, Hub

# testo = "hub: roof1 3  4 "
# pattern = r"^hub:\s+(\w+)\s+(\d+)\s+(\d+)"

# risultato = re.match(pattern, testo)

# if risultato:
#     nome = risultato.group(1)
#     x = risultato.group(2)
#     y = risultato.group(3)
    
#     print(f"Metodo B - Nome: {nome}, X: {x}, Y: {y}")

def parser(percorso_file: str) -> list[dict]:
    lista_con_tutto: list[dict] = []
    try:
        with open(percorso_file, "r") as file:
            for i, riga in enumerate(file, start=1):
                riga_pulita: str = riga.strip()
                if riga_pulita.startswith("#"):
                    continue
                elif riga_pulita.startswith("start_hub:"):
                    pass
                elif riga_pulita.startswith("end_hub:"):
                    pass
                elif riga_pulita.startswith("nb_drones:"):
                    n_drone: dict[str, int] = {}
                    pattern = r"^nb_drones:\s+(\d+)"
                    risultato = re.match(pattern,  riga_pulita)
                    if risultato:
                        n_drone["drones"] = int(risultato.group(1))
                    else:
                        raise ValueError(f"Error: qualcosa non va a riga {i}")
                    lista_con_tutto.append(n_drone)
                elif riga_pulita.startswith("hub:"):
                    pass
                elif riga_pulita.startswith("connection:"):
                    pass
                else:
                    raise ValueError(f"Error: qualcosa non va a riga {i}")

    except ValueError as e:
        print(e)
        exit()