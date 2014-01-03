FastGeo
=======

A fast, flexible, in-memory GeoIP lookup library.

By default FastGeo will use the GeoLite country database, distributed free by MaxMind. It contains IP ranges and the countries they're assigned to. The library can easily be extended (and will be later) to use the GeoLite database to also contain city and lat/lon data. 


Usage
=====

```
from FastGeo import GeoDB
geo = GeoDB()
node = geo.lookup("173.194.43.8")
print node.country_code # "US"
print node.country_name # "United States"
```

Some IPs will not be found in the database. In this case `.lookup()` will return `None`

```
node = geo.lookup("127.0.0.1")
if node:
  print node.country_name
else:
  print "Not found!"
```

The `.lookup()` function will take a string IP address or it's Long representation

```
> geo.lookup("173.194.43.8") == geo.lookup(2915183368L)
True
```
  

**Note**: It is recommended that the `GeoDB` object be instantiated at startup and not on demand as it can take a few seconds to load and parse the database file.

The `GeoDB` constructor will accept the path to a CSV file, although it defaults to the file distributed with the library.

The default parser assumes the following csv format:

"&lt;ip lower bound&gt;","&lt;ip upper bound&gt;","&lt;long lower bound&gt;","&lt;long upper bound&gt;","&lt;country code&gt;","&lt;country name&gt;"

To parse other formats, inherit from `FastGeo.parsers.DbParser` and implement `.parse()`, `.create_node()`, and `.create_value()`. To use the parser, pass a new instance to the `GeoDB` constructor.





This product includes GeoLite data created by MaxMind, available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.
