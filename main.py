import genetic_functions as genetic
import task_specific_functions as task


def main():
    # -----------------HIPERPARAMETERS----------------
    subject_size = 200
    mi = 50
    pm = 0.1
    pc = 0.01
    iter_max = 100

    objective_function = task.calculate_objective
    reproduction_function = genetic.reproduction_roulette
    mutation_function = genetic.mutation_binary
    crossover_function = genetic.crossover_singlepoint
    succesion_function = genetic.succesion_generational

    # ------------------CALCULATION-------------------
    genotype, gain = genetic.genetic_alghoritm(objective_function, reproduction_function, mutation_function, 
                                               crossover_function, succesion_function, 
                                               subject_size, mi, pm, pc, iter_max)
    print(genotype)
    print(gain)



if __name__ == "__main__":
    main()
