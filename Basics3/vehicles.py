from abc import ABC, abstractmethod
import math

from locations import CapitalType, City, Country
from locations import create_example_countries_and_cities

class Vehicle(ABC):
	"""
	A Vehicle defined by a mode of transportation, which results in a specific duration.
	"""

	@abstractmethod
	def compute_travel_time(self, departure: City, arrival: City) -> float:
		"""
		Returns the travel duration of a direct trip from one city
		to another, in hours, rounded up to an integer.
		Returns math.inf if the travel is not possible.
		"""
		pass

	@abstractmethod
	def __str__(self) -> str:
		"""
		Returns the class name and the parameters of the vehicle in parentheses.
		"""
		pass


class CrappyCrepeCar(Vehicle):
	"""
	A type of vehicle that:
		- Can go from any city to any other at a given speed.
	"""

	def __init__(self, speed: int) -> None:
		"""
		Creates a CrappyCrepeCar with a given speed in km/h.
		"""
		self.speed = speed

	def compute_travel_time(self, departure: City, arrival: City) -> float:
		"""
		Returns the travel duration of a direct trip from one city
		to another, in hours, rounded up to an integer.
		"""
		distance = departure.distance(arrival)				# calculates distance
		duration = math.ceil(distance/self.speed)			# calculates duration
		return duration

	def __str__(self) -> str:
		"""
		Returns the class name and the parameters of the vehicle in parentheses.
		For example "CrappyCrepeCar (100 km/h)"
		"""
		return f"CrappyCrepeCar ({self.speed} km/h)"		# returns Vehicle with given speed


class DiplomacyDonutDinghy(Vehicle):
	"""
	A type of vehicle that:
		- Can travel between any two cities in the same country.
		- Can travel between two cities in different countries only if they are both "primary" capitals.
		- Has different speed for the two cases.
	"""

	def __init__(self, in_country_speed: int, between_primary_speed: int) -> None:
		"""
		Creates a DiplomacyDonutDinghy with two given speeds in km/h:
			- one speed for two cities in the same country.
			- one speed between two primary cities.
		"""
		self.in_country_speed = in_country_speed
		self.between_primary_speed = between_primary_speed

	def compute_travel_time(self, departure: City, arrival: City) -> float:
		"""
		Returns the travel duration of a direct trip from one city
		to another, in hours, rounded up to an integer.
		Returns math.inf if the travel is not possible.
		"""
		distance = departure.distance(arrival)							# calculates distance
		if departure.country == arrival.country:						# iterates if cities are in the same country
			duration = math.ceil(distance/self.in_country_speed)		# calculates duration by using in_country_speed
		elif departure.capital_type == CapitalType("primary") and arrival.capital_type == CapitalType("primary"):	# iterates if cities are both primary capitals
			duration = math.ceil(distance/self.between_primary_speed)	# calculates duration by using between_primary_speed
		else:
			duration = math.inf											# if none of the above scenarios is the case duration is set to inf
		return duration

	def __str__(self) -> str:
		"""
		Returns the class name and the parameters of the vehicle in parentheses.
		For example "DiplomacyDonutDinghy (100 km/h | 200 km/h)"
		"""
		return f"DiplomacyDonutDinghy ({self.in_country_speed} km/h | {self.between_primary_speed} km/h)"


class TeleportingTarteTrolley(Vehicle):
	"""
	A type of vehicle that:
		- Can travel between any two cities if the distance is less than a given maximum distance.
		- Travels in fixed time between two cities within the maximum distance.
	"""

	def __init__(self, travel_time:int, max_distance: int) -> None:
		"""
		Creates a TarteTruck with a distance limit in km.
		"""
		self.travel_time = travel_time
		self.max_distance = max_distance

	def compute_travel_time(self, departure: City, arrival: City) -> float:
		"""
		Returns the travel duration of a direct trip from one city
		to another, in hours, rounded up to an integer.
		Returns math.inf if the travel is not possible.
		"""
		distance = departure.distance(arrival)			# calculates distance
		if distance < self.max_distance:				# if distance is less the the maximum distance to use the TeleportingTarteTrolley
			duration = self.travel_time					# sets duration to TeleportingTarteTrolley travel time
		else:
			duration = math.inf							# if distance is larger than the maximum distance to use the TeleportingTarteTrolley, duration is set to inf
		return duration

	def __str__(self) -> str:
		"""
		Returns the class name and the parameters of the vehicle in parentheses.
		For example "TeleportingTarteTrolley (5 h | 1000 km)"
		"""
		return f"TeleportingTarteTrolley ({self.travel_time} h | {self.max_distance} km)"


def create_example_vehicles() -> list[Vehicle]:
	"""
	Creates 3 examples of vehicles.
	"""
	return [CrappyCrepeCar(200), DiplomacyDonutDinghy(100, 500), TeleportingTarteTrolley(3, 2000)]

if __name__ == "__main__":
	create_example_countries_and_cities()

	australia = Country.countries["Australia"]
	melbourne = australia.get_city("Melbourne")
	canberra = australia.get_city("Canberra")
	japan = Country.countries["Japan"]
	tokyo = japan.get_city("Tokyo")
	
	vehicles = create_example_vehicles()

	for vehicle in vehicles:
		for from_city, to_city in [(melbourne, canberra), (tokyo, canberra), (tokyo, melbourne)]:
			print("Travelling from {} to {} will take {} hours with {}".format(from_city, to_city, vehicle.compute_travel_time(from_city, to_city), vehicle))
