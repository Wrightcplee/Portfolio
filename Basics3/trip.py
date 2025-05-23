from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley
from vehicles import create_example_vehicles
from locations import City, Country
from locations import create_example_countries_and_cities
import math


class Trip():
	"""
	Represents a sequence of cities.
	"""

	def __init__(self, departure: City) -> None:
		"""
		Initialises a Trip with a departure city.
		"""
		self.cities = [departure]													# departure city is the first element of list

	def add_next_city(self, city: City) -> None:
		"""
		Adds the next city to this trip.
		"""					
		self.cities.append(city) 													# appends city to self.cities

	def total_travel_time(self, vehicle: Vehicle) -> float:
		"""
		Returns a travel duration for the entire trip for a given vehicle.
		Returns math.inf if any leg (i.e. part) of the trip is not possible.
		"""
		time = 0
		for i in range(len(self.cities)-1):											# iterates until the second last city
			time += vehicle.compute_travel_time(self.cities[i], self.cities[i+1])	# adds travel time between two cities to time
		return time


	def find_fastest_vehicle(self, vehicles: list[Vehicle]) -> (Vehicle, float):
		"""
		Returns the Vehicle for which this trip is fastest, and the duration of the trip.
		If there is a tie, return the first vehicle in the list.
		If the trip is not possible for any of the vehicle, return (None, math.inf).
		"""
		fastest, duration = None, math.inf		# when if clause in line 44 is not iterated, this will be return (trip not possible for any vehicle)
		for vehicle in vehicles:
			if self.total_travel_time(vehicle) < duration:							# iterates if travel time is faster than current duration
				fastest, duration = vehicle, self.total_travel_time(vehicle)		# sets travel time as new duration
		return (fastest,duration)	

	def __str__(self) -> str:
		"""
		Returns a representation of the trip as a sequence of cities:
		City1 -> City2 -> City3 -> ... -> CityX
		"""
		return " -> ".join([f"{city}" for city in self.cities])						# returns the trip 


def create_example_trips() -> list[Trip]:
	"""
	Creates examples of trips.
	"""

	#first we create the cities and countries
#	create_example_countries_and_cities()											#removed this so it doesn't create multiple times in onboard_nav

	australia = Country.countries["Australia"]
	melbourne = australia.get_city("Melbourne")
	sydney = australia.get_city("Sydney")
	canberra = australia.get_city("Canberra")
	japan = Country.countries["Japan"]
	tokyo = japan.get_city("Tokyo")
	
	#then we create trips
	trips = []
	
	for cities in [(melbourne, sydney), (canberra, tokyo), (melbourne, canberra, tokyo), (canberra, melbourne, tokyo)]:
		trip = Trip(cities[0]) 
		for city in cities[1:]:
			trip.add_next_city(city)
		trips.append(trip)
	return trips 


if __name__ == "__main__":
	vehicles = create_example_vehicles()
	trips = create_example_trips()
	
	for trip in trips:
		vehicle, duration = trip.find_fastest_vehicle(vehicles)
		print("The trip {} will take {} hours with {}".format(trip, duration, vehicle))
