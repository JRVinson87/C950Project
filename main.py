# Name: Joshua Vinson ID: 007197656
import multiprocessing

from nodes import *
from package_table import *
from truck import *
from project_time import KeepTime


print('Would you like to load data and start the work day?')
start = input('1 to start or 2 to exit: ')
if start == "1":
    print('Today\'s delayed air cargo arrival ship out time is 9:05.')
    print('Loading packages and beginning work day.\n')
    #work_time = KeepTime()
    # create a graph instance
    my_matrix = Matrix()
    # create a hashtable instance
    my_hash = PackageTable(40)
    truck1 = Truck(1, 16)
    truck2 = Truck(2, 16)
    truck2.work_time = KeepTime('9:05')
    load_nodes('wgups_distance.csv', my_matrix)
    initialize_packages('wgups_packages.csv', my_hash)
else:
    print('Exiting.')


prioritize_packages(my_hash)

while len(my_hash.truck_manifest[2]) != 0:
    truck1.load_truck(my_hash.truck_manifest)
    truck2.load_truck(my_hash.truck_manifest)
    truck1.deliver_packages(my_hash, my_matrix)
    truck2.deliver_packages(my_hash, my_matrix)

"""
print('---------------------------')
user_input = "10:20"
my_hash.snapshot(user_input)
print('---------------------------')
"""
print('ALL DELIVERIES FINISHED.')
print('TOTAL MILES DRIVEN BY TRUCK 1: ' + str(truck1.print_miles_driven()))
print('TOTAL MILES DRIVEN BY TRUCK 2: ' + str(truck2.print_miles_driven()))
print('TOTAL COMBINED MILES: ' + str(truck2.print_miles_driven() + truck1.print_miles_driven()))
print('---------------------------')

my_hash.snapshot()
"""
start_2 = input('Enter 1 to check a snapshot of package status or 2 to exit: ')
if start_2 == "1":
    user_input = input('What time would you like to search for? (24 hour format XX:XX): ')
    my_hash.snapshot(user_input)
else:
    print('Exiting')
"""

"""
for row in range(len(my_hash.table)):
    # looks up ID 1 to 40 via lookup
    print(my_hash.lookup(row+1))

    #print(row)
"""

