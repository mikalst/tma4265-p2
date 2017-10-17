import matplotlib.pyplot as plt
import numpy as np



def task_a():
    l = [25 for i in range(33)]
    mu = [i for i in range(33)]
    
    pi = [-1 for i in range(33)]
    pi[0] = 1
    
    for i in range(1,33):
        pi[i] = pi[i-1]*l[i-1]/mu[i]
    
    L = sum(pi)
    pi = [el/L for el in pi]
    print(pi)
    
    plt.title("$\pi_n, \quad n = 0, 1 ..., 32$")
    plt.xlabel("$n$")
    plt.ylabel("$\pi_n$")
    plt.bar(range(33), pi)
    plt.savefig("p2_task_a.pdf")
    
def task_b(TIMESTEP=60):
    ITER = 100
    avg = [0 for k in range(7*24*TIMESTEP)]
    forw = 0
    long_term = [0 for k in range(33)]
    
    plt.figure()
    
    for _ in range(ITER):
        x = [0 for k in range(7*24*TIMESTEP)]
        for i in range(1,7*24*TIMESTEP):
            birth = np.random.rand() <= 25/TIMESTEP
            if (x[i-1] < 32):    
                pass
            else:
                forw += 1
                birth = 0
                
            death = np.random.rand() <= x[i-1]/TIMESTEP
            
            x[i] = x[i-1] + birth - death
        
        
        for d in x[24*60::TIMESTEP]:
            long_term[d]+=1
        
        plt.plot(range(len(x)//TIMESTEP), x[::TIMESTEP], lw=0.5)
        
        avg = [avg[i]+ el for i, el in enumerate(x)]
    
    L = sum(long_term)
    long_term = [el/L for el in long_term]
    
    print("Average forwarded pr. hour = {}".format(forw * 60 / (TIMESTEP * ITER * 7*24)))
    
    avg = [d/ITER for d in avg[::TIMESTEP]]
    
    plt.xlabel("$t$   [hours]")
    plt.ylabel("$N(t)$")
    plt.title("$N^{b}(t)$   for $b = 1, 2, ... 100$")

    
    average, = plt.plot(range(len(avg)), avg, lw=2.0, color="black", label=r"Average $ \bar{N}(t)$")
    
    plt.legend(handles=[average])
    plt.savefig("p2_task_b_simul_ts_"+str(TIMESTEP)+".pdf")
    
    return long_term
    
def task_b_cont():
    
    
    for f in [1, 4, 16]:
        color = {1:"blue",
                 4:"red",
                 16:"yellow"}[f]
        lt = task_b(f*60)
        plt.figure(9)
        plt.bar(range(33), lt, color=color)

    plt.title(r"Ratio $ r(n) = \frac{N(t)=n}{N_{tot}}$,   $t > 24$")
    plt.xlabel("$n$")
    plt.ylabel(r"$r(n)$")
    
    plt.legend([r"Timestep = $1h$",
                r"Timestep = $\frac{1}{4}h$",
                r"Timestep = $\frac{1}{16}h$"])
    
    plt.savefig("p2_task_b_r.pdf")
    
    plt.show()
    


if __name__ == "__main__":
    plt.style.use("ggplot")
    task_a()
    task_b_cont()