from app import app
from flask import render_template, request, jsonify


@app.route('/', methods=['GET', 'POST'])
def home():

    from app.app.forms import InputForm # import class from forms.py
    form = InputForm()

    if request.method == 'POST': # check if form data is submitted
        form_data = request.form
        from app.app.route_funcs import process_form
        output = process_form()
        return jsonify({'output': output}) # sent to js script

    return render_template('home.html', form=form) # link to html script with form


@app.route('/load-factors')
def load_factors():
    from app.app.route_funcs import get_load_factor
    load_factor_dict = get_load_factor()
    return jsonify(load_factor_dict)


@app.route('/point-location', methods=['POST'])
def point_location():
    data = request.get_json()
    from app.app.ft_in import return_feet
    span_length_feet = return_feet(data['span_length'])
    load_distribution = data['load_distribution']
    struct_type = data['struct_type']
    from app.app.funcs import get_load_location
    load_location = get_load_location(load_distribution, struct_type, span_length_feet)
    return jsonify(load_location)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
