import numpy as np
import random
from random import expovariate
import matplotlib.pyplot as plt

random.seed(2)


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
        self.info = {
            'client_num': self.client_num,
            'waiting_time_sum': 0,
            # add here what u want
        }

    def add_client(self, client):
        self._running_diff += client.entry_diff

        if self.client_num < self.capacity:
            self.queue.append(client)
            self.client_num += 1

    def remove_client(self):
        if self.queue[0].served:
            self.queue.pop(0)
            self.client_num-=1

    def processing(self, client):

        self.add_client(client)

        if self._running_diff >= self._running_serve:
            self._running_serve += self.queue[0].serve_time
            self.queue[0].served = True

        if self._running_diff >= self._running_serve and self.client_num!=0:
            self.remove_client()


def vis_num_of_clients_in_time(iterations, lambd, mu):
    server = Server(capacity=capacity)

    first_client = Client(lambd, mu)
    first_client.entry_diff = 0
    server.processing(first_client)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations):
        server.processing(Client(lambd, mu))
        result[i] = server.client_num

    plt.plot(range(iterations), result)
    plt.show()


if __name__ == '__main__':
    lambd = 100
    mu = 200
    capacity = 1000
    iterations = 10000

    vis_num_of_clients_in_time(iterations, lambd, mu)


