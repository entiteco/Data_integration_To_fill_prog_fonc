import json, csv
from functools import reduce
from collections import Counter

def read_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def add_flight_number_to_passenger(passenger, flight_number):
    # TODO fill method
    passenger["flight_number"] = flight_number
    return passenger

def add_flight_number_to_passengers(flight):
    flight_number = flight["flight_number"]
    passengers = flight["passengers"]
    transformed_passengers = [add_flight_number_to_passenger(passenger, flight_number) for passenger in passengers]
    flight["passengers"] = transformed_passengers
    return flight

def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)  # Reads the file as a dictionary per row
        return list(reader)

def get_city(flight, airports, origin=None):
    # TODO fill the method
    if origin:
        airport_code = flight["origin"]
    else:
        airport_code = flight["destination"]
    return airports.get(airport_code, "Unknown City")



def add_city_names_to_flights(flights, airports_list):
    airports_map = {airport['code']: airport['city'] for airport in airports_list if airport['city']}
    
    updated_flights = []
    for flight in flights:
        flight_copy = flight.copy()
        flight_copy['origin_city'] = get_city(flight_copy, airports_map, origin=True)
        flight_copy['destination_city'] = get_city(flight_copy, airports_map, origin=False)
        updated_flights.append(flight_copy)
        
    return updated_flights

def get_top_departure_cities(flights, top_n=5):
    departure_counts = Counter(flight["origin"] for flight in flights)
    city_counts = Counter({iata: count for iata, count in departure_counts.items()})
    return city_counts.most_common(top_n)

if __name__ == '__main__':
    data = read_json("resources/flights.json")

    # print the number of flights in the input file
    print(len(data["flights"]))

    # Get the flights
    flights = data["flights"]

    # add the flight_number information in the passenger dictionary and build the passenger table
    data_with_flight_number_in_passenger = [add_flight_number_to_passengers(flight.copy()) for flight in flights]

    print("Raw dataset with enriched passengers", data_with_flight_number_in_passenger[0])

    # Create the passenger dataset
    passengers = [flight["passengers"] for flight in data_with_flight_number_in_passenger]

    # flatten the map
    passengers_flatten = [passenger for sublist in passengers for passenger in sublist]
    print("Element in passenger dataset", passengers_flatten[1])

    # Create the flight dataset
    flights = [{k: v for k, v in flight.items() if k != 'passengers'} for flight in data_with_flight_number_in_passenger]
    print("Element in flight Dataset",flights[0])

    # read the airport file
    airports = read_csv("resources/airports.csv")
    # Print the 10 first elements of the airports dataset
    print("airports", airports[0:10])

    # In flight dataset, add 2 new columns with origin and destination converted into real city names
    # The code in origin and destination is the iata code
    updated_flights = add_city_names_to_flights(flights, airports)
    print("Flight updated with cities",updated_flights[0:5])

    # cities with the most outgoing flights
    top_10_departure_cities = get_top_departure_cities(updated_flights, 10)
    print(top_10_departure_cities)
