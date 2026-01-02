import sqlite3, os
DB_NAME = os.path.join('.', 'menu.db')
conn = sqlite3.connect(DB_NAME)
c = conn.cursor()
c.execute('SELECT sql FROM sqlite_master WHERE type="table" AND name="menu_items"')
result = c.fetchone()
print(result)
conn.close()