from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user  # 添加 current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models import User

auth_bp = Blueprint('auth', __name__)

# ========== 自定义装饰器：API 接口的登录检查 ==========
def api_login_required(f):
    """API 接口专用的登录检查，返回 JSON 而不是重定向"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'code': 401, 'message': '未登录，请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ========== 页面接口 ==========

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('shop.index'))
        flash('邮箱或密码错误')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('邮箱已注册')
        else:
            hashed = generate_password_hash(password)
            user = User(email=email, password=hashed)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('shop.index'))
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


# ========== API 接口 ==========

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """登录接口（返回 JSON）"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求体不能为空'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'code': 400, 'message': '邮箱和密码不能为空'}), 400

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'user_id': user.id,
            'email': user.email
        })
    else:
        return jsonify({
            'code': 401,
            'message': '邮箱或密码错误'
        }), 401


@auth_bp.route('/api/register', methods=['POST'])
def api_register():
    """注册接口（返回 JSON）"""
    data = request.get_json()

    if not data:
        return jsonify({'code': 400, 'message': '请求体不能为空'}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'code': 400, 'message': '邮箱和密码不能为空'}), 400

    # 检查邮箱是否已注册
    if User.query.filter_by(email=email).first():
        return jsonify({'code': 409, 'message': '邮箱已注册'}), 409

    # 创建新用户
    hashed_password = generate_password_hash(password)
    user = User(email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    # 注册后自动登录
    login_user(user)

    return jsonify({
        'code': 200,
        'message': '注册成功',
        'user_id': user.id,
        'email': user.email
    }), 200


@auth_bp.route('/api/logout', methods=['POST'])
def api_logout():
    """退出登录接口（返回 JSON）"""
    # 检查是否已登录
    if not current_user.is_authenticated:
        return jsonify({'code': 401, 'message': '未登录，无需退出'}), 401

    logout_user()
    return jsonify({
        'code': 200,
        'message': '退出成功'
    }), 200


@auth_bp.route('/api/user', methods=['GET'])
def api_get_user():
    """获取当前用户信息（返回 JSON）"""
    if not current_user.is_authenticated:
        return jsonify({'code': 401, 'message': '未登录'}), 401

    return jsonify({
        'code': 200,
        'user_id': current_user.id,
        'email': current_user.email
    }), 200