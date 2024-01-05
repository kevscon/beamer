from app import app
from flask import render_template, request, jsonify


@app.route('/', methods=['GET', 'POST'])
def home():

    from app.app.forms import InputForm # import class from forms.py
    form = InputForm()

    if request.method == 'POST': # check if form data is submitted
        from app.app.route_funcs import process_form
        output = process_form()
        return jsonify({'output': output}) # sent to js script

    return render_template('home.html', form=form) # link to html script with form


@app.route('/<load_case>/<load_type>/<factor_type>/load-factor')
def load_factor_default(load_case, load_type, factor_type):
    from app.app.route_funcs import get_load_factor
    load_factor = get_load_factor(load_case, load_type, factor_type)
    return jsonify(load_factor)


@app.route('/<load_distribution>/<struct_type>/<span_length>/load-location')
def load_location_default(load_distribution, struct_type, span_length):
    from app.app.funcs import get_load_location
    load_location = get_load_location(load_distribution, struct_type, span_length)
    return jsonify(load_location)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
