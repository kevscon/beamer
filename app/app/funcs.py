import os, math
import numpy as np
import pandas as pd

directory = os.getcwd() + '/app/app/'
factor_df = pd.read_csv(directory + 'max_factors.csv', index_col=0)

min_factor_dict = {
    'DC': 0.9,
    'DW': 0.65,
    'ES': 0.75,
    'EH': 0.9,
    'EV': 1
}

def max_mag(num_array):
    return num_array[np.argmax(np.abs(num_array))]


def get_load_factor(load_case, load_type, factor_type='max'):
    if factor_type == 'min' and load_case.startswith('str'):
        try:
            load_factor = min_factor_dict[load_type]
        except:
            load_factor = factor_df.loc[load_case, load_type]
    else:
        load_factor = factor_df.loc[load_case, load_type]
    return '{0:.2f}'.format(load_factor)


def get_load_location(load_distribution, struct_type, L):
    a = ''
    if load_distribution == 'point':
        if struct_type == 'cantilever':
            a = 0
        else:
            a = float(L)/2
    return a


def run_beamer(struct_type, load_distribution, load, L, a, E, I):

    # factor to convert defl to in
    unit_factor = 1/(12**2/12**4)*12
    output_dict = {}

    def analyze_simple_uniform(load, L, E, I):
        R_1 = -load * L / 2
        R_2 = -load * L / 2
        output_dict['reaction'] = [R_1, R_2]

        output_dict['shear'] = abs(max_mag([R_1, R_2]))

        M = load * L**2 / 8
        output_dict['moment'] = [M]

        deflection = 5*load*L**4 / (384*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_simple_point(load, L, a, E, I):
        b = L - a

        R_1 = -load * b / L
        R_2 = -load * a / L
        output_dict['reaction'] = [R_1, R_2]

        output_dict['shear'] = abs(max_mag([R_1, R_2]))

        M = load * a * b / L
        output_dict['moment'] = [M]

        if a < b:
            deflection = load*a*b*(b + 2*a)*math.sqrt(3*b*(b + 2*a)) / (27*E*I) * unit_factor
        else:
            deflection = load*a*b*(a + 2*b)*math.sqrt(3*a*(a + 2*b)) / (27*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_simple_triangular(load, L, E, I):
        R_1 = -load * L / 6
        R_2 = -load * L / 3
        output_dict['reaction'] = [R_1, R_2]

        output_dict['shear'] = abs(max_mag([R_1, R_2]))

        W = load * L / 2
        M = 0.1283 * W * L
        output_dict['moment'] = [M]

        deflection = 0.01304*W*L**3 / (E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_cantilever_uniform(load, L, E, I):
        R = -load * L
        output_dict['reaction'] = [R]

        output_dict['shear'] = abs(R)

        M = -load * L**2 / 2
        output_dict['moment'] = [M]

        deflection = load*L**4 / (8*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_cantilever_point(load, L, a, E, I):
        R = -load
        output_dict['reaction'] = [R]

        output_dict['shear'] = abs(R)

        if a == '':
            a = 0
        b = L - a
        M = -load * b
        output_dict['moment'] = [M]

        deflection = load*b**2*(3*L - b) / (6*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_cantilever_triangular(load, L, E, I):
        R = -load * L / 2
        output_dict['reaction'] = [R]

        output_dict['shear'] = abs(R)

        M = -load * L**2 / 6
        output_dict['moment'] = [M]

        deflection = load*L**4 / (30*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_fixed_uniform(load, L, E, I):
        R_1 = -load * L / 2
        R_2 = -load * L / 2
        output_dict['reaction'] = [R_1, R_2]

        output_dict['shear'] = abs(max_mag([R_1, R_2]))

        M_neg = -load * L**2 / 12
        M_pos = load * L**2 / 24
        output_dict['moment'] = [M_neg, M_pos]

        deflection = load*L**4 / (384*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_fixed_point(load, L, a, E, I):
        b = L - a

        R_1 = -load * b**2 / L**3 * (3*a + b)
        R_2 = -load * a**2 / L**3 * (3*b + a)
        output_dict['reaction'] = [R_1, R_2]

        output_dict['shear'] = abs(max_mag([R_1, R_2]))

        if a < b:
            M_neg = -load * a * b**2 / L**2
        else:
            M_neg = -load * a**2 * b / L**2
        M_pos = 2 * load * a**2 * b**2 / L**3
        output_dict['moment'] = [M_neg, M_pos]

        if a < b:
            deflection = 2*load*b**3*a**2 / (3*E*I*(3*b+a)**2) * unit_factor
        else:
            deflection = 2*load*a**3*b**2 / (3*E*I*(3*a+b)**2) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_fixed_triangular(load, L, E, I):
        R_1 = -3 * load * L / 20
        R_2 = -7 * load * L / 20
        output_dict['reaction'] = [R_1, R_2]

        output_dict['shear'] = abs(max_mag([R_1, R_2]))

        M_neg = -load * L**2 / 20
        M_pos = load * L**2 / 46.6
        output_dict['moment'] = [M_neg, M_pos]

        deflection = load*L**4 / (764*E*I) * unit_factor
        output_dict['deflection'] = deflection

    def analyze_model(structure_type, load_distribution):

        if structure_type == 'simple':
            if load_distribution == 'uniform':
                analyze_simple_uniform(load, L, E, I)
            elif load_distribution == 'point':
                analyze_simple_point(load, L, a, E, I)
            elif load_distribution == 'triangular':
                analyze_simple_triangular(load, L, E, I)
            else:
                raise ValueError('invalid load distribution')

        elif structure_type == 'cantilever':
            if load_distribution == 'uniform':
                analyze_cantilever_uniform(load, L, E, I)
            elif load_distribution == 'point':
                analyze_cantilever_point(load, L, a, E, I)
            elif load_distribution == 'triangular':
                analyze_cantilever_triangular(load, L, E, I)
            else:
                raise ValueError('invalid load distribution')

        elif structure_type == 'fixed':
            if load_distribution == 'uniform':
                analyze_fixed_uniform(load, L, E, I)
            elif load_distribution == 'point':
                analyze_fixed_point(load, L, a, E, I)
            elif load_distribution == 'triangular':
                analyze_fixed_triangular(load, L, E, I)
            else:
                raise ValueError('invalid load distribution')

        else:
            raise ValueError('invalid structure type')

    analyze_model(struct_type, load_distribution)

    return output_dict
