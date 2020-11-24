'''
Batuhan Çakır 150501136 
UE5 2. Frage 
walking salesman
'''
import random
import math
import matplotlib.pyplot as plt


def initiate(population_size=200, length=10, max_city_pos=100, seed=None):#or here
    if seed is not None:
        random.seed(seed)
    
    cities_x = [random.randint(1,max_city_pos) for x in range(length)]
    cities_y = [random.randint(1,max_city_pos) for x in range(length)]

    route_list = []
    unrandomized_route = list(range(length))
    for i in range(population_size):
        route_list.append(random.sample(unrandomized_route,length))

    return (route_list, cities_x, cities_y)

def euclidian_distance(x,y):
    return math.sqrt(((x[0]-x[1])**2)+((y[0]-y[1])**2))

def calculate_fitness(cities_x, cities_y, population):
    fitnesses = []
    for route in population:
        distance_traveled = euclidian_distance((cities_x[0], cities_x[-1]), (cities_y[0],cities_y[-1])) 
        for i, current_city in enumerate(route):
            if i<len(route)-1:
                x = (cities_x[current_city], cities_x[route[i+1]])
                y = (cities_y[current_city], cities_y[route[i+1]])
                distance_traveled += euclidian_distance(x,y)

        fitnesses.append(distance_traveled)

    return fitnesses
                
def tourney_selection(population, fitness):
    unselected = list(zip(population,fitness))
    start_length = len(unselected)
    selected = []
    while(len(unselected) > start_length//2):
        sample = random.sample(unselected,start_length//4)
        sample.sort(key=lambda x: x[1])
        selected.append(sample[0])
        unselected.remove(sample[0])

    return [x[0] for x in selected] 


def crossover(matched):
    selection_points = [random.randint(0,len(matched[0])),random.randint(0,len(matched[0]))]
    selection_points.sort()
    cutted = matched[0][selection_points[0]:selection_points[1]]
    child = matched[0].copy()
    child[selection_points[0]:selection_points[1]] = [x for x in matched[1] if x in cutted]

    return child

def breeding(selected):
    start_selected = selected.copy()
    selected = selected.copy()
    children = []
    while len(selected)>2:
        matched = random.sample(selected,2)
        children.append(crossover(matched))
        children.append(crossover(matched))
        selected.remove(matched[0])
        selected.remove(matched[1])

    return start_selected + children

def mutate(population, mutation_rate=0.001):
    for route in population:
        for i, city in enumerate(route):
            if random.random()<mutation_rate:
                random_index = random.randint(0,len(route)-1)
                temp = route[i]
                route[i] = route[random_index]
                route[random_index] = temp
    return population

def create_graph():
    fig = plt.figure(3)
    fig.canvas.draw()
    plt.ion()
    ax1 = fig.add_subplot(121)
    ax1.set_title("Fitness")
    ax2 = fig.add_subplot(122)

    return(fig, ax1, ax2)

def show_graph(fig, ax1, ax2, average, minimum, cities_x, cities_y, route):
    
    ax1.plot(average, "r-")
    ax1.plot(minimum, "y-") 
    ax1.legend(["Average Fitness","Minimum Fitness"])

    ax2.clear()
    for i, current in enumerate(route):
        if i < len(route)-1:
            ax2.plot([cities_x[current],cities_x[route[i+1]]], [cities_y[current],cities_y[route[i+1]]],"ro-")
    ax2.set_title("Cities and Path")
    
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.pause(0.001)


def ga(steps=100, animate=True):

    population, cities_x, cities_y = initiate()#you can change initial parameters here
    fitnesses = calculate_fitness(cities_x,cities_y, population)
    print("Initialized")

    fig, ax1, ax2 = create_graph()

    i=0
    min_fitnesses = []
    avg_fitnesses = []
    while(i<steps):

        selected = tourney_selection(population,fitnesses)
        crossed = breeding(selected)
        population = mutate(crossed,0.01)
        fitnesses = calculate_fitness(cities_x,cities_y, population)

        min_fitnesses.append(min(fitnesses))
        avg_fitnesses.append(sum(fitnesses) / len(fitnesses))
        i+=1
        if animate:
            show_graph(fig, ax1, ax2, avg_fitnesses, min_fitnesses, cities_x, cities_y, population[fitnesses.index(min(fitnesses))])

    print(f"Minimum Fitness after {steps} steps:", min(fitnesses))

    plt.ioff()
    if not animate:
        show_graph(fig, ax1, ax2, avg_fitnesses, min_fitnesses, cities_x, cities_y, population[fitnesses.index(min(fitnesses))])
    plt.show()

ga(animate=True)#you can add parameters here to change graph behaviour 
