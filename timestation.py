from manager import *
from threading import Thread, Lock, Event
from queue import Queue
from flask import Flask, render_template, session, request, \
    redirect, url_for, flash, jsonify
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_socketio import SocketIO

from auth import User, CustomLoginManager


flask_app = Flask(__name__)
socketio = SocketIO(flask_app, async_mode=None, cookie=None, logger=False, engineio_logger=False)
manager = Manager(logger=flask_app.logger)

user = User(1, u"name")
login_manager = CustomLoginManager()
login_manager.init(flask_app)


@login_manager.user_loader
def load_user(user_id) -> type(User):
    """
    Callback функция, возвращает объект класса текущего пользователя в сессии
    :param user_id: id текущего пользователя
    :return: объект класса текущего пользователя
    """
    return User


@flask_app.route("/login.html", methods=["GET", "POST"])
def login():
    return render_template("login.html", header=settings.header)


@flask_app.route("/logout", methods=["GET", "POST"])
# @authenticated_only
def logout():
    user.logout()
    # flash_message("Выход из системы!", 'warning')
    return redirect(url_for("login"))


@flask_app.route("/reauth", methods=["POST"])
def reauth():
    data = {}
    msg = request.form.get("msg")
    manager.logger.debug(msg)
    manager.logger.error('Смена пароля...')
    # if msg == 'not_equal_passwords':
    #     flash_message(u"Новые пароли не совпадают!", 'warning')
    # elif msg == 'null_password':
    #     flash_message(u"Не введен новый пароль!", 'warning')
    # elif msg:
    #     data['pass_verify'] = user.check_password(request.form["msg"])
    #     if not data['pass_verify']:
    #         flash_message(u"Неверный пароль!", 'warning')
    #     else:
    #         flash_message(u"Пароль изменен!")
    return jsonify(data)


@flask_app.route('/', methods=['GET', 'POST'])
@flask_app.route('/main.html', methods=['GET', 'POST'])
# @authenticated_only
def main() -> str:
    """
    Обрабатывает запрос к веб странице основных настроек
    :return: функция формирования шаблона веб страницы
    """
    print(request.form)
    # if request.method == 'POST':
    #
    #     action = request.form.get('btn')
    #     msg = None
    #
    #     if action == 'set_sync':
    #         msg = manager.set_sync_source(request.form.get('sync_src'))
    #     elif action == 'set_ext_sync':
    #         msg = manager.set_ext_sync_source(request.form.get('ext_sync_src'))
    #     elif action == 'save_time':
    #         msg = manager.save_time(request.form.get('date'), request.form.get('time'))
    #     elif action == 'save_time_settings':
    #         msg = manager.save_time_settings(request.form.get('timejump'),
    #                                          request.form.get('tz'),
    #                                          request.form.get('tz_kv'),
    #                                          request.form.get('tz_rs'), )
    #     elif action == 'save_gnss':
    #         msg = manager.save_gnss(request.form)
    #
    #     if msg:
    #         flash_message(u"%s" % msg)

    return render_template('main.html',
                           main=manager.get_main(),
                           header=settings.header)


if __name__ == '__main__':
    socketio.run(flask_app, debug=False, host='0.0.0.0', port='5001')
