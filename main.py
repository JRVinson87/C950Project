# Name: Joshua Vinson ID: 007197656
from nodes import *
from package_table import *
from truck import *
from project_time import KeepTime


"""
Time complexity for the entire program is O(n^2) because that is the max in the worst case scenarios.
The other O(n) loops will never grow as fast as the O(n^2) nearest neighbor delivery algorithm.
The space complexity is O(n) which is the total number of packages. Packages can have
duplicate addresses so the distance adjacency matrix won't grow in line with the number of packages.
"""
print('Would you like to load data and start the work day?')
start = input('Enter 1 to start or any other key to exit: ')
if start == "1":
    print('Today\'s delayed air cargo arrival ship out time is 9:05.')
    print('Loading packages and beginning work day.\n')
    my_matrix = Matrix()
    # Initialize with number of packages for the day.
    my_hash = PackageTable(40)
    # Initialize trucks with their truck number and number of packages they can hold.
    truck1 = Truck(1, 16)
    truck2 = Truck(2, 16)
    # Set truck 2's start time for the delayed packages, project_time.py
    truck2.work_time = KeepTime('9:05')
    load_nodes('wgups_distance.csv', my_matrix)
    initialize_packages('wgups_packages.csv', my_hash)
    prioritize_packages(my_hash)
    """
    Check the list of lowest priority packages. 
    While there are still packages to be delivered, load trucks and deliver them.
    """
    while len(my_hash.truck_manifest[2]) != 0:
        truck1.load_truck(my_hash.truck_manifest)
        truck2.load_truck(my_hash.truck_manifest)
        truck1.deliver_packages(my_hash, my_matrix)
        truck2.deliver_packages(my_hash, my_matrix)

    print('ALL DELIVERIES FINISHED.')
    print('TOTAL MILES DRIVEN BY TRUCK 1: ' + str(truck1.print_miles_driven()))
    print('TOTAL MILES DRIVEN BY TRUCK 2: ' + str(truck2.print_miles_driven()))
    print('TOTAL COMBINED MILES: ' + str(truck2.print_miles_driven() + truck1.print_miles_driven()))
    print('---------------------------')

    my_hash.snapshot()

else:
    print('Exiting.')

