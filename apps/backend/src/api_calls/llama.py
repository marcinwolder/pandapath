import json
import logging
import os

import requests

from src.data_model.places.places import Places

SUMMARY_PROMPT = """
<ROLE>
    You are a travel copywriter. You must write a short summary of a trip on the provided places.
</ROLE>
<RULES>
    - Mention most places
	- Keep to the provided names and city.
</RULES>
<OUTPUT>
    2-3 paragraph, second-person narrative about a future trip in the provided city.
</OUTPUT>
"""


class Llama:
	# In Docker the LLM container is reachable as `llama`; override via LLAMA_API_URL for host runs.
	API_URL = os.getenv('LLAMA_API_URL', 'http://llama:3000/v1/chat/completions')

	@classmethod
	def get_summary(cls, city: str, trip: list[Places]):
		trip_lines = []
		for i, day in enumerate(trip):
			day_places = ', '.join(
				place.placeInfo.displayName for place in day.get_list()
			)
			trip_lines.append(f'Day {i + 1}: {day_places}')
		trip_str = '\n'.join(trip_lines)
		modified_messages = [
			{
				'content': SUMMARY_PROMPT,
				'role': 'system',
			}
		] + [{'content': f'City: {city}, Places: {trip_str}', 'role': 'user'}]

		try:
			response = requests.post(
				cls.API_URL,
				json={
					'messages': modified_messages,
					'max_tokens': 600,
					'temperature': 0.3,
				},
			)

			if response.encoding is None:
				response.encoding = 'utf-8'

			response_dict = json.loads(response.text)
			return response_dict['choices'][0]['message']['content']
		except Exception as e:
			logging.exception(e.__str__())
			return ''
