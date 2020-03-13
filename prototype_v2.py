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

def get_mean(iterations, lambd, mu, capacity):
    server = Server(capacity=capacity)

    for i in range(1, iterations+1):
        server.processing(Client(lambd, mu))

    return mean_state(states_prob(capacity, server.exp_dict))

def get_probs(iterations, lambd, mu, capacity):
    server = Server(capacity=capacity)

    for i in range(1, iterations+1):
        server.processing(Client(lambd, mu))

    return states_prob(capacity, server.exp_dict)

def vis_num_of_clients_in_time(iterations, lambd, mu,
                               capacity, title='Состояния системы'):
    server = Server(capacity=capacity)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations+1):
        server.processing(Client(lambd, mu))

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    plt.plot(list(od.keys()), list(od.values()), '*-')
    plt.grid()
    plt.title(title + ' при lambda = ' + str(lambd) + ', mu = ' \
                                   + str(mu) + ', capacity = ' + str(capacity))
    plt.show()

    print('Lost = {}'.format(server.info['non-served']))
    print('Mean time inside = {}'.format(np.array(server.info['time_inside']).mean()))
    print('Mean waiting time  = {}'.format(np.array(server.waiting_time).mean()))
    print('Mean lost = {}'.format(server.info['non-served']/iterations))
    probs = states_prob(capacity, server.exp_dict)
    # print(probs)
    print(mean_state(probs))
    print('Mean state = {}'.format(mean_state(states_prob(capacity, server.exp_dict))))

def vis_mean_of_clients_in_time(iterations, lambd, mu,
                                capacity=100, title='Среднее количество заявок в системе к моменту t'):
    server = Server(capacity=capacity)

    result = np.zeros(iterations)
    result[0] = server.client_num

    for i in range(1, iterations):
        server.processing(Client(lambd, mu))

    od = collections.OrderedDict(sorted(server.exp_dict.items()))
    ox = np.array(list(od.keys()))
    oy = list(od.values())
    oy = [sum(oy[:i+1]) for i, x in enumerate(oy)]
    oy = np.array(oy) / ox
    ox[0] = 0
    oy[0] = 0
    plt.plot(ox, oy)
    plt.title(title + ' при lambda = ' + str(lambd) + ', mu = ' \
                                   + str(mu) + ', capacity = ' + str(capacity))
    plt.grid()
    plt.show()
    return ox, oy


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
    ret = np.array(server.info['time_inside']).mean()

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

def prob_of_non_serving(iterations, lambd, mu, capacity, verbose=False):

    server = Server(capacity=capacity)
    for i in range(1, iterations):
        server.processing(Client(lambd, mu))

    non_served = server.info['non-served'] / iterations
    return non_served

def draw(message, func_from_class, loops=10, iterations=1000, \
         mu=[10, 100, 3, 300], N=[20, 5, 1000, 10], ytitle=''):
    plt.figure(figsize=(15, 10))
    plt.suptitle(message)
    for i in range(len(mu)):
        lambd = range(mu[i] - (mu[i] // 2 + 1), mu[i] + mu[i] // 2 + 2)
        expect = []
        for l in lambd:
            expect_mean = []
            for loop in range(loops):
                expect_mean.append(func_from_class(iterations=iterations,lambd=l, mu=mu[i],capacity=N[i]))
            expect.append(np.mean(expect_mean))
        plt.subplot(221 + i)
        plt.plot(lambd, expect, 'o-')
        plt.title('mu = {}, Capacity = {}'.format(mu[i], N[i]))
        plt.xlabel('lambda')
        plt.ylabel(ytitle)
        plt.grid()
    plt.show()

if __name__ == '__main__':
    lambd = 80
    mu = 100
    capacity = 5
    iterations = 10000

    # vis_num_of_clients_in_time(iterations,lambd, mu)
    # vis_waiting_time_of_each_client(iterations, lambd, mu)
    # test()
    mean_sojourn_time(iterations, lambd, mu, capacity)
