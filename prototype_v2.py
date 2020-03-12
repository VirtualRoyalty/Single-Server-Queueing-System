import numpy as np
import random
from random import expovariate
import matplotlib.pyplot as plt
import collections

random.seed(40)


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
        self.lost = 0
        self.ST = 0
        self.info = {
            'time_inside': [],
            'non-served': 0,
        }


    def processing(self, client):

        flag_lost = 0

        self._running_diff += client.entry_diff

        if self.client_num == 0:  # for the first client
            self._running_serve = self._running_diff + client.serve_time

        self.waiting_time.append(max(0.0, self.ST - client.entry_diff))

        self.ST = client.serve_time + self.waiting_time[-1]

        self.info['time_inside'].append(self.ST)


        self.queue.append(client)
        self.client_num += 1

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
                    self.info['non-served'] += 1
                    flag_lost = 1
                    self.ST = self.waiting_time[-1]
                    self.waiting_time.pop()
                    self.info['time_inside'].pop()

                break

        if flag_lost == 0:
            self.exp_dict[self._running_diff] = self.client_num


def states_prob(capacity, dict):
    states_count = np.zeros(capacity + 1)
    for state in dict.values():
        states_count[state] += 1

    for i in range (len(states_count)):
        states_count[i] = states_count[i] / len(dict)

    return states_count


def mean_state(states_prob):
    sum_mean = 0
    for i in range(states_prob.shape[0]):
        sum_mean += i * states_prob[i]

    return sum_mean


def vis_num_of_clients_in_time(iterations, lambd, mu):
    server = Server(capacity=capacity)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations+1):
        server.processing(Client(lambd, mu))

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()), '*-')
    plt.grid()
    plt.show()

    print('Lost = {}'.format(server.info['non-served']))
    print('Mean time inside = {}'.format(np.array(server.info['time_inside']).mean()))
    print('Mean waiting time  = {}'.format(np.array(server.waiting_time).mean()))
    print('Mean lost = {}'.format(server.info['non-served']/iterations))
    probs = states_prob(capacity, server.exp_dict)
    print(probs)
    print(mean_state(probs))
    print('Mean state = {}'.format(mean_state(states_prob(capacity, server.exp_dict))))



def test():
    server = Server(capacity=capacity)

    c1 = Client(1,1)
    c1.entry_diff = 1
    c1.serve_time = 5
    c2 = Client(1,1)
    c2.entry_diff = 1
    c2.serve_time = 3
    c3 = Client(1,1)
    c3.entry_diff = 1
    c3.serve_time = 1
    c4 = Client(1,1)
    c4.entry_diff = 1
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


if __name__ == '__main__':
    lambd = 10
    mu = 1
    capacity = 10
    iterations = 10000

    vis_num_of_clients_in_time(iterations,lambd, mu)
    #
    # test()