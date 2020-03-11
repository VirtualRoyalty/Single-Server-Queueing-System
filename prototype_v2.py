import numpy as np
import random
from random import expovariate
import matplotlib.pyplot as plt
import collections

# random.seed(31)


class Client(object):
    def __init__(self, lambd, mu, id=0):
        self.lambd = lambd
        self.mu = mu
        self.entry_diff = expovariate(self.lambd)
        self.serve_time = expovariate(self.mu)
        self.id = id
        self.entry_moment = 0

class Server(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.client_num = 0
        self.queue = []
        self._running_serve = 0
        self._running_diff = 0
        self.exp_dict = {0:0}
        self.waiting_time = {}

    def add_client(self, client):
        self._running_diff += client.entry_diff
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

                self._running_serve += self.queue[0].serve_time

            else:
                break


    def processing(self, client):

        self._running_diff += client.entry_diff
        client.entry_moment = self._running_diff

        if self.client_num == 0:  # for the first client
            self._running_serve = self._running_diff + client.serve_time
            self.waiting_time[client.id] = 0


        if self.client_num < self.capacity:
            self.queue.append(client)
            self.client_num += 1


        while True:
            if self._running_diff >= self._running_serve:
                self.waiting_time[self.queue[1].id] = self.waiting_time[self.queue[0].id] + \
                                                   self.queue[0].serve_time
                self.queue.pop(0)
                self.client_num -= 1

                self.exp_dict[self._running_serve] = self.client_num - 1

                if self.client_num == 1:
                    self._running_serve = self._running_diff

                self._running_serve += self.queue[0].serve_time
            else:
                break

        self.exp_dict[self._running_diff] = self.client_num


def states_prob(capacity, dict):
    states_count = np.zeros(capacity + 1)
    for state in dict.values():
        states_count[state] += 1

    for num in states_count:
        num = num / len(dict)

    return states_count



def mean_state(states_prob):
    sum_mean = 0
    for i in len(states_prob):
        sum_mean += i * states_prob[i]

    return sum_mean




def vis_num_of_clients_in_time(iterations, lambd, mu):
    server = Server(capacity=capacity)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations):
        server.processing(Client(lambd, mu, i))

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()))
    plt.scatter(list(od.keys()), list(od.values()))
    plt.grid()
    plt.show()


def test():
    server = Server(capacity=capacity)

    c1 = Client(1,1,1)
    c1.entry_diff = 1
    c1.serve_time = 5
    c2 = Client(1,1,2)
    c2.entry_diff = 1
    c2.serve_time = 1
    c3 = Client(1,1,3)
    c3.entry_diff = 1
    c3.serve_time = 1
    c4 = Client(1,1,4)
    c4.entry_diff = 1
    c4.serve_time = 2
    c4 = Client(1,1,5)
    c4.entry_diff = 1
    c4.serve_time = 2
    c5 = Client(1,1,6)
    c5.entry_diff = 8
    c5.serve_time = 2

    clients = [c1, c2, c3, c4, c5]

    for cl in clients:
        server.processing(cl)

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()))
    plt.scatter(list(od.keys()), list(od.values()))
    plt.grid()
    plt.show()

if __name__ == '__main__':
    lambd = 100 / 100
    mu = 100 / 100
    capacity = 5
    iterations = 1000

    vis_num_of_clients_in_time(iterations,lambd, mu)
    # test()