from locations import CapitalType, City, Country
from map_plotting import plot_trip
from path_finding import find_shortest_path
from trip import Trip, create_example_trips
from vehicles import Vehicle, CrappyCrepeCar, DiplomacyDonutDinghy, TeleportingTarteTrolley, create_example_vehicles
from city_country_csv_reader import create_cities_countries_from_CSV
import time
import math


class onboard_nav():

	def __init__(self) -> None:
		"""
		Executes the entire program of navigation.
		"""
		print("Welcome to Hello World Delivery!")
		vehicles = []
		create_cities_countries_from_CSV("worldcities_truncated.csv")					#creates all cities and countries class
		while True:
			if vehicles:																#if vehicle has already been created previously
				print("---------------------------------------\n1. Create new vehicles\n2. Previous configuration")
				if int_input("What vehicle configuration would you like to use: ", (1,2)) == 1:
					vehicles = self.create_custom_vehicles()
			else:																		#allows custom vehicles
				vehicles = self.create_custom_vehicles()
			print("---------------------------------------\n1. Example trips\n2. Custom trips\n3. Shortest path for a particular vehicle")
			trip_choice = int_input("Please choose your type of trip: ", (1,2,3))		#allows choosing for types of trips
			if trip_choice in (1,2):
				if trip_choice == 1:
					print("---------------------------------------")
					trips = create_example_trips()
					for i, trip in enumerate(trips):									#prints selection of trips
						print(f"{i+1}. {trip}")
					trip = trips[int_input("Please choose your trip: ", range(1,len(trips)+1))-1]
				else:
					trip = self.create_custom_trip()
				vehicle, duration = trip.find_fastest_vehicle(vehicles)					#finds fastest vehicle automatically
				print(f"The fastest vehicle is {vehicle} and will reach in {duration} hours!")
				if not yes(f"Do you want to use {vehicle}? (Y/N): "):					#if want to choose another vehicle
					duration = math.inf
					while duration == math.inf:											#if this vehicle chosen cannot complete trip, will loop
						vehicle = self.choose_vehicle(vehicles)
						duration = trip.total_travel_time(vehicle)
						if duration == math.inf:
							print("This vehicle cannot complete this trip!")
					print(f"{vehicle} will reach in {duration} hours!")
			else:																		#shortest path trip
				trip, vehicle = self.short_trip(vehicles)
				duration = trip.total_travel_time(vehicle)
				print(f"The {vehicle} will take {duration} hours to arrive!")
			plot_trip(trip)
			print(trip)
			self.progress_bar(trip, vehicle, duration)									#progress bar
			if not yes("Do you want to continue using Hello World Delivery? (Y/N): "):	#if you don't want to continue, end the program
				break
		print("Thanks for using Hello World Delivery!")
			

	def create_custom_vehicles(self) -> list[Vehicle]:
		"""
		Allows user to choose between example vehicles or custom vehicles.
		Returns the fleet of Vehicles in a list.
		"""
		vehicles = create_example_vehicles()
		print("---------------Creating new vehicle configuration---------------")
		if not yes("Do you want to use example CrappyCrepeCar configuration? (Y/N): "):					#if no, create custom vehicle
			vehicles[0] = CrappyCrepeCar(int_input("---------------------------------------\nInput your speed for CrappyCrepeCar: "))
		if not yes("Do you want to use example DiplomacyDonutDinghy configuration? (Y/N): "):
			vehicles[1] = DiplomacyDonutDinghy(int_input("Input your country speed for DiplomacyDonutDinghy: "), int_input("Input your between primary cities speed for DiplomacyDonutDinghy: "))
		if not yes("Do you want to use example TeleportingTarteTrolley configuration? (Y/N): "):
			vehicles[2] = TeleportingTarteTrolley(int_input("Input your teleporting speed for TeleportingTarteTrolley: "), int_input("Input your maximum distance for TeleportingTarteTrolley: "))
		return vehicles

	def choose_city(self) -> City:
		"""
		Allows user to choose cities based on two search options.
		Returns City user has chosen.
		"""
		while True:
			print("How would you like to search?\n1. By country\n2. By city name")
			if int_input("Select your search method: ", (1,2)) == 1:						#2 types of search options
				while True:																	#search by country
					print("------------------------------------")
					letter = ""
					while not letter.isalpha() or letter == "X":							#loops if invalid input
						letter = input("First letter of the country: ").upper()[:1]
						if letter == "X":
							print("There are no countries that start with the letter 'X'!")
					country_list = [country for country in Country.countries.keys() if country[0] == letter]
					print(f"----------------Countries that start with the letter '{letter}'----------------")
					for i, country in enumerate(country_list):								#prints list for country that start with searched letter
						print(f"{i+1}. {country}")
					chosen_country = Country.countries[country_list[int_input("Choose a country: ", range(1, len(country_list)+1))-1]]
					city_list = [city for city in chosen_country.cities]
					print(f"--------------------------Cities in {chosen_country}--------------------------")
					for i, city in enumerate(city_list):
						print(f"{i+1}. {city}")												#prints list for cities in searched country
					chosen_city = city_list[int_input("Choose a city: ", range(1, len(city_list)+1))-1]
					if yes(f"Your selected city is {chosen_city}. Confirm? (Y/N): "):		#final confirmation
						return chosen_city
					if not yes("Do you still want to use this search method? (Y/N): "):		#if chosen no previously
						break
			else:																			#search by name
				while True:
					print("------------------------------------")
					search_city = input("Please enter the city name: ").capitalize()
					city_list = [city for city in City.cities.values() if search_city in city.name and search_city]		#search for list if input is valid
					if city_list:
						print(f"-----------------Cities that start with '{search_city}'-----------------")
						for i, city in enumerate(city_list):
							print(f"{i+1}. {city}")											#prints city that start with inputed
						chosen_city = city_list[int_input("Choose a city: ", range(1, len(city_list)+1))-1]
						if yes(f"Your selected city is {chosen_city}. Confirm? (Y/N): "):	#final confirmation
							return chosen_city
					else:
						print("--------------------No such city found--------------------")
					if not yes("Do you still want to use this search method? (Y/N): "):		#if no city found or rechoosing city
						break

	def choose_vehicle(self, vehicles: list[Vehicle]) -> Vehicle:
		"""
		Allows user to choose which vehicle from the fleet to use. Prints out the list and parameters of the fleet
		Returns the chosen Vehicle.
		"""
		for i, vehicle in enumerate(vehicles):
				print(f"{i+1}. {vehicle}")
		return vehicles[int_input("Choose a vehicle: ", range(1, len(vehicles)+1))-1]
		
	def create_custom_trip(self) -> Trip:
		"""
		Allows user to make a custom trip. Will continue to add more location until the user stops.
		Returns Trip for the cities chosen.
		"""
		print("-----------Choose your desired departure location-----------")
		trip = Trip(self.choose_city())
		while True:
			print("----------------Choose your next location----------------")
			trip.add_next_city(self.choose_city())
			if not yes("Do you want to add more location? (Y/N): "):
				return trip

	def short_trip(self, vehicles: list[Vehicle]) -> tuple[Trip, Vehicle]:
		"""
		Allows user to choose two Cities (departure and arrival) and Vehicles.
		Returns the shortest possible path made by the Vehicle between the 2 City.
		"""
		print("-----------Choose your desired departure location-----------")
		from_city = self.choose_city()
		print("-----------Choose your desired arrival location-----------")
		to_city = self.choose_city()
		print("--------------Choose your vehicle--------------")
		while True:
			vehicle = self.choose_vehicle(vehicles)
			trip = find_shortest_path(vehicle, from_city, to_city)
			if not trip:																#if trip is None, continues loop
				print("Your trip does not exist! Please choose another vehicle.")
				continue
			print(f"Your trip will be: '{trip}'")
			if yes("Confirm vehicle? (Y/N): "):
				return trip, vehicle

	def progress_bar(self, trip: Trip, vehicle: Vehicle, duration: int) -> None:
		bar_size = 50
		bar = "["+" "*bar_size+"]"+" 0%"												#default bar
		spaces = max([len(city.__str__()) for city in trip.cities])						#to prevent leftover words when replacing print
		trip_breakdown = [vehicle.compute_travel_time(trip.cities[i], trip.cities[i+1]) for i in range(len(trip.cities)-1)]			#time it takes to travel between cities
		trip_breakdown = [sum(trip_breakdown[:i]) for i in range(len(trip_breakdown))]+[duration]									#time stamp of where the vehicle is
		print(bar, end="\r")
		for hour in range(1,duration):
			time.sleep(0.1)
			percentage = int(hour/duration*100)											#for the percentage bar
			update = int(hour/duration*bar_size)										#number of "*"
			for i, x in enumerate(trip_breakdown):										#to know which part of the journey the vehicle is at
				if hour < x:
					index = i
					break
			current_city = trip.cities[index]
			print("["+"*"*update+" "*(bar_size-update)+f"] {percentage}%  Travelling to {current_city}..."+" "*spaces, end="\r")
		time.sleep(0.1)
		print("["+"*"*bar_size+"] 100%  Delivered!"+"   "*spaces)						#final print without replacing


def int_input(prompt="", restricted_to=None):
	"""
	Helper function that modifies the regular input method,
	and keeps asking for input until a valid one is entered. Input 
	can also be restricted to a set of integers.

	Arguments:
		- prompt: String representing the message to display for input
		- restricted: List of integers for when the input must be restricted
					to a certain set of numbers

	Returns the input in integer type.
	"""
	while True:
		player_input = input(prompt)
		try:                           
			int_player_input = int(player_input)
			assert int_player_input > 0
		except Exception:
			continue
		if restricted_to is None:
			break
		elif int_player_input in restricted_to:
			break

	return int_player_input

def yes(input_msg) -> bool:
	"""
	Helper function for Yes and No questions. Not case-sensitive
	Returns True for Y/yes, False for N/no. 
	"""
	reply = None
	while reply not in ("Y","N","YES","NO"):
		reply = input(input_msg).upper()
	if reply in ("Y","YES"):
		return True
	return False

if __name__ == "__main__":
	onboard_nav()
