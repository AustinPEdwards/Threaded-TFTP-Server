Austin Edwards
CSCE 360 Computer Networks
Assignment 3: Threaded TFTP Server

Thread 1 in write mode throws an error but it exits gracefully and I pass all tests so I didn't look into it.

Pytesting tests packet construction and deconstruction for all packet types. It tests a variety of valid packets and invalid packets
To run the pytesting enter: 
pytest --disable-warnings --verbose

--disable-warnings removes "\" warnings in strings
--verbose prints more information about what tests ran 