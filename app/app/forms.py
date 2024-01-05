from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SelectField, RadioField, SubmitField

class InputForm(FlaskForm):

    struct_type = SelectField(
        'Select Structure Type:',
        choices = [('simple', 'Simply Supported'), ('cantilever', 'Cantilever'), ('fixed', 'Fixed-Fixed')]
        )

    span_length = StringField(
        'Enter Span Length:',
        default=10
        )

    load_distribution = SelectField(
        'Select Load Distribution:',
        choices = [('uniform', 'Uniform'), ('point', 'Point'), ('triangular', 'Triangular')]
        )

    load = StringField(
        'Enter Load:',
        default=1
        )

    load_location = StringField(
        'Enter "a" dimension:'
        )

    E = StringField(
        'Enter Modulus of Elasticity:',
        default=29000
        )

    I = StringField(
        'Enter Moment of Inertia:',
        default=700
        )

    load_case = SelectField(
        'Select AASHTO Load Case:',
        choices = [
            ('ser_I', 'Service I'),
            ('str_I', 'Strength I'),
            ('str_IV', 'Strength IV'),
            ('str_V', 'Strength V'),
            ('ee_II', 'Extreme Event II')
            ]
        )

    load_type = SelectField(
        'Select AASHTO Load Type:',
        choices = [
            ('DC', 'DC'),
            ('DW', 'DW'),
            ('EH', 'EH'),
            ('EV', 'EV'),
            ('ES', 'ES'),
            ('LL', 'LL'),
            ('WS', 'WS'),
            ('WL', 'WL'),
            ('CT', 'CT')
            ]
        )

    factor_type = RadioField(
        choices=[('max', 'Max'), ('min', 'Min')],
        default='max'
        )

    load_factor = StringField(
        'Load Factor:',
        default='1.00'
        )

    submit = SubmitField()
