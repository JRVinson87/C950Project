# Class to define a package object.
# Ref: C950 - Webinar 2: Getting Greedy, who moved my data?



class Package:
    def __init__(self, pack_id, address, city, state, zipcode, deadline, weight, note, status):
        self.pack_id = pack_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.note = note
        self.status = status

    # overwrite the method for printing the package so that it prints the values instead of the reference
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.pack_id, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline, self.weight, self.note, self.status)

