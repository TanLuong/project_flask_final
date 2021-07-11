import functools
import json
from math import ceil

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for,
    send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import (db, User, Mst_devices, Mst_group, Role,
                     User_device_history, UserScure
)
from .auth import login_required


bp = Blueprint('views', __name__)




@bp.route("/", methods=["GET", "POST"])
# @login_required
def employee():
    page = request.args.get('page', 1, type=int)
    pagination = 5
    group_list = ['BAP Đà Nẵng', 'BAP Huế', 'BAP Tp HCM',
        'BAP TOKYO', 'BAP OSAKA']
    list_columns = ['id','full_name', 'birthday', 'group_name', 'email',
        'onboard_date', 'role_name']
    if request.method == "POST":
        name = request.form['search']
        group = request.form['group']
        g.name = request.form['ordername']
        g.role = request.form['orderrole']
        g.date = request.form['orderdate']
        x = User.full_name
        y = Role.role_name
        z = User.onboard_date
        if g.name == '⌃':
            x = User.full_name.desc()
        if g.role == '⌃':
            y = Role.role_name.desc()
        if g.date == '⌃':
            z = User.onboard_date.desc()
        if group == '全て':
            group = ''
        query = db.session.query(User.id,
            User.email, User.full_name, User.tel, User.birthday,
            User.onboard_date, Mst_group.group_name,
            Role.role_name
            ).join(Role).join(Mst_group
            ).filter(User.full_name.like(f'%{name}%')
            ).filter(Mst_group.group_name.like(f'%{group}%')
            ).order_by(x, y, z).paginate(page, pagination, False)
        return render_template('views/list_employees.html',
            users=list_columns, rows=query, group=(ceil(page/3)-1),
            name=name, se_group=group, group_list=group_list)
    g.name = "⌄"
    g.role = "⌄"
    g.date = "⌃"
    query = db.session.query(User.id,
        User.email, User.full_name, User.gender, User.birthday,
        User.onboard_date, Mst_group.group_name, User.tel,
        Role.role_name
        ).join(Role).join(Mst_group
        ).order_by(User.full_name, Role.role_name,
        User.onboard_date.desc()).paginate(page, pagination, False)

    return render_template('views/list_employees.html', users=list_columns,
        rows=query, group=(ceil(page/3)-1),
        group_list=group_list)


@bp.route('/update/<int:id>', methods = ['GET', 'POST'])
# @login_required
def update(id):
    group = ['BAP Đà Nẵng', 'BAP Huế', 'BAP Tp HCM', 'BAP TOKYO', 'BAP OSAKA']
    role = ['Super User', 'Admin', 'PMO', 'BMO', 'PM',
        'Leader', 'Developer', 'QC', 'QA', 'BrSE', 'Fresher', 'Intern'
    ]
    if request.method == "POST":
        if id == 0:
            email = request.form['email']
            role_name = request.form['role']
            group_name = request.form['group']
            full_name = request.form['full_name']
            fullname_kana = request.form['fullname_kana']
            birthday = request.form['birthday']
            persional_email = request.form['persional_email']
            tel = request.form['tel']
            pwd = request.form['password']
            pwd = generate_password_hash(pwd)
            pwd_confirm = request.form['pass_confirm']
            query_group = Mst_group.query.filter(
                Mst_group.group_name==group_name).first()
            query_role = Role.query.filter(
                Role.role_name==role_name).first()
            group_id = query_group.group_id
            role_id = query_role.role_id
            x = {'user_name':email,
                          'password':pwd}
            y = {'group_id':group_id,
                'email':email, 'persional_email':persional_email,
                'full_name':full_name, 'fullname_kana':fullname_kana,
                'tel':tel, 'birthday':birthday,
                'role_id':role_id
            }

            session['user_new'] = json.dumps(y)
            session['scure_new'] = json.dumps(x)

            return render_template('views/confirm.html', group=group_name,
                role=role_name, email=email, full_name=full_name,
                fullname_kana=fullname_kana, birthday=birthday,
                persional_email=persional_email, tel=tel)

    query = db.session.query(User.id,
        User.email, User.full_name, User.gender, User.birthday,
        User.fullname_kana, User.persional_email,
        User.onboard_date, Mst_group.group_name, User.tel,
        Role.role_name
        ).join(Role).join(Mst_group).filter(User.user_id == id).first()
    return render_template('views/edit.html', page_id=id, user=query,
        groups=group, roles=role)

@bp.route('/view/<int:id>', methods = ['GET', 'POST'])
def view_detail(id):
    query_user = db.session.query(
        User.email, Mst_group.group_name, User.full_name, User.fullname_kana,
        User.birthday, User.persional_email, User.tel,
        ).join(Mst_group).filter(User.id == id).first()
    query_devices = db.session.query(
        Mst_devices.device_name,
        User_device_history.start_date,
        User_device_history.end_date,
    ).join(Mst_devices).filter(User_device_history.id == id).all()
    return render_template('views/view_employee.html', user=query_user,
        devices=query_devices, page_id = id)


@bp.route('/confirm', methods = ['GET', 'POST'])
def confirm():
    x = session['scure_new']
    y = session['user_new']
    x_load = json.loads(x)
    y_load = json.loads(y)
    y_load['onboard_date'] = db.func.now()
    userscure = UserScure(**x_load)
    user = User(**y_load)
    userscure.child.append(user)
    db.session.add(userscure)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('views.employee'))
