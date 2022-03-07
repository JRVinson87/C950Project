# Class for the truck object.
from datetime import *
from project_time import KeepTime

class Truck:
    delivery_order = []
    speed = 18.0
    m_driven = 0.0
    delivery_num = 1
    work_time = KeepTime()

    def __init__(self, number, load):
        self.number = number
        self.load = load
        self.table = []

    def load_truck(self, manifest):
        if self.number == 1:
            if self.delivery_num == 1:
                while len(self.table) < self.load:
                    if len(manifest[0]) != 0:
                        self.table.append(manifest[0][0])
                        manifest[0][0].status = "ON TRUCK " + str(self.number)
                        del manifest[0][0]
                    elif len(manifest[1]) != 0:
                        self.table.append(manifest[1][0])
                        manifest[1][0].status = "ON TRUCK " + str(self.number)
                        del manifest[1][0]
                    else:
                        break
            else:
                while len(self.table) < self.load:
                    if len(manifest[2]) != 0:
                        self.table.append(manifest[2][0])
                        manifest[2][0].status = "ON TRUCK " + str(self.number)
                        del manifest[2][0]
                    else:
                        break
        else:
            if self.delivery_num == 1:
                while len(self.table) < self.load:
                    if len(manifest[3]) != 0:
                        self.table.append(manifest[3][0])
                        manifest[3][0].status = "ON TRUCK " + str(self.number)
                        del manifest[3][0]
                    elif len(manifest[1]) != 0:
                        self.table.append(manifest[1][0])
                        manifest[1][0].status = "ON TRUCK " + str(self.number)
                        del manifest[1][0]
                    else:
                        break
            else:
                while len(self.table) < self.load:
                    if len(manifest[2]) != 0:
                        self.table.append(manifest[2][0])
                        manifest[2][0].status = "ON TRUCK " + str(self.number)
                        del manifest[2][0]
                    else:
                        break

    def deliver_packages(self, mh, dm):
        print('TRUCK ' + str(self.number) + ' DELIVERY ' + str(self.delivery_num) + ' DEPARTING @ ' + str(self.work_time.current_time))
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
            self.work_time.current_time += timedelta(minutes=tod)
            d.status = 'TRUCK ' + str(self.number) + ' DELIVERED @ ' + str(self.work_time.current_time)
            print(d)
            x = mh.table.copy()
            mh.delivery_snapshot[self.work_time.current_time] = []
            for row in x:
                mh.delivery_snapshot[self.work_time.current_time].append(str(row[0][1]))
            self.table.remove(d)
        ret_miles = dm.edge_weights[dm.edge_index.get(a)][dm.edge_index.get('HUB')]
        self.m_driven += ret_miles
        ret_time = 60 * (ret_miles/self.speed)
        self.work_time.current_time += timedelta(minutes=ret_time)
        print('TRUCK ' + str(self.number) + ' DELIVERY ' + str(self.delivery_num) + ' COMPLETE. RETURNED TO HUB.')
        print('---------------------------------------------\n')
        self.delivery_num += 1

    def print_miles_driven(self):
        return round(self.m_driven, 2)

