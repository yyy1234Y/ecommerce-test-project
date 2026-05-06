from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify  # 加上 jsonify
from flask_login import login_required, current_user
from extensions import db
from models import Cart, Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/')
@login_required
def view_cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)


@cart_bp.route('/add/<int:product_id>')
@login_required
def add(product_id):
    product = Product.query.get_or_404(product_id)
    cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    db.session.commit()
    flash(f'已添加 {product.name} 到购物车')
    return redirect(url_for('shop.product_detail', id=product_id))


@cart_bp.route('/update/<int:item_id>', methods=['POST'])
@login_required
def update(item_id):
    cart_item = Cart.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return '无权操作', 403
    quantity = int(request.form.get('quantity', 1))
    if quantity <= 0:
        db.session.delete(cart_item)
    else:
        cart_item.quantity = quantity
    db.session.commit()
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/remove/<int:item_id>')
@login_required
def remove(item_id):
    cart_item = Cart.query.get_or_404(item_id)
    if cart_item.user_id == current_user.id:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart.view_cart'))


# ========== 新增：购物车 API 接口 ==========

@cart_bp.route('/api/cart', methods=['GET'])
@login_required
def api_get_cart():
    """获取购物车内容（JSON格式）"""
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    items = []
    total = 0
    for item in cart_items:
        product = item.product
        subtotal = product.price * item.quantity
        total += subtotal
        items.append({
            'id': item.id,
            'product_id': product.id,
            'product_name': product.name,
            'price': product.price,
            'quantity': item.quantity,
            'subtotal': subtotal
        })
    return jsonify({
        'code': 200,
        'items': items,
        'total': total,
        'count': len(items)
    })


@cart_bp.route('/api/cart/add', methods=['POST'])
@login_required
def api_add_to_cart():
    """添加商品到购物车（API）"""
    data = request.get_json()
    if not data:
        return jsonify({'code': 400, 'message': '请求体不能为空'}), 400

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'code': 400, 'message': 'product_id 不能为空'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'code': 404, 'message': '商品不存在'}), 404

    cart_item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = Cart(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)

    db.session.commit()

    return jsonify({
        'code': 200,
        'message': f'已添加 {product.name} 到购物车',
        'product_id': product_id,
        'quantity': cart_item.quantity
    })


@cart_bp.route('/api/cart/item/<int:item_id>', methods=['DELETE'])
@login_required
def api_remove_cart_item(item_id):
    """删除购物车商品"""
    cart_item = Cart.query.get_or_404(item_id)
    if cart_item.user_id != current_user.id:
        return jsonify({'code': 403, 'message': '无权操作'}), 403

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({'code': 200, 'message': '删除成功'})