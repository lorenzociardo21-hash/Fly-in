from src.classi import Drone, Hub, Map, Connection
from src.parsing import MapParser

def main() -> None:
    parser: MapParser = MapParser("maps/easy/01_linear_path.txt")
    mapp: Map = parser.parse_and_create_map()
    print(f"Hub di partenza: {mapp.start_hub}")
    print(f"Numero di droni: {mapp.n_drones}")
    print(f"Hub totali trovati: {len(mapp.hub_dict)}")

if __name__ == "__main__":
    main()