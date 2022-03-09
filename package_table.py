# HashTable class using chaining.
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining
# Ref: C950 - Webinar 1: Let’s Go Hashing
import csv
from package import *
from datetime import *


class PackageTable:
    truck_manifest = []
    delivery_snapshot = dict()

    # Constructor with optional initial capacity parameter.
    # Our current WGUPS location handles 40 packages a day.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # inserts a package object into the package hashtable
    def insert(self, pack_id, data):  # does both insert and update
        # get the bucket list where this package will go.
        bucket = hash(pack_id) % len(self.table)
        bucket_list = self.table[bucket]

        # update package if it is already in the bucket
        for p in bucket_list:
            if p[0] == pack_id:
                p[1] = data
                return True

        # if not, insert the package to the end of the bucket list.
        package = [pack_id, data]
        bucket_list.append(package)
        return True

    # Searches for a package with matching package ID in the hash table.
    # Returns the package if found, or None if not found.
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
        # get the bucket list where this package will be removed from.
        bucket = hash(pack_id) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the package from the bucket list if it is present.
        for p in bucket_list:
            if p[0] == pack_id:
                bucket_list.remove([p[0], p[1]])

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
                        print(row)
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


# reads CSV of package data and loads package objects into the package hashtable
def initialize_packages(csv_file, my_hash):
    with open(csv_file) as packageCSV:
        reader = csv.reader(packageCSV, delimiter=",")
        # skip the csv header
        next(reader)
        for p in reader:
            pack_id = int(p[0])
            address = p[1]
            city = p[2]
            state = p[3]
            zipcode = p[4]
            if 'EOD' in p[5]:
                deadline = time(17, 00)
            else:
                d = datetime.strptime(p[5], '%H:%M %p')
                deadline = d.time()
            weight = p[6]
            note = p[7]
            status = "AT HUB"

            # create package object
            p = Package(pack_id, address, city, state, zipcode, deadline, weight, note, status)
            # insert package into package hashtable
            my_hash.insert(pack_id, p)


def prioritize_packages(my_hash):
    # create package priority lists to load trucks with
    # create a temporary set to hold special note values
    prio_special = []
    prio_linked = []
    prio_morning = []
    prio_norm = []
    temp = set()

    # search for the package ID in the bucket list
    for p in my_hash.table:
        q = p[0][1]
        # check special notes, put ones containing special notes in priority 2
        if 'DELAYED' in q.note.upper() or 'CAN' in q.note.upper():
            prio_special.append(q)
        elif 'MUST' in q.note.upper():
            temp.update([int(i) for i in q.note.replace(',', "").split() if i.isdigit()])
            # temp.update(temp_list)
            prio_linked.append(q)
        elif q.deadline < time(12, 00):
            prio_morning.append(q)
        else:
            prio_norm.append(q)

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
    prio_linked.sort(key=lambda a: a.address)
    prio_linked.sort(key=lambda d: d.deadline)
    prio_norm.sort(key=lambda a: a.address)
    prio_norm.sort(key=lambda d: d.deadline)
    prio_morning.sort(key=lambda a: a.address)
    prio_morning.sort(key=lambda d: d.deadline)
    prio_special.sort(key=lambda a: a.address)
    prio_special.sort(key=lambda d: d.deadline)
    my_hash.truck_manifest.insert(0, prio_linked)
    my_hash.truck_manifest.insert(1, prio_morning)
    my_hash.truck_manifest.insert(2, prio_norm)
    my_hash.truck_manifest.insert(3, prio_special)

