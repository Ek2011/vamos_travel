import os
import uuid

from flask import Flask, render_template, redirect, request, abort, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import desc
from werkzeug.utils import secure_filename
from flask import flash, redirect

from forms.user import RegisterForm, LoginForm
from data.users import User
from data import db_session

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

if __name__ == '__main__':
    main()
