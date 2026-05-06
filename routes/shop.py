from flask import Blueprint, render_template, request, jsonify  # 加上 jsonify
from models import Product
from extensions import db

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def index():
    # 商品列表，支持搜索和筛选
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    query = Product.query
    if search:
        query = query.filter(Product.name.contains(search))
    if category:
        query = query.filter_by(category=category)
    products = query.all()
    # 获取所有分类供筛选使用
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    return render_template('index.html', products=products, search=search, category=category, categories=categories)

@shop_bp.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

# ========== 新增：API 接口 ==========

@shop_bp.route('/api/products', methods=['GET'])
def api_products():
    """获取商品列表接口"""
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'category': p.category
    } for p in products])

@shop_bp.route('/api/product/<int:id>', methods=['GET'])
def api_product_detail(id):
    """获取单个商品详情接口"""
    product = Product.query.get(id)
    if not product:
        return jsonify({'error': '商品不存在'}), 404
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'description': product.description
    })