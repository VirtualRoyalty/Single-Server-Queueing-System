import numpy as np
import random
from random import expovariate
import pylab
import matplotlib.pyplot as plt
from queue import Queue

class Server(object):
    def __init__(self, server_rate, capacity):
        self.capacity = capacity
        # self.prev_clients_info
        self.serve_prev_client_time = 0
        self.server_rate = server_rate
        self.queue = []
        self._diff_sum = 0
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
        return

    def add_client(self, client):
        self._diff_sum += client.entry_diff
        if self.client_num < self.capacity:
            self.queue.append(client)
            self.client_num+=1
            self.serve(self.queue[0])
        self.remove_client(self.queue[0])
        return

    def remove_client(self, client):
        if self._diff_sum > client.serve_time:
            self.queue.pop(0)
            self.client_num -= 1
            self._diff_sum = 0


    # def get_diff_sum(self):
    #     diff_sum = sum([client for client.entry_diff in self.queue])

class Client(object):
    def __init__(self, ratio):
        self.ratio = ratio
        self.entry_diff = expovariate(self.ratio)
        self.serve_time = 0
        self.waiting_time = 0

    def update_sojourn(self):
        self.sojourn = self.serve_time + self.waiting_time


client_per_hour = 10
serve_possibility = 10

# client_per_hour /= 100
# serve_possibility /= 100

# c = Client(client_per_hour/100)
s = Server(serve_possibility, 100)

results = []

for i in range(10000):
    c = Client(client_per_hour)
    s.add_client(c)
    results.append(s.client_num)


plt.plot(range(0, len(results)), results)
plt.show()
# pylab.hist(results, bins=25)
# pylab.show()
