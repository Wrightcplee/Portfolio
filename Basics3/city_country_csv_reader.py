import csv
from locations import City, Country, test_example_countries_and_cities

def create_cities_countries_from_CSV(path_to_csv: str) -> None:
	"""
	Reads a CSV file given its path and creates instances of City and Country for each line.
	"""
	with open(path_to_csv, 'r') as csv_file:
		csv_reader = csv.DictReader(csv_file)			#default delimiter is "," and quotechar is "
		for line in csv_reader:							#also auto assign header to fields as dict
			if line['country'] not in Country.countries:
				Country(line['country'], line['iso3'])
			City(line['city_ascii'], line['lat'], line['lng'], line['country'], line['capital'], line['id'])

if __name__ == "__main__":
	create_cities_countries_from_CSV("worldcities_truncated.csv")
	test_example_countries_and_cities()
