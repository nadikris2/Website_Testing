import sqlite3
con = sqlite3.connect('dbLibrary.db')
cursor = con.cursor()
cursor.execute('''CREATE TABLE tHp(id CHAR(4) NOT NULL PRIMARY KEY, Merk VARCHAR(40), Harga VARCHAR(25), Stok VARCHAR(30))''')
con.commit()
cursor.close()
con.close()