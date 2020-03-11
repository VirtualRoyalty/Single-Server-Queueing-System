import numpy as np
import random
from random import expovariate
import pylab
import matplotlib.pyplot as plt
from queue import Queue

# random.seed(3)

class Server(object):
    def __init__(self, server_rate, capacity):
        self.capacity = capacity
        # self.prev_clients_info
        self.serve_prev_client_time = 0
        self.server_rate = server_rate
        self.queue = []
        self._running_serve = 0
        self._running_diff = 0
        self.client_num = 0

    def serve(self, client):
        # waiting time for i client is the time difference
        # between serving time of previous (that is i-1) client and
        # entry time for new (i) client
        client.waiting_time = \
            max(0, self.serve_prev_client_time - client.entry_diff)

        # random exponential serving time of client
        client.serve_time = expovariate(self.server_rate)

        # just sum of waiting and serving
        client.update_sojourn()

        # update info about
        self.serve_prev_client_time = client.serve_time
        self._running_serve += client.serve_time
        return

    def add_client(self, client):
        self._running_diff += client.entry_diff
        if self.client_num < self.capacity:
            self.queue.append(client)
            self.client_num += 1
            self.serve(self.queue[0])
        soj_time = self.remove_client(self.queue[0])
        if soj_time is not None:
            return soj_time

    def remove_client(self, client):
        if self._running_diff > self._running_serve:
            excluded = self.queue.pop(0)
            self.client_num -= 1
            # self._running_diff -= (excluded.entry_diff+excluded.serve_time)
            return excluded.serve_time
        return None

    # def get_diff_sum(self):
    #     diff_sum = sum([client for client.entry_diff in self.queue])

class Client(object):
    def __init__(self, ratio):
        self.ratio = ratio
        self.entry_diff = expovariate(self.ratio)
        self.serve_time = 0
        self.waiting_time = 0
        self.sojourn = -1


    def update_sojourn(self):
        self.sojourn = self.serve_time + self.waiting_time


lambd = 10  # entry flow
mu = 9  # exit flow

# client_per_hour /= 100
# serve_possibility /= 100

# c = Client(client_per_hour/100)
s = Server(mu, capacity=5)

results = []

def mean_sojourn_time():
    for i in range(10000):
        c = Client(lambd)
        sojourn_time_of_last_client = s.add_client(c)
        if sojourn_time_of_last_client is not None:
            results.append(sojourn_time_of_last_client)


    # plt.plot(range(0, len(results)), results)
    # plt.show()
    pylab.hist(results, bins=50)
    pylab.show()


def mean_clients_num():
    for i in range(10000):
        c = Client(lambd)
        sojourn_time_of_last_client = s.add_client(c)
        if sojourn_time_of_last_client is not None:
            results.append(sojourn_time_of_last_client)

    # plt.plot(range(0, len(results)), results)
    # plt.show()
    pylab.hist(results, bins=50)
    pylab.show()