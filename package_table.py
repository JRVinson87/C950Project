# HashTable class using chaining.
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining
# Ref: C950 - Webinar 1: Let’s Go Hashing
import csv
from package import *
from datetime import *


# Class to create a hash table to store the packages of the day.
class PackageTable:
    # Creates a master truck manifest.
    truck_manifest = []
    # Creates a dictionary to store a timed copy of the package hashtable after every delivery.
    delivery_snapshot = dict()

    # Constructor with optional initial capacity parameter.
    # Our current WGUPS location handles 40 packages a day.
    def __init__(self, initial_capacity):
        # Initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    """
    Hashes passed in package ID. 
    Checks current package table for the passed in package ID.
    If found, updates that package.
    If not found, inserts a package object into the package hashtable.
    """
    def insert(self, pack_id, data):  # does both insert and update
        # Check list.
        bucket = hash(pack_id) % len(self.table)
        bucket_list = self.table[bucket]

        # Update.
        for p in bucket_list:
            if p[0] == pack_id:
                p[1] = data
                return True

        # Insert.
        package = [pack_id, data]
        bucket_list.append(package)
        return True

    """
    Hashes passed in package ID and searches package table.
    If the package is found, the package data is returned.
    If it is not found, None is returned.
    """
    def lookup(self, pack_id):
        # get the bucket list where this package would be.
        bucket = hash(pack_id) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the package ID in the bucket list
        for p in bucket_list:
            if p[0] == pack_id:
                return p[1]
        return None

    # Removes a package with matching key from the hash table.
    def remove(self, pack_id):
        # Hash the package ID and check if it's in the table.
        bucket = hash(pack_id) % len(self.table)
        bucket_list = self.table[bucket]

        # Remove the package from the table if it is present.
        for p in bucket_list:
            if p[0] == pack_id:
                bucket_list.remove([p[0], p[1]])

    """
    Function to perform package "snapshot" operations.
    Asks the user for a specified time to check and then looks up the stored snapshot of package data.
    The user can print the data for all packages or a specified package.
    """
    def snapshot(self):
        while True:
            start = input('\nEnter 1 to check a snapshot of package status or 2 to exit: ')
            if start == "1":
                try:
                    t = input('What time would you like to search for? (24 hour format XX:XX): ')
                    datetime.strptime(t, '%H:%M')
                except ValueError:
                    print('Invalid entry. Please use 24 hour format XX:XX.')
                    continue

                h = int(t.split(':')[0])
                m = int(t.split(':')[1])
                search_time = datetime.combine(date.today(), time(hour=h, minute=m))
                # Look through snapshot items by time.
                # Return the time closest to, but not greater than, the users time input.
                for k, v in self.delivery_snapshot.items():
                    if search_time > k:
                        x = v
                    else:
                        break
                start_2 = input('Enter "ALL" to see all packages or enter a specific package ID: ')
                if start_2.upper() == 'ALL':
                    print('\nSTATUS OF ALL PACKAGES AT ' + str(search_time))
                    print('--------------------------------------')
                    for row in x:
                        print('Package ID: ' + str(row))
                elif start_2.isdigit():
                    nf = True
                    for row in x:
                        if start_2 == row.replace(',', "").split()[0]:
                            nf = False
                            print(row)
                    if nf:
                        print('Package ID not found.')
                else:
                    print('Invalid entry.')
            elif start == "2":
                print('Exiting')
                return
            else:
                print("Invalid input.")
                continue


# Reads CSV of package data and loads package objects into the package hashtable.
def initialize_packages(csv_file, my_hash):
    with open(csv_file) as packageCSV:
        reader = csv.reader(packageCSV, delimiter=",")
        # Skip the csv header
        next(reader)
        for p in reader:
            pack_id = int(p[0])
            address = p[1]
            city = p[2]
            state = p[3]
            zipcode = p[4]
            """
            Check the deadline. 
            If it is "EOD" (end of day), then replace it with the actual end of day time, 17:00.
            If it is a written time, turn it into a proper time object.
            """
            if 'EOD' in p[5]:
                deadline = time(17, 00)
            else:
                d = datetime.strptime(p[5], '%H:%M %p')
                deadline = d.time()
            weight = p[6]
            note = p[7]
            status = "AT HUB"

            # Create package object.
            p = Package(pack_id, address, city, state, zipcode, deadline, weight, note, status)
            # Insert package into package hashtable.
            my_hash.insert(pack_id, p)


# Function to prioritize the days packages to meet constraints and deadlines.
def prioritize_packages(my_hash):
    # Create package priority lists to load trucks.
    prio_special = []
    prio_linked = []
    prio_morning = []
    prio_norm = []
    # Create a temporary set to hold special note values.
    temp = set()

    # Iterate through package hash table.
    for p in my_hash.table:
        q = p[0][1]
        # Check special notes.
        # Put ones containing special notes in special priority.
        if 'DELAYED' in q.note.upper() or 'CAN' in q.note.upper():
            prio_special.append(q)
        # Put ones that are linked with others, into linked priority.
        # Keep track of all linked package ID's in temp set.
        elif 'MUST' in q.note.upper():
            temp.update([int(i) for i in q.note.replace(',', "").split() if i.isdigit()])
            prio_linked.append(q)
        # Check deadline, put early deliveries in morning priority.
        elif q.deadline < time(12, 00):
            prio_morning.append(q)
        # All others go in normal priority.
        else:
            prio_norm.append(q)

    """
    Check the normal priority list for any package ID's that are linked to
    packages in the linked list. If a package is found, add it to the linked list
    and remove it from the normal list. In order to not lose the correct current index
    location in the for loop, add a [] to the front of the normal list.
    Keep a counter for how many entries are added to the front of the normal list
    and then delete that number of entries from the front of the normal list after
    the for loops is completed.
    """
    counter = 0
    for i in prio_norm:
        if len(temp) < 1:
            break
        elif i.pack_id in temp:
            prio_linked.append(i)
            temp.remove(i.pack_id)
            prio_norm.insert(0, [])
            prio_norm.remove(i)
            counter += 1
    del prio_norm[:counter]

    # Sort all the priority lists by address and deadline.
    prio_linked.sort(key=lambda a: a.address)
    prio_linked.sort(key=lambda d: d.deadline)
    prio_norm.sort(key=lambda a: a.address)
    prio_norm.sort(key=lambda d: d.deadline)
    prio_morning.sort(key=lambda a: a.address)
    prio_morning.sort(key=lambda d: d.deadline)
    prio_special.sort(key=lambda a: a.address)
    prio_special.sort(key=lambda d: d.deadline)

    # Insert the priority lists into the truck manifest in order of priority.
    my_hash.truck_manifest.insert(0, prio_linked)
    my_hash.truck_manifest.insert(1, prio_morning)
    my_hash.truck_manifest.insert(2, prio_norm)
    my_hash.truck_manifest.insert(3, prio_special)

