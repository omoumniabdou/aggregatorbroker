from distutils.core import setup

setup(
    name='aggregatorbroker',
    version='1.0',
    package_dir={'': 'aggregatorbroker'},
    url='https://github.com/othmanemoumni88/aggregatorbroker',
    license='Apache-2.0',
    author='Othman Moumni Abdou',
    author_email='othman.moumniabdou@gmail.com',
    description='MQTT broker that aggregates data to an SQL data base', requires=['paho-mqtt']
)
