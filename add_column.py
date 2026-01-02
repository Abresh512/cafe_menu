import sqlite3
conn = sqlite3.connect('menu.db')
c = conn.cursor()
c.execute("ALTER TABLE menu_items ADD COLUMN category TEXT DEFAULT 'Breakfast'")
conn.commit()
conn.close()
print('Category column added')