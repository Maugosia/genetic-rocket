import numpy as np

m_fuel = 1
m_rocket = 200
gravity = -0.9
friction_const = 0.06
rocket_thrust_const = 500


def calculate_objective(genotypes):
    objectives = []
    heights = calculate_heigth_for_population(genotypes)
    for thrust_configuration, heigth in zip(genotypes, heights):
        # heigth = calculate_heigth(thrust_configuration)  # calculated in vectorized form
        objective = 0
        # print("h", heigth)
        if heigth >= 750:
            # print("whaaat", np.sum(thrust_configuration), thrust_configuration)
            objective = 200 - np.sum(thrust_configuration)

        objectives.append(objective)

    return objectives


def calculate_heigth(thrust_configuration_input):
    thrust_configuration = thrust_configuration_input
    h = 0
    v = 0
    a = 0
    
    mass = calculate_mass(thrust_configuration, m_fuel, m_rocket)  # calculating this inside loop hurts performance
    
    for current_thrust in thrust_configuration:
        a_T = -friction_const * v * (abs(v) / mass)
        a_g = gravity
        a_r = current_thrust * rocket_thrust_const/mass
        a = a_T + a_g + a_r
        v = v + a
        h = h + v

        mass -= current_thrust * m_fuel  # fuel burns

    return h

def calculate_heigth_for_population(thrust_configurations):
    # even faster is to use numpy vectorization to process whole population (code practically the same)
    thrust_configurations = np.array(thrust_configurations)

    h = np.zeros(len(thrust_configurations))
    v = np.zeros(len(thrust_configurations))
    a = np.zeros(len(thrust_configurations))

    mass = np.sum(thrust_configurations, axis=1)*m_fuel + m_rocket

    for current_thrust in thrust_configurations.T:  # iterate over columns
        a_T = -friction_const * v * (abs(v) / mass)
        a_g = gravity
        a_r = current_thrust * rocket_thrust_const/mass
        a = a_T + a_g + a_r
        v = v + a
        h = h + v

        mass -= current_thrust * m_fuel  # fuel burns
                
    return h


def calculate_mass(thrust_configuration, mass_fuel, mass_rocket):
    mass = np.sum(thrust_configuration)*mass_fuel + mass_rocket
    return mass
