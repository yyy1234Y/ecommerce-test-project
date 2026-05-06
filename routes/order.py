from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify  # 加上 jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Cart, Order, OrderItem

order_bp = Blueprint('order', __name__)


@order_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('购物车为空')
        return redirect(url_for('shop.index'))
    total = sum(item.product.price * item.quantity for item in cart_items)
    if request.method == 'POST':
        address = request.form['address']
        # 创建订单
        order = Order(user_id=current_user.id, total_amount=total, address=address, status='pending')
        db.session.add(order)
        db.session.commit()
        # 创建订单项
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            db.session.add(order_item)
        # 清空购物车
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash('订单已创建，请等待处理')
        return redirect(url_for('order.list_orders'))
    return render_template('checkout.html', total=total)


@order_bp.route('/list')
@login_required
def list_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)


@order_bp.route('/status/<int:order_id>')
@login_required
def status(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        return '无权查看', 403
    return render_template('order_status.html', order=order)


# ========== 新增：订单 API 接口 ==========

@order_bp.route('/api/orders', methods=['GET'])
@login_required
def api_get_orders():
    """获取当前用户的订单列表"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()

    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'address': order.address,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'items_count': len(order.items) if order.items else 0
        })

    return jsonify({
        'code': 200,
        'orders': orders_data,
        'count': len(orders_data)
    })


@order_bp.route('/api/order/<int:order_id>', methods=['GET'])
@login_required
def api_get_order_detail(order_id):
    """获取单个订单详情"""
    order = Order.query.get_or_404(order_id)

    # 权限校验
    if order.user_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权查看此订单'}), 403

    items = []
    for item in order.items:
        items.append({
            'id': item.id,
            'product_id': item.product_id,
            'product_name': item.product_name,
            'price': item.price,
            'quantity': item.quantity,
            'subtotal': item.price * item.quantity
        })

    return jsonify({
        'code': 200,
        'order': {
            'id': order.id,
            'total_amount': order.total_amount,
            'status': order.status,
            'address': order.address,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'items': items
        }
    })


@order_bp.route('/api/order/create', methods=['POST'])
@login_required
def api_create_order():
    """创建订单（API 方式）"""
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '请求体不能为空'}), 400

    address = data.get('address')
    if not address:
        return jsonify({'code': 400, 'message': '地址不能为空'}), 400

    # 获取购物车商品
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        return jsonify({'code': 400, 'message': '购物车为空'}), 400

    # 计算总金额
    total = sum(item.product.price * item.quantity for item in cart_items)

    # 创建订单
    order = Order(
        user_id=current_user.id,
        total_amount=total,
        address=address,
        status='pending'
    )
    db.session.add(order)
    db.session.commit()

    # 创建订单项
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product.name,
            price=item.product.price,
            quantity=item.quantity
        )
        db.session.add(order_item)

    # 清空购物车
    Cart.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '订单创建成功',
        'order_id': order.id,
        'total_amount': total,
        'status': 'pending'
    }), 201


@order_bp.route('/api/order/<int:order_id>/cancel', methods=['PUT'])
@login_required
def api_cancel_order(order_id):
    """取消订单（仅 pending 状态可取消）"""
    order = Order.query.get_or_404(order_id)

    # 权限校验
    if order.user_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权操作此订单'}), 403

    # 状态校验
    if order.status != 'pending':
        return jsonify({'code': 400, 'message': f'订单状态为 {order.status}，无法取消'}), 400

    order.status = 'cancelled'
    db.session.commit()

    return jsonify({
        'code': 200,
        'message': '订单已取消',
        'order_id': order.id,
        'status': order.status
    })