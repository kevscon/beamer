from flask import request
import os
import pandas as pd

def process_form():

    struct_type = request.form['struct_type']
    span_length = request.form['span_length']
    from app.app.ft_in import return_feet
    span_length_feet = return_feet(span_length)
    load_distribution = request.form['load_distribution']
    load = float(request.form['load'])
    a = request.form['load_location']
    if a == '':
        a_feet = a
    else:
        a = request.form['load_location']
        a_feet = return_feet(a)
    E = float(request.form['E'])
    I = float(request.form['I'])
    load_factor = float(request.form['load_factor'])

    factored_load = load_factor * load

    from app.app.funcs import run_beamer
    output = run_beamer(struct_type, load_distribution, factored_load, span_length_feet, a_feet, E, I)
    return output

def get_load_factor():
    max_factor_filepath = os.getcwd() + '/app/app/data/max_factors.csv'
    min_factor_filepath = os.getcwd() + '/app/app/data/min_factors.csv'

    max_factor_df = pd.read_csv(max_factor_filepath, index_col=0)
    min_factor_df = pd.read_csv(min_factor_filepath, index_col=0)

    factor_dict = {
        'max': max_factor_df.transpose().to_dict(),
        'min': min_factor_df.transpose().to_dict()
    }
    return factor_dict
