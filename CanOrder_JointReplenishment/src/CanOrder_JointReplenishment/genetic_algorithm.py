import random
import sys
import time
from src.CanOrder_JointReplenishment.simulation import simulate_policy
from src.CanOrder_JointReplenishment.graph import static_plot, live_plot
import matplotlib.pyplot as plt
import concurrent.futures

def initialize_population(pop_size, num_items, setup):
    """
    Initialize a population of (s, c, S) policy combinations for all items.
    
    Parameters:
        pop_size (int): Size of the population.
        num_items (int): Number of items.
        setup (dict): Dictionary containing setup parameters.
    
    Returns:
        list: A list of policy combinations for the population.
    """
    population = []

    max_s = setup['max_s']
    max_c = setup['max_c']
    max_S = setup['max_S']

    # Generate random population of (s, c, S) policy combinations for all items
    for _ in range(pop_size):
        policies = []
        for _ in range(num_items):
            s = random.randint(1, max_s)
            c = random.randint(s + 1, max_c) # Ensure 'c' is larger than 's'
            S = random.randint(c + 1, max_S) # Ensure 'S' is larger than 'c'
            policies.append([s, c, S])
        population.append(policies)
    
    return population

def sort_by_cost(fitness_tuple):
    return fitness_tuple[1]

def evaluate_fitness(population, demand_distribution, setup):
    """
    Evaluate the fitness of each policy combination in the population.
    
    Parameters:
        population (list): List of policy combinations.
        demand_distribution (numpy.ndarray): Empirical demand distribution for items.
        setup (dict): Dictionary containing setup parameters.
    
    Returns:
        list: A list of tuples containing policy combinations and their corresponding costs and service levels.
    """
    fitness_scores = []

    # Use ProcessPoolExecutor to parallelize the fitness evaluations
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit each policy evaluation as a task to the executor
        futures = [executor.submit(simulate_policy, demand_distribution, policies, setup) for policies in population]
        
        # Collect results as they finish
        for future in concurrent.futures.as_completed(futures):
            cost, service_level, container_fill_rate, periodicity = future.result()
            # Add the policy, cost, and service level to the fitness_scores list
            fitness_scores.append((population[futures.index(future)], cost, service_level, container_fill_rate, periodicity))

    # Sort by the cost (using the external function instead of lambda)
    fitness_scores.sort(key=sort_by_cost)

    return fitness_scores

''' 

# Useful for debugging (when needing to step into e.g. simulation.py)

def evaluate_fitness(population, demand_distribution, setup):
    """
    Evaluate the fitness of each policy combination in the population.
    
    Parameters:
        population (list): List of policy combinations.
        demand_distribution (numpy.ndarray): Empirical demand distribution for items.
        setup (dict): Dictionary containing setup parameters.
    
    Returns:
        list: A list of tuples containing policy combinations and their corresponding costs and service levels.
    """
    fitness_scores = []

    # Loop through each policy in the population and evaluate its fitness
    for policies in population:
        # Simulate the policy and get the cost and service level
        cost, service_level, container_fill_rate, peroidicity = simulate_policy(demand_distribution, policies, setup)
        # Add the policy, cost, and service level to the fitness_scores list
        fitness_scores.append((policies, cost, service_level, container_fill_rate, peroidicity))

    # Sort by the cost (using the external function instead of lambda)
    fitness_scores.sort(key=sort_by_cost)

    return fitness_scores
    '''

def select_parents(fitness_scores, num_parents):
    """
    Select the top-performing policy combinations as parents for the next generation.
    
    Parameters:
        fitness_scores (list): List of tuples containing policy combinations and their corresponding costs.
        num_parents (int): Number of parents to select.
    
    Returns:
        list: A list of the top-performing policy combinations.
    """
    fitness_scores.sort(key=lambda x: x[1])
    return fitness_scores[:num_parents]

import random

