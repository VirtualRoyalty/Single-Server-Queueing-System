import numpy as np
import random
from random import expovariate
import matplotlib.pyplot as plt
import collections

random.seed(32)


class Client(object):
    def __init__(self, lambd, mu):
        self.lambd = lambd
        self.mu = mu
        self.entry_diff = expovariate(self.lambd)
        self.serve_time = expovariate(self.mu)
        self.served = False
        # self.info = {
        #     'serve_time': 0,
        #     'waiting_time': 0,
        #     'sojourn': 0
        # }


class Server(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.client_num = 0
        self.queue = []
        self._running_serve = 0
        self._running_diff = 0
        # self.info = {
        #     'client_num': [],
        #     'time': [],
        # }
        self.exp_dict = {}

    def add_client(self, client):
        self._running_diff += client.entry_diff
        # if self._running_diff > self._running_serve and self.client_num>1:
        #     self._running_serve = self._running_diff
        if self.client_num < self.capacity:
            self.queue.append(client)
            self.client_num += 1
        self.exp_dict[self._running_diff] = self.client_num

    def remove_client(self):

        while True:
            if self._running_diff > self._running_serve:
                self.queue.pop(0)
                self.client_num -= 1
                self.exp_dict[self._running_serve] = self.client_num

                if self.client_num == 1:
                    self._running_serve = self._running_diff

                self._running_serve+=self.queue[0].serve_time

            else:
                break

            # else:
            #     break

    def processing(self, client):

        self.add_client(client)


        if self._running_diff > self._running_serve:
            self.remove_client()


def vis_num_of_clients_in_time(iterations, lambd, mu):
    server = Server(capacity=capacity)

    first_client = Client(lambd, mu)
    first_client.entry_diff = 0
    server._running_diff = first_client.serve_time
    server.processing(first_client)


    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations):
        server.processing(Client(lambd, mu))

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()))
    plt.scatter(list(od.keys()), list(od.values()))
    plt.grid()
    plt.show()


def test():
    server = Server(capacity=capacity)

    c1 = Client(1,1)
    c1.entry_diff = 0
    c1.serve_time = 5
    c2 = Client(1,1)
    c2.entry_diff = 1
    c2.serve_time = 1
    c3 = Client(1,1)
    c3.entry_diff = 1
    c3.serve_time = 1
    c4 = Client(1,1)
    c4.entry_diff = 1
    c4.serve_time = 2
    c4 = Client(1,1)
    c4.entry_diff = 1
    c4.serve_time = 2
    c5 = Client(1,1)
    c5.entry_diff = 8
    c5.serve_time = 2

    clients = [c1, c2, c3, c4, c5]

    server._running_serve = c1.serve_time
    for cl in clients:
        server.processing(cl)

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()))
    plt.scatter(list(od.keys()), list(od.values()))
    plt.grid()
    plt.show()

if __name__ == '__main__':
    lambd = 10 / 100
    mu = 100 / 100
    capacity = 1000
    iterations = 10

    # vis_num_of_clients_in_time(iterations,lambd, mu)
    test()


