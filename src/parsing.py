from src.classi import Drone, Hub, Map, Connection
import re
from typing import Match


class MapParser:
    def __init__(self, percorso_file: str):
        self.percorso_file: str = percorso_file
        self.hub_dict: dict[str, Hub] = {}
        self.connection_dict: dict[str, Connection] = {}
        self.list_drone: list[Drone] = []
        self.start_hub_name: str = ""
        self.end_hub_name: str = ""

    def parse_and_create_map(self) -> Map:
        list_namehub: list[str] = []
        start = 0
        end = 0
        try:
            with open(self.percorso_file, "r") as file:
                for i, riga in enumerate(file, start=1):
                    riga_pulita: str = riga.strip()
                    if not riga_pulita or riga_pulita.startswith("#"):
                        continue

                    elif riga_pulita.startswith("nb_drones:"):
                        pattern = r"^nb_drones:\s+(\d+)"
                        risultato = re.match(pattern, riga_pulita)
                        if risultato:
                            n_drones = int(risultato.group(1))
                            if n_drones == 0:
                                raise ValueError(
                                    "Erroree, non puoi mettere 0 droni"
                                )
                            for x in range(n_drones):
                                nuovo_drone = Drone(name=f'd{x + 1}')
                                self.list_drone.append(nuovo_drone)
                        else:
                            raise ValueError(
                                f"Errore sintassi nb_drones a riga {i}"
                            )

                    elif riga_pulita.startswith(
                        ("hub:", "start_hub:", "end_hub:")
                    ) and n_drones:
                        if riga_pulita.startswith("start_hub:"):
                            start += 1
                        if riga_pulita.startswith("end_hub:"):
                            end += 1
                        pattern = (
                            r"^(hub|start_hub|end_hub):\s+(\w+)\s+(\d+)"
                            r"\s+(\d+)\s*(?:\s*\[(.*?)\])?"
                        )
                        risultato_hub: Match[str] | None = re.match(
                            pattern, riga_pulita
                        )

                        if risultato_hub:
                            tipo_hub = risultato_hub.group(1)
                            nome_hub = risultato_hub.group(2)
                            coord_x = int(risultato_hub.group(3))
                            coord_y = int(risultato_hub.group(4))
                            t_zone: str = "normal"
                            t_color: str = ""
                            t_max_drones: int = 1
                            list_namehub.append(nome_hub)
                            if risultato_hub.group(5):
                                rigaa: str = risultato_hub.group(5).strip()
                                riga_splittata: list[str] = rigaa.split()
                                for param in riga_splittata:
                                    riga_split: list[str] = param.split('=')
                                    if len(riga_split) != 2:
                                        raise ValueError(
                                            f"Errore riga {i} in '{param}'"
                                        )
                                    chiave = riga_split[0]
                                    valore = riga_split[1]

                                    if chiave == 'zone':
                                        zone_val = [
                                            "normal", "blocked",
                                            "restricted", "priority"
                                        ]
                                        if valore in zone_val:
                                            t_zone = valore
                                        else:
                                            raise ValueError(
                                                f"Riga {i}: zona errata"
                                            )
                                    elif chiave == 'color':
                                        t_color = valore
                                    elif chiave == 'max_drones':
                                        try:
                                            num: int = int(valore)
                                            if num > 0:
                                                t_max_drones = num
                                            else:
                                                raise ValueError(
                                                    f"Riga {i}: d. <= 0"
                                                )
                                        except ValueError:
                                            raise ValueError(
                                                f"Riga {i}: non numero, \
o sbagliato"
                                            )
                                    else:
                                        raise ValueError(
                                            f"Riga {i}: '{chiave}' ignoto"
                                        )

                            nuovo_hub = Hub(
                                name=nome_hub,
                                cord=(coord_x, coord_y),
                                typezone=t_zone,
                                color=t_color,
                                max_drones=t_max_drones
                            )
                            self.hub_dict[nome_hub] = nuovo_hub

                            if tipo_hub == "start_hub":
                                self.start_hub_name = nome_hub
                            elif tipo_hub == "end_hub":
                                self.end_hub_name = nome_hub
                        else:
                            raise ValueError(f"Sintassi hub a riga {i}")

                    elif riga_pulita.startswith(
                        "connection:") and n_drones:
                        pattern_conn = (
                            r"^connection:\s+(\w+)\-(\w+)"
                            r"\s*(?:\s*\[(.*?)\])?"
                        )
                        risultato_conn: Match[str] | None = re.match(
                            pattern_conn, riga_pulita
                        )
                        if risultato_conn:
                            hub_a_name: str = risultato_conn.group(1)
                            hub_b_name: str = risultato_conn.group(2)
                            if hub_a_name == hub_b_name:
                                raise ValueError(
                                    "Mi spieghi che connessione sarebbe,"
                                    "una tra due punti uguali??? SCEMO!\n"
                                    f"Controlla riga {i}")
                            maax_capacity: int = 1

                            if risultato_conn.group(3):
                                r_conn: str = risultato_conn.group(3).strip()
                                if r_conn.startswith("max_link_capacity="):
                                    r_split: list[str] = r_conn.split("=")
                                    maax_capacity = int(r_split[1])
                                else:
                                    raise ValueError(
                                        f"Errore connection riga {i}"
                                    )
                            new_connection: Connection = Connection(
                                hub_a=hub_a_name,
                                hub_b=hub_b_name,
                                max_capacity=maax_capacity
                            )
                            nome_c = new_connection.name_connection
                            self.connection_dict[nome_c] = new_connection
                        else:
                            raise ValueError(f"Sintassi conn a riga {i}")

                    else:
                        raise ValueError(f"Riga sconosciuta a riga {i}")

        except ValueError as e:
            print(e)
            exit(1)
        except FileNotFoundError as e:
            print(f"Erroreee hai messo il file nel posto sbagliato: {e}")
            exit(1)
        except UnboundLocalError:
            print(f"A bellooo, la prima riga del file "
                  "deve essere i numero di droni!")
            exit(1)
        if self.start_hub_name == "":
            print("Eiii, manca la partenzaaaa!")
            exit(1)

        if self.end_hub_name == "":
            print("Eiii, manca la fineee!")
            exit(1)

        if start != 1:
            print("Eiii, ci deve essere UNA sola partenza")
            exit(1)

        if end != 1:
            print("Eiii, ci deve essere UNA sola fineeee")
            exit(1)

        if not self.list_drone:
            print("Eiii, hai dimenticato di mettere i numeri di droniii!")
            exit(1)

        for nome_c, conn in self.connection_dict.items():
            if conn.hub_a not in self.hub_dict:
                print(f"Eiii, non esiste hub {conn.hub_a}, \
allora perche la scivi in '{nome_c}'")
                exit(1)
            if conn.hub_b not in self.hub_dict:
                print(f"Eiii, non esiste hub {conn.hub_b}, \
allora perche la scivi in '{nome_c}'")
                exit(1)

        for x in range(len(list_namehub)):
            for y in range(x + 1, len(list_namehub)):
                if list_namehub[x] == list_namehub[y]:
                    print("Eii, hai scritto piu volte lo stesso nome!"
                          f" {list_namehub[x]}")
                    exit(1)
        list_connec: list[list[str]] = []
        for _, conne in self.connection_dict.items():
            list_connec.append([conne.hub_a, conne.hub_b])
        risultato = [sorted(piccola_lista) for piccola_lista in list_connec]
        if  len(risultato) != len(set(tuple(x) for x in risultato)):
            print('Ei, non possono esserci due connessioni uguali sciocchino')
            exit(1)
        return Map(
            hub_dict=self.hub_dict,
            connection_dict=self.connection_dict,
            start_hub=self.start_hub_name,
            end_hub=self.end_hub_name,
            drones=self.list_drone
        )
