from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired


class StepFirstForm(FlaskForm):
    title = StringField('Название маршрута', validators=[DataRequired()])
    next_step = SubmitField('Продолжить')
    exit_step = SubmitField('Выйти')
