import city_country_csv_reader
from locations import create_example_countries_and_cities
from trip import Trip, create_example_trips
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def plot_trip(trip: Trip, projection = 'cyl', line_width=2, colour='b') -> None:
	"""
	Plots a trip on a map and writes it to a file.
	Ensures a size of at least 50 degrees in each direction.
	Ensures the cities are not on the edge of the map by padding by 5 degrees.
	The name of the file is map_city1_city2_city3_..._cityX.png.
	"""
	long_lst = [float(city.long) for city in trip.cities]						#list of longitude of cities in trip
	lat_lst = [float(city.lat) for city in trip.cities]							#list of latitude of cities in trip
	centre_long = (min(long_lst)+max(long_lst))/2
	centre_lat = (min(lat_lst)+max(lat_lst))/2									#finds the center of the map amongst the cities
	coordinates = [centre_long-25,centre_long+25,centre_lat-25,centre_lat+25]	#adds 25 degrees in each direction to meet 50 degree requirement
	if max(long_lst) - min(long_lst) > 50:										#if cities are more than 50deg apart in longitude, changes the coordinates
		coordinates[0] = min(long_lst)-5
		coordinates[1] = max(long_lst)+5
	if max(lat_lst) - min(lat_lst) > 50:										#if cities are more than 50deg apart in latitude, changes the coordinates
		coordinates[2] = min(lat_lst)-5
		coordinates[3] = max(lat_lst)+5
	map = Basemap(projection=projection, llcrnrlon=coordinates[0], urcrnrlon=coordinates[1], 
				llcrnrlat=coordinates[2], urcrnrlat=coordinates[3], resolution='c', lon_0=centre_long-180)
																				#lon_0 is to prevent robinson projection error
	map.drawcoastlines()						#draw coastal and countries border
	map.drawcountries()
	map.fillcontinents(color = "lightgrey")

	x, y = map(long_lst, lat_lst)
	map.plot(x, y, c=colour, lw= line_width)					#plot straight line

	name = "map"
	for city in trip.cities:									#creates name of map plot
		name += f"_{city.name}"
	plt.savefig(f"{name}.png")
	plt.clf()													#clear plot after saving image


if __name__ == "__main__":
	city_country_csv_reader.create_cities_countries_from_CSV("worldcities_truncated.csv")

	create_example_countries_and_cities()

	trips = create_example_trips()

	for trip in trips:
		plot_trip(trip)
