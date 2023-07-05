import numpy as np
import random


def genetic_alghoritm(objective_fun, reproduction_fun, mutation_fun, crossover_fun, succesion_fun, subject_size, population_size, p_mutation, p_crossingover, t_max):
    t = 0
    population = get_random_population(subject_size, population_size)
    evaluation = objective_fun(population)
    individual_best, evaluation_best = choose_best_element(population, evaluation)

    while t < t_max:
        population_reproduced = reproduction_fun(population, evaluation, population_size)
        population_crossedover = crossover_fun(population_reproduced, p_crossingover)
        population_mutated = mutation_fun(population_crossedover, p_mutation)

        evaluation = objective_fun(population_mutated)
        new_individual_best, new_evaluation_best = choose_best_element(population_mutated, evaluation)

        if new_evaluation_best >= evaluation_best:
            evaluation_best = new_evaluation_best
            individual_best = new_individual_best

        # print("CURRENT BEST", evaluation_best, "ITER", t+1, "/", t_max)
        population = succesion_fun(population, population_mutated)
        t = t + 1
    
    return individual_best, evaluation_best


def get_random_population(subject_size, population_size):
    random_population = np.zeros((population_size, subject_size))
    for i in range(0, population_size):
        subject =  np.random.choice([0, 1], size=subject_size, p=[.5, .5])
        random_population[i] = subject
    
    return random_population


def reproduction_roulette(population, evaluation_input, population_size):
    population_indices = range(0, population_size)
    population_reproduced = np.copy(population)
    evaluation = np.copy(evaluation_input)
    evaluation = np.multiply(evaluation, 2)
    
    for i in range(0, len(evaluation)):
        if evaluation[i] <= 0:
            evaluation[i] = 1

    for i in range(0, population_size):
        choosen_element = random.choices(population_indices, weights=evaluation, k=1)
        population_reproduced[i] = population[choosen_element]

    return population_reproduced


def crossover_singlepoint(population_input, probability_crossingover):
    population_crossedover = np.copy(population_input)
    looping_indices = range(0, int(np.floor(len(population_crossedover)/2)))

    for i in looping_indices:
        random_draw = random.random()
        if random_draw < probability_crossingover:
            genotype_1 = np.copy(population_input[2*i])
            genotype_2 = np.copy(population_input[(2*i)+1])

            indices = range(0, len(genotype_1))
            crossover_point = random.choice(indices)

            population_crossedover[2*i][crossover_point:] = genotype_2[crossover_point:]
            population_crossedover[(2*i)+1][:crossover_point] = genotype_1[:crossover_point]

    return population_crossedover


def succesion_generational(old_population, population_mutated):
    new_population = population_mutated
    return new_population


def mutation_binary(input_population, probability_mutation):
    output_population = np.copy(input_population)
    for i, element in enumerate(output_population):
        for j in range(0, len(element)):
            random_draw = random.random()
            if random_draw < probability_mutation:
                var = np.copy(output_population[i][j])
                if var == 0:
                    output_population[i][j] = 1
                if var == 1:
                    output_population[i][j] = 0

    return output_population


def choose_best_element(elements, evaluations):
    id_max = np.argmax(evaluations)
    best_element = elements[id_max]
    best_evaluation = evaluations[id_max]

    return best_element, best_evaluation