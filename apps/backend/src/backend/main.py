import logging
from datetime import datetime

from firebase_admin import auth
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from src.backend.get_recommendation import get_recommendations
from src.backend.get_user_trip_history import get_user_trip
from src.data_model import UserPreferences
from src.database import DataBase, DataBaseUsers

app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': 'http://localhost:4200'}})

db = DataBase()
db_users = DataBaseUsers()


@app.route('/api/trip-history/<trip_id>', methods=['GET'])
def trip_details(trip_id: str):
	token: str = request.headers.get('Authorization', '').split('Bearer ')[1]
	try:
		trip = get_user_trip(
			db,
			db_users,
			token,
			trip_id,
		)
		print('\n' * 4, trip)
		return jsonify(
			{
				'success': True,
				'data': trip,
			}
		), 200
	except auth.InvalidIdTokenError:
		logging.exception('Invalid token')
		return jsonify(
			{
				'success': False,
				'message': 'Unauthorized',
			}
		), 401
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify(
			{
				'success': False,
				'message': str(e),
			}
		), 500


@app.route('/api/recommendation/preferences', methods=['POST'])
@cross_origin(origins='localhost', allow_headers=['Content-Type', 'Authorization'])
def get_with_categories():
	"""Check if loc exist in firebase db"""
	data = request.json

	if not data:
		return jsonify({'status': 'error', 'message': 'No data in the request'})

	categories = [category for category in data['preferences']['categories'].keys()]
	subcategories = data['preferences']['categories']
	dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in data['dates']]
	dates_tuple = (dates[0], dates[1])

	user_specified_needs = UserPreferences(
		data['preferences']['needs'],
		data['preferences']['money'],
		categories,
		subcategories,
	)
	try:
		recommendation = get_recommendations(
			db,
			db_users,
			data['user_id'],
			data['city_id'],
			data['days'],
			dates_tuple,
			user_specified_needs,
		)
	except Exception as e:
		logging.exception(e.__str__())
		return jsonify({'status': 'error', 'received_data': e.__str__()})

	return jsonify({'status': 'success', 'received_data': recommendation})


if __name__ == '__main__':
	app.run(port=5000)
