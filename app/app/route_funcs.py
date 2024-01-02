from flask import request

def process_form():

    struct_type = request.form['struct_type']
    span_length = float(request.form['span_length'])
    load_distribution = request.form['load_distribution']
    load = float(request.form['load'])
    a = request.form['load_location']
    if a == '':
        pass
    else:
        a = float(request.form['load_location'])
    E = float(request.form['E'])
    I = float(request.form['I'])
    load_factor = float(request.form['load_factor'])

    factored_load = load_factor * load

    from app.app.funcs import run_beamer
    output = run_beamer(struct_type, load_distribution, factored_load, span_length, a, E, I)
    return output
