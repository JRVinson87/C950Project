# Name: Joshua Vinson ID: 007197656
import multiprocessing

from nodes import *
from package_table import *
from truck import *
from project_time import KeepTime


print('Would you like to load data and start the work day?')
start = input('1 to start or 2 to exit: ')
if start == "1":
    work_time = KeepTime()
    # create a graph instance
    my_matrix = Matrix()
    # create a hashtable instance
    my_hash = PackageTable(40)
    truck1 = Truck(1, 16)
    truck2 = Truck(2, 16)
    print('\nLoading packages and beginning work day.')
    load_nodes('wgups_distance.csv', my_matrix)
    initialize_packages('wgups_packages.csv', my_hash)
else:
    print('Exiting.')


prioritize_packages(my_hash)

while len(my_hash.truck_manifest[1]) != 0:
    process1 = multiprocessing.Process(target=truck1.truck_operations(my_hash, my_matrix, work_time))
    process2 = multiprocessing.Process(target=truck2.truck_operations(my_hash, my_matrix, work_time))
    """
    truck1.load_truck(my_hash.truck_manifest)
    truck2.load_truck(my_hash.truck_manifest)

    truck1.deliver_packages(my_hash, my_matrix, work_time)
    if work_time.current_time > work_time.delayed_time:
        truck2.deliver_packages(my_hash, my_matrix, work_time)
        """

print('---------------------------')
user_input = "10:20"
my_hash.snapshot(user_input)
print('---------------------------')

print(truck1.print_miles_driven())
print(truck2.print_miles_driven())
print(truck2.print_miles_driven() + truck1.print_miles_driven())
"""
start_2 = input('Enter 1 to check a snapshot of package status or 2 to exit: ')
if start_2 == "1":
    user_input = input('What time would you like to search for? (24 hour format XX:XX): ')
    my_hash.snapshot(user_input)
else:
    print('Exiting')
    """


#for row in range(len(my_hash.table)):
    # looks up ID 1 to 40 via lookup
    #print(my_hash.lookup(row+1))

    #print(row)