def crossover(parents, num_offspring):
    """
    Perform crossover between parent policy combinations to generate offspring.
    
    Parameters:
        parents (list): List of top-performing policy combinations.
        num_offspring (int): Number of offspring to generate.
    
    Returns:
        list: A list of new policy combinations generated from the parents.
    """
    offspring = []

    # Combine (r, s, S) policies to generate a new policy
    for _ in range(num_offspring):
        parent1 = random.choice(parents)[0]  # Select a role-model parent
        parent2 = random.choice(parents)[0]

        # Create a new child by combining policies from both parents
        child = []
        
        for p1_item, p2_item in zip(parent1, parent2):
            s = random.choice([p1_item[0], p2_item[0]]) # Select from either parent
            c = random.choice([p1_item[1], p2_item[1]])
            S = random.choice([p1_item[2], p2_item[2]])

            # If s >= c, adjust to make a feasible policy
            if s >= c:
                max_s = max(p1_item[0], p2_item[0])
                max_c = max(p1_item[1], p2_item[1])
                c = int(random.uniform(max_s, max_c))

            # If c >= S, adjust to make a feasible policy
            if c >= S:
                max_c = max(p1_item[1], p2_item[1])
                max_S = max(p1_item[2], p2_item[2])
                S = int(random.uniform(max_c, max_S))

            child.append([s, c, S])  # Add the new valid policy to the child

        offspring.append(child)

    return offspring

def mutate(offspring, mutation_rate, setup):
    """
    Apply mutation to the offspring to introduce variability in the policies.
    
    Parameters:
        offspring (list): List of policy combinations generated from crossover.
        mutation_rate (float): Probability of mutation for each policy.
        setup (dict): Dictionary containing setup parameters.
    
    Returns:
        list: A list of mutated policy combinations.
    """

    max_s = setup['max_s']
    max_c = setup['max_c']
    max_S = setup['max_S']

    # Randomly modify some policies to introduce variability
    for policies in offspring:
        if random.random() < mutation_rate:
            item_index = random.randint(0, len(policies) - 1)

            s = random.randint(1, max_s)
            c = random.randint(s + 1, max_c)
            S = random.randint(c + 1, max_S)  # Ensure 's' is smaller than 'S'
            policies[item_index] = [s, c, S]
    
    return offspring

def genetic_algorithm(demand_distribution, setup):
    """
    Run a genetic algorithm to optimize inventory policies based on demand distribution.
    
    Parameters:
        demand_distribution (numpy.ndarray): Empirical demand distribution for items.
        setup (dict): Dictionary containing setup parameters.
    
    Returns:
        list: A list of the best policy combinations after running the genetic algorithm.
    """
    pop_size = setup['pop_size']
    num_generations = setup['num_generations']
    mutation_rate = setup['mutation_rate']
    decay_rate = setup['decay_rate']
    parent_fraction = setup['parent_fraction']

    population = initialize_population(pop_size, setup['num_items'], setup)
    cost_progression = []  # List to track cost at each generation
    service_level_progression = []  # List to track service level at each generation

    # Create the initial plot
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    live_plot(cost_progression, service_level_progression, num_generations, ax)  # Modified live plot function

    for generation in range(num_generations):
        # Exponentially shrink the population size
        current_pop_size = max(100, int(pop_size * (decay_rate ** generation)))  # Shrinks by decay_rate each generation, minimum 100
        
        # Adjust the number of parents based on current population size
        num_parents = int(current_pop_size * parent_fraction)
        
        # Start measuring time for the generation evaluation
        start_time = time.time()

        # Calculate fitness, select parents, perform crossover and mutation
        fitness_scores = evaluate_fitness(population, demand_distribution, setup)
        parents = select_parents(fitness_scores, num_parents)
        offspring = crossover(parents, current_pop_size - num_parents)
        offspring = mutate(offspring, mutation_rate, setup)
        population = [p[0] for p in parents] + offspring

        # Get the cost and service level of the best policy in this generation
        best_policy = parents[0]
        best_cost = best_policy[1]
        best_service_level = best_policy[2]
        cost_progression.append(best_cost)
        service_level_progression.append(best_service_level)

        # End measuring time for the generation evaluation
        end_time = time.time()
        generation_time = end_time - start_time

        # Update the live plot with both cost and service level
        live_plot(cost_progression, service_level_progression, num_generations, ax)

        # Progress bar
        progress = (generation + 1) / num_generations * 100
        sys.stdout.write(f'\rGeneration {generation + 1}/{num_generations} - Progress: {progress:.2f}% - Last generation evaluation time: {generation_time:.2f} seconds     ')
        sys.stdout.flush()

    print()  # Move to the next line after the progress bar is done

    plt.ioff()  # Turn off interactive mode

    # Save the final plot
    fig.savefig('GeneticAlgorithm_Convergence', dpi=300)

    # Return the best policies
    best_policies = select_parents(fitness_scores, num_parents)

    return best_policies