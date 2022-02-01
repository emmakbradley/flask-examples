'''
# Local Preview
At the command line: 

conda activate PIC16B
export FLASK_ENV=development; flask run

# Sources:
Lecture notes from class, and flask-examples repository from Professor Chodrow on GitHub
'''
import sqlite3

from flask import Flask, render_template, request, g
app = Flask(__name__)

def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect("messages_db.sqlite")
    g.message_db.execute('''CREATE TABLE IF NOT EXISTS messages(id INTEGER, handle TEXT, message TEXT)''')
    return g.message_db

def insert_message(request):
    # connect to db
    g.message_db = get_message_db()

    # intialize cursor
    cursor = g.message_db.cursor()
    
    # count rows
    cursor.execute("select count(*) from messages")
    rows = cursor.fetchone()[0]
    
    # get message data
    message = request.form["message"]
    handle = request.form["handle"]
    this_id = 1 + rows
    
    # sql cmd
    cmd = f"""INSERT INTO messages (id, handle, message)
    VALUES('{this_id}', '{message}', '{handle}')"""
    
    # add message to db
    cursor.execute(cmd)
    g.message_db.commit()
    
    # close connection
    g.message_db.close()
    return

def random_messages(n):
    # connect to db
    g.message_db = get_message_db()

    # initialize cursor
    cursor = g.message_db.cursor()

    # grab n random messages
    cmd = f"""SELECT * FROM messages ORDER BY RANDOM() LIMIT '{n}'"""
    cursor.execute(cmd)

    messages_list = cursor.fetchall()

    # close database
    g.message_db.close()

    return messages_list

@app.route("/")
def main():
    return render_template('base.html')
    
# getting messages
@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        insert_message(request)
        try:
            return render_template('submit.html', thanks=True)
        except:
            return render_template('submit.hmtl', error=True)

#viewing messages
@app.route('/view/')
def view():
    messages_list = random_messages(3)
    return render_template('view.html', messages_list = messages_list)
    

    


