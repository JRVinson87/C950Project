# HashTable class using chaining.
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining
# Ref: C950 - Webinar 1: Let’s Go Hashing
import csv
from package import *
from datetime import *


class PackageTable:
    truck_manifest = []
    delivery_snapshot = dict()
    dock_avail = True

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

    def snapshot(self, t):
        h = int(t.split(':')[0])
        m = int(t.split(':')[1])
        search_time = datetime.combine(date.today(), time(hour=h, minute=m))
        print(search_time)
        for k, v in self.delivery_snapshot.items():
            if search_time > k:
                x = v
            else:
                break
        for row in x:
            print(row)


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
                deadline = time(20, 00)
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
    priority0 = []
    priority1 = []
    priority2 = []
    temp = set()

    # search for the package ID in the bucket list
    for p in my_hash.table:
        q = p[0][1]
        # check special notes, put ones containing special notes in priority 2
        if 'DELAYED' in q.note.upper() or 'CAN' in q.note.upper():
            priority2.append(q)
        elif 'MUST' in q.note.upper():
            temp.update([int(i) for i in q.note.replace(',', "").split() if i.isdigit()])
            # temp.update(temp_list)
            priority0.append(q)
        else:
            priority1.append(q)

    counter = 0
    for i in priority1:
        if len(temp) < 1:
            break
        elif i.pack_id in temp:
            priority0.append(i)
            temp.remove(i.pack_id)
            priority1.insert(0, [])
            priority1.remove(i)
            counter += 1

    del priority1[:counter]
    priority0.sort(key=lambda a: a.address)
    priority0.sort(key=lambda d: d.deadline)
    priority1.sort(key=lambda a: a.address)
    priority1.sort(key=lambda d: d.deadline)
    priority2.sort(key=lambda a: a.address)
    priority2.sort(key=lambda d: d.deadline)
    my_hash.truck_manifest.insert(0, priority0)
    my_hash.truck_manifest.insert(1, priority1)
    my_hash.truck_manifest.insert(2, priority2)

