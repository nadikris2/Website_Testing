from flask import Flask, render_template, request, redirect, url_for
import sqlite3, os

application = Flask(__name__, template_folder='templates', static_folder='static')
application.config['DB_NAME'] = os.getcwd() + '/dbLibrary.db'

con = cursor = None

def openDb():
    global con, cursor
    con = sqlite3.connect(application.config['DB_NAME'])
    cursor = con.cursor()

def closeDb():
    global con, cursor
    cursor.close()
    con.close

@application.route('/')
def index():
    return render_template('index.html')

@application.route('/listed')
def listed():
    openDb()
    container = []
    for id,merk,harga,stok in cursor.execute('SELECT * FROM tHp'):
        container.append((id,merk,harga,stok))
    closeDb()
    return render_template('listhp.html', container=container)

@application.route('/inputData', methods=['GET','POST'])
def inputData():
    if request.method == 'POST':
        id = request.form['txtID']
        judul = request.form['txtMerk']
        penulis = request.form['txtHarga']
        penerbit = request.form['txtStok']
        data = id, judul, penulis, penerbit
        openDb()
        cursor.execute('INSERT INTO tHp VALUES(?,?,?,?)', data)
        con.commit()
        closeDb()
        return redirect(url_for('listed'))
    else:
        return render_template('inputform.html')

@application.route('/ubahData/<id>', methods=['GET','POST'])
def ubahData(id):
    openDb()
    hasil = cursor.execute('SELECT * FROM tHp WHERE id=?', (id,))
    data = cursor.fetchone()
    if request.method == 'POST':
        id = request.form['txtID']
        merk = request.form['txtMerk']
        harga = request.form['txtHarga']
        stok = request.form['txtStok']
        cursor.execute('''UPDATE tHp SET merk=?, harga=?, stok=? WHERE id=?''', \
                       (merk, harga, stok, id))
        con.commit()
        closeDb()
        return redirect(url_for('listed'))
    else:
        closeDb()
        return render_template('ubahdata.html', data=data)

@application.route('/hapusData/<id>', methods=['GET','POST'])
def hapusData(id):
    openDb()
    cursor.execute('DELETE FROM tHp WHERE id=?', (id,))
    con.commit()
    closeDb()
    return redirect(url_for('listed'))

if __name__ == '__main__':
    application.run(debug=True)
    