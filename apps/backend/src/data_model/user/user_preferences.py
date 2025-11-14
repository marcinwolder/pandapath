import json
from dataclasses import dataclass
from typing import Any, Literal, TypeAlias

Need: TypeAlias = Literal[
	'wheelchairAccessible',
	'goodForGroups',
	'vegan',
	'children',
	'alcohol',
	'allowsDogs',
]


@dataclass
class UserPreferences:
	"""User preferences data model."""

	priceLevel: int
	accessibilityOptions: bool
	goodForGroups: bool

	servesVegetarianFood: bool
	children: bool
	alcohol: bool
	allowsDogs: bool
	categories: list[str]

	subcategories: dict[str, list[str]]
	restaurant_categories: list[str]

	def __init__(
		self,
		needs: list[Need],
		priceLevel: int,
		categories: list[str],
		subcategories: dict[str, list[str]],
	):
		self.price_level: int = priceLevel

		self.accessibility_options: bool = 'wheelchairAccessible' in needs
		self.good_for_groups: bool = 'goodForGroups' in needs

		self.serves_vegetarian_food: bool = 'vegan' in needs
		self.children: bool = 'children' in needs
		self.alcohol: bool = 'alcohol' in needs
		self.allows_dogs: bool = 'allowsDogs' in needs
		self.categories: list[str] = categories
		self.subcategories: dict[str, list[str]] = subcategories
		self._handle_places_of_worship()
		self.restaurant_categories: list[str] = []

	def _handle_places_of_worship(self):
		"""Handle places of worship."""
		if 'place_of_worship' not in self.categories:
			return
		self.categories.remove('place_of_worship')
		pow: list[str] = self.subcategories.pop('place_of_worship')
		if len(pow) == 0:
			pow: list[str] = ['church', 'mosque', 'synagogue']
		for cat in pow:
			if cat == 'church':
				self.categories.append('church')
				self.subcategories['church'] = []
			elif cat == 'mosque':
				self.categories.append('mosque')
				self.subcategories['mosque'] = []
			elif cat == 'synagogue':
				self.categories.append('synagogue')
				self.subcategories['synagogue'] = []

	def to_json(self):
		return json.dumps(self.to_dict())

	def cat_weights(self):
		weights = dict.fromkeys(self.categories, 0)
		for key, _ in weights.items():
			weights[key] = len(self.subcategories[key])
		return weights

	def to_dict(self) -> dict[str, Any]:
		return {
			'priceLevel': self.price_level,
			'wheelchairAccessible': self.accessibility_options,
			'goodForGroups': self.good_for_groups,
			'vegan': self.serves_vegetarian_food,
			'children': self.children,
			'alcohol': self.alcohol,
			'allowsDogs': self.allows_dogs,
			'restaurant': self.restaurant_categories,
		}
