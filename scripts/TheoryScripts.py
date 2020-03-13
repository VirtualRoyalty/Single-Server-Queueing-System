import matplotlib.pyplot as plt

def get_probability(i, lambd, mu, capacity):
    """get probability of state i"""
    ro = lambd / mu
    if ro != 1:
        return ro ** i * (1 - ro) / (1 - (ro) ** (capacity + 1))
    else:
        return 1 / (capacity + 1)

def get_decline_probability(lambd, mu, capacity, **params):
    return get_probability(capacity, lambd, mu, capacity)

def get_waiting_probability(lambd, mu, capacity, **params):
    return 1 - get_probability(0, lambd, mu, capacity)


def get_expectation(lambd, mu, capacity, **params):
    """get math expectation of states"""
    expectation = 0
    for i in range(capacity + 1):
            expectation += i * get_probability(i, lambd, mu, capacity)
    return expectation

def get_manual_expectation(lambd, mu, capacity, **params):
    """get math expectation of states that calculated manually"""
    ro = lambd / mu
    if ro != 1:
        return (ro / (1 - ro) - (capacity + 1) * (ro ** (capacity + 1)) / (1 - ro ** (capacity + 1)))
    else:
        return capacity / 2

def get_average_time(lambd, mu, capacity, iterations):
    """get average time that customer spends in the system"""
    state_prob = get_probability(capacity, lambd, mu, capacity)
    expectation = get_expectation(lambd, mu, capacity)
    return (1 / (lambd * (1 - state_prob)) * expectation)

def draw_graph(func, size=(15, 10)):
    m = [10, 100, 3, 1000]
    N = [20, 5, 1000, 10]
    plt.figure(figsize=size)
    for i in range(len(m)):
        lamb = range(m[i] - (m[i] // 2 + 1), m[i] + m[i] // 2 + 2)
        pN = []
        for l in lamb:
            pN.append(globals().get('func'))

        plt.subplot(221 + i)
        plt.plot(lamb, pN, 'o-')
        plt.title('mu = {}, N = {}'.format(m[i], N[i]))
        plt.xlabel('lambda')
        plt.grid()
