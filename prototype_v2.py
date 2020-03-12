import numpy as np
import random
from random import expovariate
import matplotlib.pyplot as plt
import collections

#random.seed(57)

class Client(object):
    def __init__(self, lambd, mu):
        self.lambd = lambd
        self.mu = mu
        self.entry_diff = expovariate(self.lambd)
        self.serve_time = expovariate(self.mu)


class Server(object):
    def __init__(self, capacity):
        self.capacity = capacity
        self.client_num = 0
        self.queue = []
        self._running_serve = 0
        self._running_diff = 0
        self.exp_dict = {0:0}
        self.waiting_time = []
        self.ST = 0
        self.info = {
            'serve_time': [],
            'diff_time': [],
            'sojourn_time': [],
            'non-served': 0,
            
        }

    def update_info(self, client):
        self.info['serve_time'].append(client.serve_time)
        self.info['diff_time'].append(client.entry_diff)

    def processing(self, client):
        flag_lost = 0

        self._running_diff += client.entry_diff

        if self.client_num == 0:  # for the first client
            self._running_serve = self._running_diff + client.serve_time

        if self.client_num < self.capacity:
            self.update_info(client)
            if self.client_num == 0:
                self.waiting_time.append(0)
            else:
                
                self.waiting_time.append(max(0.0, self.ST-client.entry_diff))
            self.ST = client.serve_time + self.waiting_time[-1]

            self.info['sojourn_time'].append(self.ST)

        self.queue.append(client)
        self.client_num+=1

        # self.update_info(client)

        while True:
            if self._running_diff >= self._running_serve:
                self.queue.pop(0)
                self.client_num -= 1

                self.exp_dict[self._running_serve] = self.client_num - 1

                if self.client_num == 1:
                    self._running_serve = self._running_diff

                self._running_serve += self.queue[0].serve_time
            else:
                if self.client_num > self.capacity:
                    self.queue.pop()
                    self.client_num -= 1
                    self.info['non-served'] +=1
                    flag_lost = 1
                break

        if flag_lost==0:
            self.exp_dict[self._running_diff] = self.client_num

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

def vis_num_of_clients_in_time(iterations, lambd, mu, capacity):
    server = Server(capacity=capacity)

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
    c2.serve_time = 2
    c3 = Client(1,1)
    c3.entry_diff = 1
    c3.serve_time = 1
    c4 = Client(1,1)
    c4.entry_diff = 3
    c4.serve_time = 2
    c5 = Client(1,1)
    c5.entry_diff = 1
    c5.serve_time = 2
    c6 = Client(1,1)
    c6.entry_diff = 8
    c6.serve_time = 2

    clients = [c1, c2, c3, c4, c5, c6]

    for cl in clients:
        server.processing(cl)

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()))
    plt.scatter(list(od.keys()), list(od.values()))
    plt.grid()
    plt.show()


def vis_waiting_time_of_each_client(iterations, lambd, mu, capacity):
    server = Server(capacity=capacity)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations):
        server.processing(Client(lambd, mu))

    plt.plot(range(len(server.waiting_time)), server.waiting_time)
    plt.scatter(range(len(server.waiting_time)), server.waiting_time)
    plt.grid()
    plt.show()

    print('Average time of waiting of all clients with lambda={}, mu={} & '
          'server capacity={} is {}'.format(lambd, mu, capacity, np.array(server.waiting_time).mean()))


def mean_sojourn_time(iterations, lambd, mu, capacity, verbose=False):
    server = Server(capacity=capacity)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations):
        server.processing(Client(lambd, mu))

    ret = np.array(server.info['sojourn_time']).mean()
    
    if verbose:
        print('Average sojourn time of all clients with lambda={}, mu={} & '
              'server capacity={} is {}'.format(lambd, mu, capacity, ret))    
    return ret

def prob_of_waiting(iterations, lambd, mu, capacity, verbose=False):
    server = Server(capacity=capacity)

    for i in range(1, iterations):
        server.processing(Client(lambd, mu))

    non_zero_wait_time = np.array(server.waiting_time).nonzero()[0].size
    total_wait_times = len(server.waiting_time)

    ret = non_zero_wait_time/total_wait_times

    if verbose:
        print('Average sojourn time of all clients with lambda={}, mu={} & '
              'server capacity={} is {}'.format(lambd, mu, capacity, ret))   
    return ret

if __name__ == '__main__':
    lambd = 80
    mu = 100
    capacity = 5
    iterations = 10000

    # vis_num_of_clients_in_time(iterations,lambd, mu)
    # vis_waiting_time_of_each_client(iterations, lambd, mu)
    # test()
    mean_sojourn_time(iterations, lambd, mu, capacity)