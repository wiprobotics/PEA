import os
import networkx as nx


class Location:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.links = []  # Each link is a tuple: (location, link_type)

    def add_link(self, other_location, link_type=""):
        self.links.append((other_location, link_type))
        other_location.links.append((self, link_type))

    def remove_link(self, other_location):
        for link in self.links:
            if link[0] == other_location:
                self.links.remove(link)
                other_location.links.remove((self, link[1]))

    def save_to_file(self):
        filename = f"Project/Dependencies/Locations/{self.name}.txt"
        with open(filename, "w") as file:
            file.write(f"Name: {self.name}\n")
            if self.description:
                file.write(f"Description: {self.description}\n")
            for link, link_type in self.links:
                file.write(f"Link: {link.name} ({link_type})\n")

    def find_link_type(self, other_location):
        for link, link_type in self.links:
            if link == other_location:
                return link_type
        return None
    

class LocationManager:
    def __init__(self):
        self.locations = []

    def add_location(self, name, description=""):
        new_location = Location(name, description)
        self.locations.append(new_location)
        return new_location

    def load_locations(self):
        for filename in os.listdir("Project/Dependencies/Locations"):
            fullPath = os.path.join("Project/Dependencies/Locations", filename)
            if filename.endswith(".txt"):
                with open(fullPath, "r") as file:
                    name = file.readline().strip().split(": ")[1]
                    description = ""
                    for line in file:
                        if line.startswith("Description:"):
                            description = line.strip().split(": ")[1]
                            break
                    new_location = self.add_location(name, description)
                    file.seek(0)
                    for line in file:
                        if line.startswith("Link: "):
                            parts = line.strip().split(": ")
                            if len(parts) >= 2:  # Ensure there are at least two elements
                                link_name = parts[1].split(" (")[0]
                                link_type = parts[1].split(" (")[1][:-1] if len(parts[1].split(" (")) > 1 else ""
                                linked_location = self.find_location(link_name)
                                if linked_location:
                                    new_location.add_link(linked_location, link_type)

    def find_location(self, name):
        for location in self.locations:
            if location.name == name:
                return location
        return None

    def find_route(self, start_location_name, end_location_name):
        G = nx.Graph()

        # Add nodes (locations)
        for location in self.locations:
            G.add_node(location.name)

        # Add edges (links between locations)
        for location in self.locations:
            for link, _ in location.links:
                G.add_edge(location.name, link.name)

        try:
            shortest_path = nx.shortest_path(G, source=start_location_name, target=end_location_name)
            return shortest_path
        except nx.NetworkXNoPath:
            return None


class Run():

    def __init__(self):
        print("LocationModule has been loaded")
        self.location_manager = LocationManager()
        self.location_manager.load_locations()
        self.current_location = self.location_manager.find_location("Robotics Lab")

    def ReturnDescription(self):
        return "This module manages locations and links between them allowing the user to find routes between locations, it must be used when the user asks how to get to a location, do not imagine the routes, it has one string input which is the destination you want to get to. The module is told what the current location is so you don't have to tell it every time. The module will then return the route to the destination."
    
    def ReturnScenario(self):
        response = "This module should be used when the user asks something similar to:"
        response += "\n\t\t - How do I get to the 'Location'?"
        response += "\n\t\t - What is the route to the 'Location'?"
        response += "\n\t\t - How do I get to the 'Location' from here?"
        response += "\n\t\t - What is the route to the 'Location' from here?"
        return response

    def ReturnFunctionality(self):
        return self.location_manager
    
    def ReturnResponse(self, end_location):
        start = self.current_location.name
        end_location = end_location.title()
        try:
            end = self.location_manager.find_location(end_location).name
        except AttributeError:
            return "The location could not be found. It may not exist or it may not be in the system. Please ask the user to try again or talk to the system administrator."
        if start and end:
            route = self.location_manager.find_route(start, end)
            peaNote = "PEA here is the route which the user must follow to get to the {}: {} Please explain the route without expanding any more on the data you have been given".format(end, route)
            return peaNote
        else:
            return "One or both of the locations could not be found."
