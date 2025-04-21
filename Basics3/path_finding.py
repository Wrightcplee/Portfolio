import city_country_csv_reader
from locations import City, Country
from trip import Trip
from vehicles import Vehicle, create_example_vehicles, CrappyCrepeCar
import networkx as nx
import math


def find_shortest_path(vehicle: Vehicle, from_city: City, to_city: City) -> Trip:
	"""
	Returns a shortest path between two cities for a given vehicle,
	or None if there is no path.
	"""
	if isinstance(vehicle, CrappyCrepeCar):		#if vehicle is CrappyCrepeCar, shortest distance will be direct as it can travel anywhere
		trip = Trip(from_city)
		trip.add_next_city(to_city)
		return trip

	G = nx.Graph()											#plots the graph G
	for city1 in City.cities.values():						#for every city against every other city
		for city2 in City.cities.values():
			if city1 != city2 and vehicle.compute_travel_time(city1,city2) != math.inf:				#add edges when travel is possible, with travel duration as weight
				G.add_edge(city1, city2, weight = vehicle.compute_travel_time(city1, city2))		#nodes are auto added with add edge
	try:
		trip_lst = nx.shortest_path(G, from_city, to_city, weight = "weight")						#try to find shortest path based on weight
		trip = Trip(trip_lst[0])
		for city in trip_lst[1:]:
			trip.add_next_city(city)																#creates a trip
	except nx.exception.NetworkXNoPath:																#if no path between the nodes
		trip = None
	except nx.exception.NodeNotFound:																#if no nodes of that city is created (no path at all)
		trip = None
	return trip

if __name__ == "__main__":
	city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

	vehicles = create_example_vehicles()

	australia = Country.countries["Australia"]
	melbourne = australia.get_city("Melbourne")
	japan = Country.countries["Japan"]
	tokyo = japan.get_city("Tokyo")

	for vehicle in vehicles:
		print("The shortest path for {} from {} to {} is {}".format(vehicle, melbourne, tokyo, find_shortest_path(vehicle, melbourne, tokyo)))
