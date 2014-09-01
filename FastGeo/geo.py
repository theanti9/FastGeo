import socket, struct, re, sys, os, csv
from parsers import DbParser
from bintrees import FastAVLTree


class MaxMindGeoLiteCSVParser(DbParser):
	"""
	The default GeoIP Database parser to load the GeoData from.

	Designed to use the Max Mind GeoLite country CSV. (Available at http://www.maxmind.com)
	"""

	fields = {
		"ip_lower": 0,
		"ip_upper": 1,
		"long_lower": 2,
		"long_upper": 3,
		"country_code": 4,
		"country_name": 5
	}

	def parse(self, path=None):
		"""
		Parses the CSV database into List((GeoNode, GeoValue), ...)

		Note: May take several seconds.
		"""

		# Default to the MaxMind file distributed with the source
		if path is None:
			basepath = os.path.dirname(os.path.abspath(__file__))
			path = os.path.join(basepath, "data", "geoip.csv")

		if not os.path.exists(path):
			raise IOError("File not found: %s" % path)

		with open(path) as csvfile:
			georeader = csv.reader(csvfile)
			for line in georeader:
				node = self.create_node(line)
				value = self.create_value(line)
				yield (node, value)

	def create_node(self, line):
		"""
		Creates a GeoNode from a line of the parsed CSV file.
		"""
		return GeoNode(long(line[self.fields["long_lower"]]), long(line[self.fields["long_upper"]]))

	def create_value(self, line):
		"""
		Creates a GeoValue from a line of the parsed CSV file.
		"""
		return GeoValue(line[self.fields["ip_lower"]], line[self.fields["ip_upper"]], line[self.fields["country_code"]], line[self.fields["country_name"]])


class GeoNode(object):
	"""
	GeoNode encapsulates an IP range into single node that can be easily inserted into a search tree.
	"""
	ip_check = re.compile(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}")

	def __init__(self, lower, upper):
		"""
		Creates a GeoNode given the lower and upper bounds of an IP range as either Long's or dotted-decimal formatted strings.
		"""
		if isinstance(lower, str):
			lower = self.__class__.ip2long(lower)

		if isinstance(upper, str):
			upper = self.__class__.ip2long(upper)

		if not isinstance(lower, long) or not isinstance(upper, long):
			raise ValueError("Invalid IP longs")

		self.lower = lower
		self.upper = upper

	@staticmethod
	def ip2long(ip):
		"""
		Converts a dotted-decimal formatted string to a Long
		"""
		return struct.unpack("!L", socket.inet_aton(ip))[0]

	@staticmethod
	def valid_ip(ip):
		"""
		Checks that a string is a valid IP address.
		"""
		return GeoNode.ip_check.match(ip) is not None

	def __cmp__(self, other):
		if isinstance(other, GeoNode):
			if other.upper < self.lower:
				return 1
			elif self.upper < other.lower:
				return -1
			else:
				return 0
		else:
			ip = other

			if isinstance(other, str):
				ip = GeoNode.ip2long(other)
			elif not isinstance(other, long):
				raise ValueError("Cannot compare IP address: %s(%s)" % (other.__class__.__name__, str(other)))

			if ip < self.lower:
				return 1
			elif ip > self.upper:
				return -1
			else:
				return 0


class GeoValue(object):
	"""
	GeoValue objects contain information to be returned from a lookup
	"""
	def __init__(self, ip_lower, ip_upper, country_code, country_name):
		self.ip_lower = ip_lower
		self.ip_upper = ip_upper
		self.country_code = country_code
		self.country_name = country_name


class MaxMindGeoLiteASNCSVParser(DbParser):
	"""
	The ASN database parser to load ASN data from the MaxMind CSV
	"""

	fields = {
		"long_lower": 0,
		"long_upper": 1,
		"asn_corp": 2
	}

	def parse(self, path=None):
		if path is None:
			basepath = os.path.dirname(os.path.abspath(__file__))
			path = os.path.join(basepath, "data", "GeoIPASNum2.csv")

		if not os.path.exists(path):
			raise IOError("File not found: %s" % path)

		with open(path) as csvfile:
			asnreader = csv.reader(csvfile)
			for line in asnreader:
				node = self.create_node(line)
				value = self.create_value(line)
				yield (node, value)

	def create_node(self, line):
		"""
		Creates a GeoNode from a line of the parsed CSV file.
		"""
		return GeoNode(long(line[self.fields["long_lower"]]), long(line[self.fields["long_upper"]]))

	def create_value(self, line):
		"""
		Creates an ASNValue from a line of the parsed CSV file.
		"""
		return ASNValue(long(line[self.fields["long_lower"]]), long(line[self.fields["long_upper"]]), line[self.fields["asn_corp"]])


class ASNValue(object):
	def __init__(self, ip_lower, ip_upper, asn):
		self.ip_lower = ip_lower
		self.ip_upper = ip_upper
		self.asn = asn


class GeoDB(object):
	"""
	Container object for the geo tree that allows applications to easily lookup country information by IP address.
	"""
	def __init__(self, csvfile=None, parser=MaxMindGeoLiteCSVParser()):
		treelist = parser.parse(csvfile)
		self.tree = FastAVLTree(treelist)

		# Done with the list, remove it since it can be rather large
		del treelist

	def lookup(self, ip, default=None):
		"""
		Get the GeoValue object for a given IP address

		IP addresses can be either a Long or a dotted-decimal formatted string.
		"""
		return self.tree.get(ip, default)