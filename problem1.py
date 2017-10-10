import numpy as np
import matplotlib.pyplot as plt

def simulate_poisson(intensity, days):
    events = []
    time = 0
    
    while (time <= days):
        time += np.random.exponential(1/intensity)
        if (time <= days):
            #print("Event at {}".format(time))
            events.append(time)
    
    states = np.zeros((days+1),)
    
    for t in events:
        states[int(np.ceil(t))]+=1
        
    for i, s in enumerate(states[1:]):
        states[i+1] += states[i]
    
    return states, events

def nonhomogeneous_poisson(ll, days):
    
    lmax=max([ll(x) for x in range(days)])
    thrash, events = simulate_poisson(lmax, days)

    # Apply thinning
    events = [k for k in filter(lambda t: ll(t)/lmax >= np.random.uniform(), events)]
    

    states = np.zeros((days+1),)

    for t in events:
        states[int(np.ceil(t))]+=1
                
    for i, s in enumerate(states[1:]):
        states[i+1] += states[i]
                
    return states, events

def weighted_events(times, mu, sigma):
        
    N = len(times)
    weights = np.random.normal(mu, sigma, N)
    weights = np.exp(weights)
    
    return sum(weights)

def discount_events(times, mu, sigma, alpha):
    
    N = len(times)
    weights = np.exp(np.random.normal(mu, sigma, N))
    discount_factors = [k for k in map(lambda t: -alpha*t, times)]
    
    return np.dot(np.exp(discount_factors), weights)

def average_over_simulate(days, ITERATIONS, intensity=None):
    
    print("N simulations = {}".format(ITERATIONS))
    
    average = np.zeros((days+1),)
    cost = 0
    discount = 0
    realizations = []
    
    for _ in range(ITERATIONS):
        if (isinstance(intensity, int)):
            chain, times = simulate_poisson(intensity, days)
        else:
            chain, times = nonhomogeneous_poisson(intensity, days)
        for i, d in enumerate(chain):
            average[i] += d
        cost += weighted_events(times, -2.0, 1.0) 
        discount += discount_events(times, -2.0, 1.0, 0.001)
        realizations.append(chain)
        
    average/=ITERATIONS
    cost/=ITERATIONS
    discount/=ITERATIONS
    
    return average, realizations, cost, discount
    
def task_a():
    plt.style.use("ggplot")
    r1, *t = average_over_simulate(59, 100, 3)
    plt.title("$N(t)$,   $\lambda = 3$")
    plt.xlabel("Days after January 1st 0:00.00")
    plt.ylabel("$N(t)$")
    plt.plot(range(60), r1)
    plt.savefig("task_a.pdf")
    plt.show()

def task_b():
    plt.style.use("ggplot")
    r1, *t = average_over_simulate(59, 100, lambda t: 2+np.cos(t*np.pi/182.5))
    plt.title("$N(t)$,   $\lambda(t) = 2+cos(t\pi/182.5)$")
    plt.xlabel("Days after January 1st 0:00.00")
    plt.ylabel("$N(t)$")
    plt.plot(range(60), r1)
    plt.savefig("task_b.pdf")
    plt.show()

def task_c():
    r1, r, c1, t = average_over_simulate(59, 100, 3)
    print("Average claim amount with fixed lambda: {}".format(c1))
    r2, r, c2, t = average_over_simulate(59, 100, lambda t: 2+np.cos(t*np.pi/182.5))
    print("Average claim amount with varying lambda: {}".format(c2))

def task_d():
    a, r, c, discount = average_over_simulate(365, 100, 3)
    print("Approximate discounted amount with fixed lambda {}".format(
            discount))
    a, r, c, discount = average_over_simulate(365, 100, lambda t: 2+np.cos(t*np.pi/182.5))
    print("Approximate discounted amount with varying lambda {}".format(
            discount))

if __name__ == "__main__":
    #task_a()
    #task_b()
    #task_c()
    task_d()