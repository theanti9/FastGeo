

class DbParser(object):
	"""
	DbParse parser is meant to serve as an interface for creating parsers to load data from a file or external source.
	"""

	def parse(self, path=None):
		"""
		Parses the CSV database into List((GeoNode, GeoValue), ...)

		Note: May take several seconds.
		"""
		raise NotImplementedError


	def create_node(self, line):
		"""
		Creates a GeoNode from a line of the parsed CSV file.

		Can be overriden for easy parsing of other similar CSV files.
		"""
		raise NotImplementedError


	def create_value(self, line):
		"""
		Creates a GeoValue from a line of the parsed CSV file.

		Can be overriden for easy parsing of other similar CSV files.
		"""
		raise NotImplementedError
