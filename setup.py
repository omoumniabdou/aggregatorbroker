from distutils.core import setup

setup(
    name='aggregatorbrocker',
    version='1.0',
    package_dir={'': 'aggregatorbrocker'},
    url='https://github.com/othmanemoumni88/aggregatorbrocker',
    license='Apache-2.0',
    author='Othman Moumni Abdou',
    author_email='othman.moumniabdou@gmail.com',
    description='MQTT brocker that aggregates data to an SQL data base', requires=['paho-mqtt']
)
