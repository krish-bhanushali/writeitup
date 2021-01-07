import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db', 'notes.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    db = get_db()
    with app.open_resource('data/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
        
# Uncomment and use this to initialize database, then comment it
#   You can rerun it to pave the database and start over
# @app.route('/initdb')
# def initdb():
#     init_db()
#     return 'Initialized the database.'

@app.route('/catagories', methods=['POST'])
def create_Catagory():
    if not request.json:
        abort(400)
    catagoryTitle = request.json['cTitle']
    catagoryColor = request.json['cColor']
    db = get_db()
    db.execute('INSERT INTO catagories (catagory_Name,catagory_Color) VALUES (?, ?)',[catagoryTitle,catagoryColor])
    db.commit()
    
    return jsonify({'catagory': 'Added'}), 201

@app.route('/catagories', methods=['GET'])
def show_allCatagories():
    db = get_db()
    query = '''
        SELECT id, catagory_Name, catagory_Color
        FROM catagories
    '''
    cur = db.execute(query)
    resultQuery = cur.fetchall()
    print(resultQuery)
    data = []
    for rows in resultQuery:
        data.append({
            'cId' : rows[0],
            'cName' : rows[1],
            'cColor' : rows[2]
        })
    return jsonify(data)

@app.route('/catagories/<int:catagory_id>', methods=['PUT'])
def update_task(catagory_id):
    db = get_db()
    query = '''
    UPDATE catagories
        SET
          catagory_Name = ?,
          catagory_Color = ?
        WHERE id = ?
    '''
    db.execute(query,[request.json['cTitle'],request.json['cColor'],catagory_id])
    db.commit()

    return jsonify({'catagory': 'updated'}),201


@app.route('/catagories/<int:catagory_id>', methods=['DELETE'])
def delete_task(catagory_id):
    db = get_db()
    query = '''
    DELETE from catagories
        WHERE id = ?
    '''
    db.execute(query,[catagory_id])
    db.commit()

    return jsonify({'catagory': 'deleted'}),201



@app.route('/note', methods=['POST'])
def create_note():
    if not request.json:
        abort(400)
    noteTitle = request.json['nTitle']
    noteMain = request.json['nNote']
    noteDate = request.json['nDate']
    noteCatagory = request.json['nCatagory']

    db = get_db()
    db.execute('INSERT INTO notes (title,note,dateOfNote,catagoryOfNote) VALUES (?, ?,?,?)',[noteTitle,noteMain,noteDate,noteCatagory])
    db.commit()
    
    return jsonify({'note': 'Added'}), 201

@app.route('/note', methods=['GET'])
def show_allnotes():
    db = get_db()
    query = '''
        SELECT *
        FROM notes
    '''
    cur = db.execute(query)
    resultQuery = cur.fetchall()
    print(resultQuery)
    data = []
    for rows in resultQuery:
        data.append({
            'nId' : rows[0],
            'nTitle' : rows[1],
            'nNote' : rows[2],
            'nDate' : rows[3],
            'nCatagory' : rows[4]
        })
    return jsonify(data)

@app.route('/note/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    db = get_db()
    query = '''
    UPDATE notes
        SET
          title = ?,
          note = ?,
          dateOfNote = ?,
          catagoryOfNote = ?
        WHERE id = ?
    '''
    db.execute(query,[request.json['nTitle'],request.json['nNote'],request.json['nDate'],request.json['nCatagory'],note_id])
    db.commit()

    return jsonify({'note': 'updated'}),201


@app.route('/note/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    db = get_db()
    query = '''
    DELETE from notes
        WHERE id = ?
    '''
    db.execute(query,[note_id])
    db.commit()

    return jsonify({'note': 'deleted'}),201



if __name__ == '__main__':
    app.run(debug=True,port=5001)



