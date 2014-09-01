from setuptools import setup, find_packages

setup(name="FastGeo",
		description="A fast, in-memory GeoIP data lookup module",
		download_url="https://github.com/theanti9/FastGeo/releases/download/v0.1.2-alpha/FastGeo-0.1.2-py2.7.egg",
		long_description=open("README.md", 'r').read(),
		author="Ryan Merl",
		author_email="ryan@ryanmerl.com",
		url="https://github.com/theanti9/FastGeo",
		version="0.1.3",
		install_requires=[
			"bintrees>=2.0.1"
		],
		classifiers=[
			"Development Status :: 3 - Alpha",
			"Intended Audience :: Developers",
			"Programming Language :: Python",
			"License :: OSI Approved :: MIT License",
			"Topic :: Database",
			"Topic :: Internet",
			"Topic :: Software Development :: Libraries"
		],
		license="MIT",
		platforms=('Any',),
		keywords='geo geoip lookup db',
		packages=find_packages(exclude="tests"),
		package_dir={"FastGeo": "FastGeo"},
		package_data={"FastGeo": ["data/*.csv"]},
		)

