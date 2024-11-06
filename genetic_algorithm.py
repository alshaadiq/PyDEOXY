import random
from scipy.stats import spearmanr

def calculate_fitness(response, expert_response):
    if len(response) != len(expert_response):
        raise ValueError("Response and expert response must have the same length.")
    correlation, _ = spearmanr(response, expert_response)
    return correlation  # Higher values are better

def selection(population, expert_response, num_selected):
    fitness_scores = [(response, calculate_fitness(response, expert_response)) for response in population]
    selected_population = sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:num_selected]
    return [individual[0] for individual in selected_population]

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 2)
    return parent1[:crossover_point] + parent2[crossover_point:]

def mutate(response, mutation_rate=0.1):
    for i in range(len(response)):
        if random.random() < mutation_rate:
            response[i] = random.randint(1, 10)  # Assuming scale is 1-10
    return response

def genetic_algorithm(population, expert_response, num_generations, mutation_rate=0.1, num_selected=5, crossover_rate=0.7, text_output=None, plot_widget=None, elite_size=1):
    pop_size = len(population)
    best_fitness_over_time = []

    for generation in range(num_generations):
        fitness_scores = [(response, calculate_fitness(response, expert_response)) for response in population]
        selected_population = selection(population, expert_response, num_selected)
        
        # Extract elite individuals
        elites = sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:elite_size]
        elite_individuals = [elite[0] for elite in elites]
        
        best_fitness = elites[0][1]
        best_fitness_over_time.append(best_fitness)
        
        if text_output:
            text_output.append(f"Generation {generation + 1}, Best Fitness (Spearman Correlation): {best_fitness:.4f}\n {selected_population}\n")
        
        if plot_widget:
            plot_widget.update_plot(best_fitness_over_time)
        
        new_population = elite_individuals.copy()  # Start with elite individuals
        while len(new_population) < pop_size:
            parent1, parent2 = random.sample(selected_population, 2)
            if random.random() < crossover_rate:
                offspring = crossover(parent1, parent2)
            else:
                offspring = parent1.copy()
                
            offspring = mutate(offspring, mutation_rate)
            new_population.append(offspring)
        
        population = new_population
    
    best_response = max(population, key=lambda x: calculate_fitness(x, expert_response))
    return best_response

