# Class for the truck object.
from datetime import *


class Truck:
    delivery_order = []
    speed = 18.0
    m_driven = 0.0
    loaded = False
    avail = True

    def __init__(self, number, load):
        self.number = number
        self.load = load
        self.table = []
        # for i in range(load):
            # self.table.append([])

    def load_truck(self, manifest):
        manifest.dock_avail = False
        if self.number == 1:
            while len(self.table) < self.load:
                if len(manifest[0]) != 0:
                    self.table.append(manifest[0][0])
                    manifest[0][0].status = "ON TRUCK"
                    del manifest[0][0]
                elif len(manifest[1]) != 0:
                    self.table.append(manifest[1][0])
                    manifest[1][0].status = "ON TRUCK"
                    del manifest[1][0]
                else:
                    break
        else:
            while len(self.table) < self.load:
                if len(manifest[2]) != 0:
                    self.table.append(manifest[2][0])
                    manifest[2][0].status = "ON TRUCK"
                    del manifest[2][0]
                elif len(manifest[1]) != 0:
                    self.table.append(manifest[1][0])
                    manifest[1][0].status = "ON TRUCK"
                    del manifest[1][0]
                else:
                    break
        self.loaded = True
        manifest.dock_avail = True

    def deliver_packages(self, mh, dm, wt):
        self.avail = False
        a = 'HUB'
        # checks each package against hub
        while len(self.table) > 0:
            x = []
            b = 99999
            for i in self.table:
                c = dm.edge_weights[dm.edge_index.get(a)][dm.edge_index.get(i.address)]
                if c < b:
                    b = c
                    d = i
                    if b == 0:
                        break
            a = d.address
            tod = 60 * (b/self.speed)
            self.m_driven += b
            wt.current_time += timedelta(minutes=tod)
            d.status = 'TRUCK ' + str(self.number) + ' DELIVERED @ ' + str(wt.current_time)
            print(d)
            x = mh.table.copy()
            mh.delivery_snapshot[wt.current_time] = []
            for row in x:
                mh.delivery_snapshot[wt.current_time].append(str(row[0][1]))
            self.table.remove(d)
        ret_miles = dm.edge_weights[dm.edge_index.get(a)][dm.edge_index.get('HUB')]
        self.m_driven += ret_miles
        ret_time = 60 * (ret_miles/self.speed)
        wt.current_time += timedelta(minutes=ret_time)
        print('TRUCK ' + str(self.number) + ' DELIVERY COMPLETE. RETURNING TO HUB.')
        print('--------------------------------------------')
        self.loaded = False
        self.avail = True

    def print_miles_driven(self):
        return round(self.m_driven, 2)

    def truck_operations(self, mh, mm, wt):
        if mh.dock_avail is True and self.loaded is False and self.avail is True:
            self.load_truck(mh)
        elif self.loaded is True and self.avail is True:
            self.deliver_packages(mh, mm, wt)
        else:
            return


