# Class for the truck object.
from datetime import *
from project_time import KeepTime


class Truck:
    # Average speed in mph.
    speed = 18.0
    # Initialize miles driven to 0.
    m_driven = 0.0
    # Initialize delivery dispatch from the hub to 1.
    delivery_num = 1
    # Initialize a datetime object to keep track of delivery times.
    work_time = KeepTime()

    def __init__(self, number, load):
        # Truck number.
        self.number = number
        # Truck's max number of packages.
        self.load = load
        # Truck's list of packages that it is carrying.
        self.table = []

    """
    Function to load trucks from the master truck manifest of prioritized package lists.
    The truck checks to see if it is at it's max capacity after each package loaded and then stops.
    Truck 1 is prioritized to deliver linked packages and morning deliveries first in order
    to meet deadlines. After those packages are all delivered it will load and deliver normal priority.
    Truck 2 is prioritized to wait for delayed deliveries and then deliver those and
    any remaining morning deliveries. After those are all delivered it will check for normal priority.
    """
    def load_truck(self, manifest):
        # Check truck number.
        if self.number == 1:
            # Check if morning/first delivery.
            if self.delivery_num == 1:
                while len(self.table) < self.load:
                    # Linked priority.
                    if len(manifest[0]) != 0:
                        self.table.append(manifest[0][0])
                        manifest[0][0].status = "EN ROUTE ON TRUCK " + str(self.number)
                        del manifest[0][0]
                    # Morning priority.
                    elif len(manifest[1]) != 0:
                        self.table.append(manifest[1][0])
                        manifest[1][0].status = "EN ROUTE ON TRUCK " + str(self.number)
                        del manifest[1][0]
                    else:
                        break
            else:
                while len(self.table) < self.load:
                    # Normal priority.
                    if len(manifest[2]) != 0:
                        self.table.append(manifest[2][0])
                        manifest[2][0].status = "EN ROUTE ON TRUCK " + str(self.number)
                        del manifest[2][0]
                    else:
                        break
        else:
            if self.delivery_num == 1:
                while len(self.table) < self.load:
                    # Special/delayed priority.
                    if len(manifest[3]) != 0:
                        self.table.append(manifest[3][0])
                        manifest[3][0].status = "EN ROUTE ON TRUCK " + str(self.number)
                        del manifest[3][0]
                    elif len(manifest[1]) != 0:
                        self.table.append(manifest[1][0])
                        manifest[1][0].status = "EN ROUTE ON TRUCK " + str(self.number)
                        del manifest[1][0]
                    else:
                        break
            else:
                while len(self.table) < self.load:
                    if len(manifest[2]) != 0:
                        self.table.append(manifest[2][0])
                        manifest[2][0].status = "EN ROUTE ON TRUCK " + str(self.number)
                        del manifest[2][0]
                    else:
                        break

    """
    Function with algorithm to deliver packages. Uses a nearest neighbor type of algorithm.
    A while loop is used to check each package loaded onto the truck. Starting at the HUB, 
    a for loop checks the distance adjacency matrix for distances between the trucks current
    location and destination. For example, the first iteration checks the distance between the
    HUB and each packages address. Each distance entry is stored in a variable. Each iteration
    checks the destination to see if it is smaller than the previous. If it is, the new smaller
    distance is stored and that package is not checked again. After each package is checked, 
    the nearest neighbor to the trucks current location is driven to, the time to get there is 
    recorded, the miles driven are recorded, and a snapshot of the package hashtable is taken 
    and added to a dictionary. Finally, the return trip to the HUB is recorded and the truck
    ups it's delivery number in preparation for another delivery.
    """
    def deliver_packages(self, mh, dm):
        print('TRUCK ' + str(self.number) + ' DELIVERY ' + str(self.delivery_num) + ' DEPARTING @ ' + str(self.work_time.current_time))
        a = 'HUB'
        # Run nearest neighbor algorithm until all packages are in queue for delivery.
        while len(self.table) > 0:
            b = 99999
            for i in self.table:
                # Look up distance between current location and package in distance adjacency matrix.
                c = dm.edge_weights[dm.edge_index.get(a)][dm.edge_index.get(i.address)]
                # If new distance is smaller than previous, store new data.
                if c < b:
                    b = c
                    d = i
                    # If distance is 0, the package is going to the same address.
                    # Break out of loop to save time.
                    if b == 0:
                        break
            a = d.address
            # Time taken to deliver.
            tod = 60 * (b/self.speed)
            # Record miles driven.
            self.m_driven += b
            # Record delivery time.
            self.work_time.current_time += timedelta(minutes=tod)
            d.status = 'TRUCK ' + str(self.number) + ' DELIVERED @ ' + str(self.work_time.current_time)
            print(d)
            # Create snapshot of package hashtable for future reference.
            x = mh.table.copy()
            mh.delivery_snapshot[self.work_time.current_time] = []
            for row in x:
                mh.delivery_snapshot[self.work_time.current_time].append(str(row[0][1]))
            self.table.remove(d)
        # Record return to HUB time and miles.
        ret_miles = dm.edge_weights[dm.edge_index.get(a)][dm.edge_index.get('HUB')]
        self.m_driven += ret_miles
        ret_time = 60 * (ret_miles/self.speed)
        self.work_time.current_time += timedelta(minutes=ret_time)
        print('TRUCK ' + str(self.number) + ' DELIVERY ' + str(self.delivery_num) + ' COMPLETE. RETURNED TO HUB.')
        print('---------------------------------------------\n')
        self.delivery_num += 1

    # Function for printing given trucks total miles.
    def print_miles_driven(self):
        return round(self.m_driven, 2)

