# Aggregator Broker
MQTT message broker that aggregates data to an SQL data base

# installation
- This code runs with runs with Python 3.7.
- The code has been packaged using [setup.py](setup.py). It can be installed with the requirements using:

`$ pip install .`

-The configuration [configuration.conf](configuration.conf) file contains the configuration of:
 - The database
 - The MQTT 
 - The message handler

- After configuring the database, create the table 'machine_statistics' using the script in [init_db](init_db) folder (the sql script directly or using the python script)
- The main script to run is [aggregatorbroker.py](aggregatorbroker.py)

# Notes
[my notes](NOTES.md)