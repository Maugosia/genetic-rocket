import numpy as np

m_fuel = 1
m_rocket = 200
gravity = -0.9
friction_const = 0.06
rocket_thrust_const = 500


def calculate_objective(genotypes):
    objectives = []
    for thrust_configuration in genotypes:
        heigth = calculate_heigth(thrust_configuration)
        objective = 0
        # print("h", heigth)
        if heigth >= 750:
            # print("whaaat", np.sum(thrust_configuration), thrust_configuration)
            objective = 200 - np.sum(thrust_configuration)

        objectives.append(objective)

    return objectives


def calculate_heigth(thrust_configuration_input):
    thrust_configuration = np.copy(thrust_configuration_input)
    h = 0
    v = 0
    a = 0
    for i in range(0, len(thrust_configuration)):
        mass = calculate_mass(thrust_configuration, m_fuel, m_rocket)

        if thrust_configuration[i] == 1:
            a_T = -friction_const * v * (abs(v) / mass)
            a_g = gravity
            a_r = rocket_thrust_const/mass
            a = a_T + a_g + a_r
            v = v + a
            h = h + v

        if thrust_configuration[i] == 0:
            a_T = -friction_const * v * abs(v) / mass
            a_g = gravity
            a_r = 0
            a = a_T + a_g + a_r
            v = v + a
            h = h + v
            
        thrust_configuration[i] = 0  # fuel burns

    return h


def calculate_mass(thrust_configuration, mass_fuel, mass_rocket):
    mass = np.sum(thrust_configuration)*mass_fuel + mass_rocket
    return mass
