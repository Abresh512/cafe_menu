from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2 import pool
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)

# Upload config
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database
def init_db():
    conn = pool.getconn()
    try:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS menu_items (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT NOT NULL,
                image TEXT
            )
        ''')
        conn.commit()
    finally:
        pool.putconn(conn)

init_db()

@app.route('/')
def index():
    category = request.args.get('category', 'All')
    conn = pool.getconn()
    try:
        c = conn.cursor()
        if category == 'All':
            c.execute("SELECT * FROM menu_items")
        else:
            c.execute("SELECT * FROM menu_items WHERE category = %s", (category,))
        items = c.fetchall()
    finally:
        pool.putconn(conn)
    return render_template('index.html', items=items, current_category=category)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        image = request.files.get('image')

        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = pool.getconn()
        try:
            c = conn.cursor()
            c.execute(
                "INSERT INTO menu_items (name, price, category, image) VALUES (%s, %s, %s, %s)",
                (name, price, category, filename)
            )
            conn.commit()
        finally:
            pool.putconn(conn)

        return redirect(url_for('index'))

    return render_template('add_item.html')


@app.route('/admin')
def admin():
    conn = pool.getconn()
    try:
        c = conn.cursor()
        c.execute("SELECT * FROM menu_items")
        items = c.fetchall()
    finally:
        pool.putconn(conn)
    return render_template('admin.html', items=items)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = pool.getconn()
    try:
        c = conn.cursor()
        c.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
        conn.commit()
    finally:
        pool.putconn(conn)
    return redirect(url_for('admin'))


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        category = request.form['category']
        image = request.files.get('image')

        filename = None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        conn = pool.getconn()
        try:
            c = conn.cursor()
            if filename:
                c.execute("UPDATE menu_items SET name = %s, price = %s, category = %s, image = %s WHERE id = %s", (name, price, category, filename, item_id))
            else:
                c.execute("UPDATE menu_items SET name = %s, price = %s, category = %s WHERE id = %s", (name, price, category, item_id))
            conn.commit()
        finally:
            pool.putconn(conn)
        return redirect(url_for('admin'))
    else:
        conn = pool.getconn()
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM menu_items WHERE id = %s", (item_id,))
            item = c.fetchone()
        finally:
            pool.putconn(conn)
        return render_template('edit_item.html', item=item)


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

# WSGI entry point for production
application = app
