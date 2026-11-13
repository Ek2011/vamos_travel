import json
import os
import sqlite3

from flask import Flask
from flask_login import LoginManager, login_user, logout_user
from werkzeug.utils import secure_filename

from forms.user import RegisterForm, LoginForm
from data.users import User

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user
from data import db_session
from data.trips import Trip
from data.points import TripPoint
from forms.step_1_form import StepFirstForm
from flask import request

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
UPLOAD_FOLDER = "static/uploads/"


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    return user


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    port = int(os.environ.get("PORT", 5000))
    db_session.global_init("db/trevel.db")
    app.run(host='0.0.0.0', port=port)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Создаем оба экземпляра форм для главной страницы
    login_form = LoginForm()
    register_form = RegisterForm()

    message = ""
    show_modal = None

    # --- ОБРАБОТКА ВХОДА (LOGIN) ---
    if 'submit_login' in request.form:
        if login_form.validate_on_submit():
            db_sess = db_session.create_session()
            user = db_sess.query(User).filter(User.email == login_form.email.data).first()
            if user and user.check_password(login_form.password.data):
                login_user(user, remember=login_form.remember_me.data)
                return redirect('/')

            message = "Неправильный логин или пароль"
            show_modal = "loginModal"
        else:
            show_modal = "loginModal"

    # --- ОБРАБОТКА РЕГИСТРАЦИИ (REGISTER) ---
    elif 'submit_register' in request.form:
        if register_form.validate_on_submit():
            # Проверка совпадения паролей
            if register_form.password.data != register_form.password_again.data:
                message = "Пароли не совпадают"
                show_modal = "registerModal"
            else:
                db_sess = db_session.create_session()
                # Проверка уникальности Email
                if db_sess.query(User).filter(User.email == register_form.email.data).first():
                    message = "Такой пользователь уже есть"
                    show_modal = "registerModal"
                else:
                    # Создание пользователя
                    user = User(
                        name=register_form.name.data,
                        email=register_form.email.data,
                        about=register_form.about.data
                    )
                    # Обработка аватара
                    if register_form.file.data:
                        file = register_form.file.data
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        user.file = filename

                    user.set_password(register_form.password.data)
                    db_sess.add(user)
                    db_sess.commit()
                    login_user(user)
                    return redirect('/')
        else:
            show_modal = "registerModal"

    # Рендерим главную страницу и передаем туда обе формы и метки ошибок
    return render_template('index.html',
                           login_form=login_form,
                           register_form=register_form,
                           message=message,
                           Icon='static/icon',
                           show_modal=show_modal)


@app.route('/step_1', methods=['GET', 'POST'])
@login_required
def step_1():
    form = StepFirstForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        # 1. Создаем новую поездку для текущего пользователя
        new_trip = Trip(
            user_id=current_user.id,
            title=form.title.data
        )
        db_sess.add(new_trip)
        db_sess.flush()  # Получаем id новой поездки до финального сохранения

        # 2. Достаем список городов, который собрал JavaScript на сайте
        raw_points = form.points_data.data
        if raw_points:
            points_list = json.loads(raw_points)
            for index, item in enumerate(points_list):
                point = TripPoint(
                    trip_id=new_trip.id,
                    sequence_order=index + 1,
                    destination=item['destination'],
                    arrival_time=item['arrival_time']
                )
                db_sess.add(point)

        db_sess.commit()

        # 3. Проверяем, какая кнопка была нажата
        #if form.next_step.data:
        #    return redirect(url_for('index'))
        if form.exit_step.data:
            return redirect(url_for('index'))

    return render_template('step_1.html', form=form)



if __name__ == '__main__':
    main()
