from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')  # Menggunakan variabel lingkungan
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Model untuk User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # Menandakan apakah user adalah admin

# Model untuk Produk
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Halaman login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('home'))
    return render_template('login.html')

# Halaman beranda
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Stok barang
@app.route('/stock')
def stock():
    products = Product.query.all()  # Ambil semua produk dari database
    return render_template('stock.html', products=products)

# Tambahkan produk
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        stock = int(request.form['stock'])
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('stock'))
    return render_template('add_product.html')

# Edit produk
@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = float(request.form['price'])
        product.stock = int(request.form['stock'])
        db.session.commit()
        return redirect(url_for('stock'))
    return render_template('edit_product.html', product=product)

# Hapus produk
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('stock'))

# Pengelola transaksi
@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

# Laporan penjualan
@app.route('/sales-report')
def sales_report():
    return render_template('sales_report.html')

# Pengelola struk
@app.route('/receipt-manager')
def receipt_manager():
    return render_template('receipt_manager.html')

# Daftar barang masuk dan keluar
@app.route('/inventory')
def inventory():
    return render_template('inventory.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# Buat database dan tambahkan admin jika belum ada
def create_db():
    with app.app_context():
        db.create_all()  # Buat database
        # Tambahkan admin jika belum ada
        if User.query.filter_by(username='admin').first() is None:
            admin = User(username='admin', password='admin', is_admin=True)  # Ganti 'admin_password' sesuai kebutuhan
            db.session.add(admin)
            db.session.commit()

if __name__ == '__main__':
    create_db()  # Membuat database dan menambahkan admin
    app.run(debug=True)
