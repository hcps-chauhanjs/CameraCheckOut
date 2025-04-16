'''
As I leave my desk today, I could hardly imagine the pain you would feel at being met with such a website with little guidance than your feeble knowledge gained over merely the last 2 days.
Thus, I will explain in simple english -- plain indeed:
I have created 5 different equipment inputs, both in the forms.py and in the html itself.
I haven't, however, created a way to access the inputs from each of the equipment IDs, nor have i figured out how to add each equipment id to the sql table.

Another problem that you absolutely must fix with utmost priority: Each equipment id input field is REQUIRED, but only one -- preferably the topmost -- must be required, and everything else not.

Appreciate your help sir, and I look forward to our reconvening

P.S: I would certainly delete this text or paste it in notepad and view with from there as Python -- being the stickler that is -- hates having floating strings in and about its file.


Why on earth did I write like an old english gentleman
'''








import os
import psycopg2
import secrets
from datetime import datetime
from forms import CourseForm
from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect
# from forms import CourseForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key blah blah'

secret_key = secrets.token_hex(16)

def get_db_connection():
    load_dotenv()
    conn = psycopg2.connect(
        host = "drhscit.org",
        database = os.getenv('DB'),
        user = os.getenv('DB_UN'),
        password = os.getenv('DB_PW')
    )
    return conn

@app.route('/', methods=['GET', 'POST'])
def create():
    form = CourseForm()
    if request.method == 'POST':
        if form.validate_on_submit(): #if fields filled properly
            #add to sql table
            student_id = request.form['studentId']
            equipment_ids = request.form.getlist('equipments')
            now = datetime.now()
            date = now.date()
            time = now.strftime("%H:%M:%S")
            
            conn = get_db_connection()
            cur = conn.cursor()
            for equipment_id in equipment_ids:
                cur.execute('INSERT INTO currently_checked_out(student_id, equipment_id, date, time)'
                            'VALUES (%s, %s, %s, %s)',
                            (student_id, equipment_id, date, time))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('create'))
        return render_template('create.html', form=form, checked_out = []) #if not validated, you stay on the page
    
    conn = get_db_connection()
    cur = conn.cursor()
    # SQL query to join currently_checked_out with students and equipment tables
    cur.execute('''
        SELECT 
        s.first_name,
        s.last_name,
        COALESCE(l.brand, h.brand, c.brand) AS equipment_brand,
        COALESCE(l.model, h.model, c.model) AS equipment_model,
        COALESCE(l.num, h.num, c.num) AS equipment_num,
        co.date,
        co.time,
        co.student_id,
        co.equipment_id
        FROM currently_checked_out as co
        JOIN students as s ON co.student_id = s.student_id
        LEFT JOIN lens as l ON co.equipment_id = l.badge_num
        LEFT JOIN hard_drives as h ON co.equipment_id = h.badge_num
        LEFT JOIN cameras as c ON co.equipment_id = c.badge_num
                ''')

    data = cur.fetchall()
    cur.close()
    conn.close()

    
    return render_template('create.html', form=form, checked_out = data)

@app.route('/main-list/')
def mainList():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('main-list.html', all_students=data)

@app.route('/history/', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        print("POST METHOD!")
        student_id = request.form['hStudentId']
        equipment_id = request.form['hEquipmentId']
        now = datetime.now()
        date = now.date()
        time = now.strftime("%H:%M:%S")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM currently_checked_out WHERE student_id = %s AND equipment_id = %s', (student_id, equipment_id))
        cur.execute('INSERT INTO returned (student_id, equipment_id, date, time)'
                    'VALUES (%s, %s, %s, %s)',
                    (student_id, equipment_id, date, time))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('create'))
    print("GET METHOD")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        SELECT 
        s.first_name,
        s.last_name,
        COALESCE(l.brand, h.brand, c.brand) AS equipment_brand,
        COALESCE(l.model, h.model, c.model) AS equipment_model,
        COALESCE(l.num, h.num, c.num) AS equipment_num,
        r.date,
        r.time
        FROM returned as r
        JOIN students as s ON r.student_id = s.student_id
        LEFT JOIN lens as l ON r.equipment_id = l.badge_num
        LEFT JOIN hard_drives as h ON r.equipment_id = h.badge_num
        LEFT JOIN cameras as c ON r.equipment_id = c.badge_num
        ORDER BY r.date DESC, r.time DESC
        ''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('history.html', returned=data)

if __name__ == '__main__':
    app.run(debug=True)