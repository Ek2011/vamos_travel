from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class StepFirstForm(FlaskForm):
    title = StringField('Название маршрута', validators=[DataRequired()])
    points_data = HiddenField('Список точек')
    next_step = SubmitField('Продолжить')
    exit_step = SubmitField('Выйти')
