

class Hub:
    def __init__(self, name: str, cord: tuple[int, int],
                 typezone: str = "normal", color: str = "",
                 max_drones: int = 1):
        self.name = name
        self.cord = cord
        self.typezone = typezone
        self.color = color
        self.max_drones = max_drones
        self.actual_drones: list[str] = []

    def is_there_room(self) -> bool:
        return self.max_drones > len(self.actual_drones)

    def go_in(self, name_drone: str) -> bool:
        if self.is_there_room():
            self.actual_drones.append(name_drone)
            return True
        return False

    def go_out(self, name_drone: str) -> None:
        self.actual_drones.remove(name_drone)


class Connection:
    def __init__(self, hub_a: str, hub_b: str, max_capacity: int = 1):
        self.hub_a = hub_a
        self.hub_b = hub_b
        self.maxcapacity = max_capacity
        self.name_connection: str = f"{hub_a}-{hub_b}"
        self.actual_drones: list[str] = []

    def is_there_room(self) -> bool:
        return self.maxcapacity > len(self.actual_drones)

    def go_in(self, name_drone: str) -> bool:
        if self.is_there_room():
            self.actual_drones.append(name_drone)
            return True
        return False

    def go_out(self, name_drone: str) -> None:
        self.actual_drones.remove(name_drone)


class Drone:
    def __init__(self, name: str,
                 actual_position: str = "start_hub",
                 finish: bool = False):
        self.name = name
        self.actual_position = actual_position
        self.finish = finish

    def change_position(self, name_next_position: str) -> None:
        self.actual_position = name_next_position


class Map:
    def __init__(self, hub_dict: dict[str, Hub],
                 connection_dict: dict[str, Connection],
                 start_hub: str, end_hub: str, drones: list[Drone] ):
        self.hub_dict = hub_dict
        self.connection_dict = connection_dict
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.n_drones = len(drones)
        self.drones = drones

    def get_neighbors(self, name_hub: str) -> list[str]:
        list_hub_neighbors: list[str] = []
        for _, con in self.connection_dict.items():
            if name_hub == con.hub_a:
                list_hub_neighbors.append(con.hub_b)
            elif name_hub == con.hub_b:
                list_hub_neighbors.append(con.hub_a)
        return list_hub_neighbors
