import functools
import json
from math import ceil

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, session, url_for,
    send_from_directory
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.datastructures import TypeConversionDict

from .models import (db, User, Mst_devices, Mst_group, Role,
                     User_device_history, UserScure
)
from .auth import login_required
from .function import vali_dict, validate


bp = Blueprint('views', __name__)




@bp.route("/", methods=["GET"])
# @login_required
def employee():
    page = request.args.get('page', 1, type=int)
    name = request.args.get('search','', type=str)
    group = request.args.get('group','', type=str)
    g.name = request.args.get('ordername', '⌄', type=str)
    g.role = request.args.get('orderrole', '⌄', type=str)
    g.date = request.args.get('orderdate', '⌃', type=str)
    pagination = 5
    group_list = ['BAP Đà Nẵng', 'BAP Huế', 'BAP Tp HCM',
        'BAP TOKYO', 'BAP OSAKA']
    list_columns = ['id','full_name', 'birthday', 'group_name', 'email',
        'onboard_date', 'role_name']
    if '%' in name:
        name = name.replace('%','/%')
    x = User.full_name
    y = Role.role_name
    z = User.onboard_date
    if g.name == '⌃':
        x = User.full_name.desc()
    if g.role == '⌃':
        y = Role.role_name.desc()
    if g.date == '⌃':
        z = User.onboard_date.desc()

    query = db.session.query(User.id,
        User.email, User.full_name, User.tel, User.birthday,
        User.onboard_date, Mst_group.group_name,
        Role.role_name
        ).join(Role).join(Mst_group
        ).filter(User.full_name.ilike(f'%{name}%', escape='/')
        ).filter(Mst_group.group_name.like(f'%{group}%')
        ).order_by(x, y, z).paginate(page, pagination, False)

    return render_template('views/list_employees.html',
        users=list_columns, rows=query, Group=(ceil(page/3)-1),
        group_list=group_list, maxgroup=(ceil(query.pages/3)>(ceil(page/3))),
        name=name, group=group
        )

@bp.route('/update/<int:id>', methods = ['GET', 'POST'])
# @login_required
def update(id):
    group = Mst_group.query.all()
    role = Role.query.all()
    email = request.form.get('email', '')
    role_id = request.form.get('role', '')
    group_id = request.form.get('group', '')
    full_name = request.form.get('full_name', '')
    fullname_kana = request.form.get('fullname_kana', '')
    birthday = request.form.get('birthday', '')
    persional_email = request.form.get('persional_email', '')
    tel = request.form.get('tel', '')
    pwd = request.form.get('password', '')
    pwd_encode = generate_password_hash(pwd)
    pwd_confirm = request.form.get('pass_confirm', '')
    query = db.session.query(User.id,
        User.email, User.full_name, User.gender, User.birthday,
        User.fullname_kana, User.persional_email,
        User.onboard_date, Mst_group.group_name, User.tel,
        Role.role_name, UserScure.password, Role.role_id
        ).join(Role).join(Mst_group).filter(User.id == id).first()
    error = dict()
    if request.method == 'POST':
        x = {'user_name':email,
                      'password':pwd_encode}
        y = {'group_id':group_id,
            'email':email, 'persional_email':persional_email,
            'full_name':full_name, 'fullname_kana':fullname_kana,
            'tel':tel, 'birthday':birthday,
            'role_id':role_id
        }
        vali = {'email':email, 'persional_email':persional_email,
            'full_name':full_name, 'fullname_kana':fullname_kana,
            'tel':tel, 'password':pwd
            }
        vali_dict['email']['query'] = db.session.query(User.email).all()
        session['update'] = 0
        for i in vali:
            if validate(vali[i], **vali_dict[i]):
                error[i] = validate(vali[i], **vali_dict[i])
                return render_template('views/edit.html', page_id=id,
                    user=query, groups=group, roles=role, error=error)

        if id !=0:
            y.pop('email')
            session['update'] = id
        else:
            if validate(pwd, compare=pwd_confirm ):
                error['pass_confirm'] = validate(pwd, compare=pwd_confirm)
                return render_template('views/edit.html',
                    page_id=id, user=query,
                    groups=group, roles=role, error=error)
        session['user_new'] = json.dumps(y)
        session['scure_new'] = json.dumps(x)
        return render_template('views/confirm.html',
            group=Mst_group.query.get(group_id).group_name,
            role=Role.query.get(role_id).role_name,
            email=User.query.get(id)
            )
    return render_template('views/edit.html', page_id=id, user=query,
        groups=group, roles=role, error=error)

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
    if request.method == 'POST':
        userscure = UserScure.query.filter(User.id==id).first()
        db.session.delete(user)
        db.session.commit()
        return render_template('views/announce.html',
        announce='ユーザの削除が完了しました。')
    return render_template('views/view_employee.html', user=query_user,
        devices=query_devices, page_id = id)


@bp.route('/confirm', methods = ['GET', 'POST'])
def confirm():
    x = session['scure_new']
    y = session['user_new']
    x_load = json.loads(x)
    y_load = json.loads(y)
    y_load['onboard_date'] = db.func.now()
    if session['update']:
        user = db.session.query(User).filter(
            User.id==session['update']).update(y_load)
        db.session.commit()
        return render_template('views/announce.html',
            announce='ユーザの更新が完了しました。')
    userscure = UserScure(**x_load)
    user = User(**y_load)
    userscure.child.append(user)
    db.session.add(userscure)
    db.session.add(user)
    db.session.commit()
    return render_template('views/announce.html',
        announce='ユーザの登録が完了しました。')
