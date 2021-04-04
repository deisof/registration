from data import db_session
from flask import Flask, render_template
from werkzeug.utils import redirect
from data.users import User
from data.jobs import Jobs
from forms.users import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/index')
def main():
    db_session.global_init("db/mars_explorer.db")
    session = db_session.create_session()
    sp = session.query(Jobs).all()
    action_list = []
    for elem in sp:
        leader = session.query(User).filter(User.id == elem.team_leader).first()
        if elem.is_finished:
            finished = 'Is finished'
        else:
            finished = 'Is not finished'
        action_list.append([elem.id, elem.job, leader.surname + ' ' + leader.name, elem.work_size,
                            elem.collaborators, finished])
    return render_template('index.html', actions=action_list)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    db_session.global_init("db/mars_explorer.db")
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.login.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.login.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
