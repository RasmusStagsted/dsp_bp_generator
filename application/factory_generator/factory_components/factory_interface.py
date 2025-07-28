import math
from dsp_bp_generator.utils import Vector, Yaw
from dsp_bp_generator import buildings
from ..recipes import Item
import logging

class FactoryInterface:
    def __init__(self, pos, bus_interface, input_sources, output_destinations):
        self.pos = pos
        self.bus_interface = bus_interface
        self.input_sources = input_sources
        self.output_destinations = output_destinations
        self.interface = {"ingredient": []}
        
        self.generate_logistic_station_data()
        self.generate_pls(pos)

    def generate_logistic_station_data(self):
        pls_count = 0
        ils_count = 0
        routes = {}
        for key, value in self.input_sources.items():
            if value["type"] == "PLS":
                routes[key] = {
                    "LS": "PLS",
                    "type": "source",
                    "index": math.floor(pls_count / 3),
                    "item_index": pls_count % 3,
                    "items_per_second": value["items_per_second"],
                }
                pls_count += 1
            if value["type"] == "ILS":
                routes[key] = {
                    "LS": "ILS",
                    "type": "source",
                    "index": math.floor(ils_count / 3),
                    "item_index": ils_count % 3,
                    "items_per_second": value["items_per_second"],
                }
                ils_count += 1
        for key, value in self.output_destinations.items():
            if value["type"] == "PLS":
                routes[key] = {
                    "LS": "PLS",
                    "type": "destination",
                    "index": math.floor(pls_count / 3),
                    "item_index": pls_count % 3,
                    "items_per_second": value["items_per_second"],
                }
                pls_count += 1
            if value["type"] == "ILS":
                routes[key] = {
                    "LS": "ILS",
                    "type": "destination",
                    "index": math.floor(ils_count / 3),
                    "item_index": ils_count % 3,
                    "items_per_second": value["items_per_second"],
                }
                ils_count += 1
        self.pls_count = math.ceil(pls_count / 3)
        self.ils_count = math.ceil(ils_count / 3)
        self.routes = routes
        print(routes)

    def generate_pls(self, pos):
        # Place PLSs
        plss = []
        for i in range(self.pls_count):
            pls = buildings.PlanetaryLogisticsStation(name = "PLS", pos = pos + Vector(x = -7.0, y = 6 + i * 10))
            plss.append(pls)

        for key, route in self.routes.items():
            for proliferator in ["No-Proliferator", "MK.I", "MK.II", "MK.III"]:
                if proliferator in key:
                    key = key.replace(proliferator, "")
                    break

            if route["LS"] == "PLS":
                pls = plss[route["index"]]
                item_id = Item.items[key].item_id
                if route["type"] == "source":
                    mode = pls.ItemMode.DEMAND
                elif route["type"] == "destination":
                    mode = pls.ItemMode.SUPPLY
                items_per_second = route["items_per_second"]
                pls.set_item(item_index = route["item_index"], item_id = item_id, mode = mode, storage_limit = 100)
                self.route_belt_from_pls_to_bus(pls, route["item_index"], key, proliferator, items_per_second)
        # Route belt from PLAs to factory bus

    def route_belt_from_pls_to_bus(self, pls, pls_item_index, item_name, proliferator, items_per_second):
        item_name = item_name + proliferator + "FlowBus"
        for bus_belt in self.bus_interface.belts:
            if bus_belt.name == item_name:
                belt_type = buildings.ConveyorBelt.get_minimum_required_belt_type(items_per_second)
                start_pos = pls.get_position_of_slot(pls_item_index + 9).closest_grid_point()
                x_length = int(bus_belt.pos.x - start_pos.x)
                y_length = int(start_pos.y - self.pos.y)
                belt = belt_type.generate_belt(
                    name = "",
                    pos = start_pos,
                    yaw = [Yaw.East, Yaw.South],
                    length = [x_length, y_length]
                )
                belt[x_length - 2].set_height(0.5)
                belt[x_length - 1].set_height(1.0)
                for b in belt[x_length:]:
                    b.set_height(1.0)
                pls.connect_output_to_belt(belt[0], pls_item_index)
                self.interface["ingredient"].append(belt[-1])
                return
        logging.error(f"{item_name} not found in bus interface: {self.bus_interface}")
        
    def connect_to_bus(self, bus_interface, input_list, graph):
        j = 0
        for i, node_name in enumerate(input_list):
            node_name = node_name[:-4]
            if self.input_sources[node_name]["type"] == "PLS":
                belt = bus_interface["ingredient"][i]
                self.interface["ingredient"][j].connect_to_belt(belt)
                j = j + 1
        for belt in bus_interface["product"]:
            pass
        # TODO: Implement connection to bus interface