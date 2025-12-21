from src.data_model.city.city import City
from src.data_model.place.place_visitor import PlaceVisitor
from src.database import DataBase, DataBaseTrips


def get_trip(db: DataBase, db_trips: DataBaseTrips, trip_id: str):
	trip = db_trips.get_trip(trip_id)
	city = City(trip['city_id'])
	place_map = db.get_place_map(city)
	for day in trip['days']:
		for i, place in enumerate(day['places']):
			place_id = place.get('id')
			full_place = place_map.get(place_id)
			if full_place is None:
				full_place = db.get_place(city, place_id)
			day['places'][i] = {**PlaceVisitor.place_to_itinerary(full_place), **place}
	return trip


def get_trip_history(db: DataBase, db_trips: DataBaseTrips):
	trip_history = db_trips.get_trip_history()
	for i, trip in enumerate(trip_history):
		trip_history[i] = get_trip(db, db_trips, trip['id'])
	return trip_history


def get_trip_history_overview(db_trips: DataBaseTrips):
	trip_history = db_trips.get_trip_history()
	overview = []
	for trip in trip_history:
		overview.append(
			{
				'trip_id': trip.get('id'),
				'city_name': trip.get('city_name'),
				'days_len': trip.get('days_len', len(trip.get('days', []))),
				'dates': trip.get('dates', []),
			}
		)
	return overview
