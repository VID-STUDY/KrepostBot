import os

import telebot
from application import telegram_bot
from application.admin import bp
from application.core.models import User
from config import Config
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from werkzeug.utils import secure_filename

from .forms import MailForm


def do_mailing(image, text, preview):
    file_id = None
    if preview:
        users = User.query.all()
    else:
        users = [583411442, 1294618325, 64925540]
    if image:
        for user in users:
            user_id = user if preview else user.id
            if file_id:
                try:
                    telegram_bot.send_photo(chat_id=user_id,
                                            photo=file_id,
                                            caption=text)
                except telebot.apihelper.ApiException:
                    continue
            else:
                try:
                    file = open(image, 'rb')
                    file_id = telegram_bot.send_photo(chat_id=user_id,
                                                        photo=file,
                                                        caption=text).photo[-1].file_id
                    file.close()
                except telebot.apihelper.ApiException:
                    continue
            sleep(1 / 10) # 10 message per second
    else:
        for user in users:
            user_id = user if preview else user.id
            try:
                telegram_bot.send_message(chat_id=user_id,
                                            text=text)
            except telebot.apihelper.ApiException:
                continue
            sleep(1 / 10) # 10 message per second

@bp.route('/mailing', methods=['GET', 'POST'])
@login_required
def mailing():
    mail_form = MailForm()
    if request.method == 'POST':
        file = request.files['image']
        filepath = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(Config.MAILING_DIRECTORY, filename))
            filepath = (Config.MAILING_DIRECTORY + filename)
        text = mail_form.mail.data
        preview = mail_form.preview.data
        thread = Thread(target = do_mailing, args = (filepath, text, preview))
        thread.start()
        flash('Рассылка запущена!', category='success')
        return redirect(url_for('admin.mailing'))

    return render_template('admin/mailing.html',
                           title='Рассылка',
                           area='mailing',
                           mail_form=mail_form)
