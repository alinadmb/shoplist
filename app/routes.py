# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, ListCreationForm, ListEditionForm, ItemAdditionForm, DeleteListForm, DeleteItemForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, List, Item
from werkzeug.urls import url_parse


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = current_user
    lists = user.get_lists()
    items = []
    for list in lists:
        items += list.get_items()
    form = ListCreationForm()
    if form.validate_on_submit():
        list = List(listname=form.listname.data, author=current_user)
        db.session.add(list)
        db.session.commit()
        flash('Новый список создан')
        return redirect(url_for('index'))
    return render_template('index.html', user=user, lists=lists, items=items, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/list/<list_id>', methods=['GET', 'POST'])
@login_required
def show_list(list_id):
    list = List.query.filter_by(id=list_id).first_or_404()
    items = list.get_items()
    form1 = ItemAdditionForm()
    if form1.validate_on_submit():
        item = Item(itemname=form1.itemname.data, dir=list)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('show_list', list_id=list.id))
    form2 = DeleteItemForm
    if form2.validate_on_submit():
        list =
    return render_template('list.html', title='Список '+list.listname, list=list, items=items, form1=form1)


@app.route('/list/<list_id>/edit_list', methods=['GET', 'POST'])
@login_required
def edit_list(list_id):
    list = List.query.filter_by(id=list_id).first_or_404()
    form = ListEditionForm()
    if form.validate_on_submit():
        list.listname = form.listname.data
        db.session.commit()
        flash('Список изменен')
        return redirect(url_for('show_list', list_id=list.id))
    elif request.method == 'GET':
        form.listname.data = list.listname
    return render_template('edit_list.html', title='Изменить список', form=form)