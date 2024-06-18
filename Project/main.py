from flask import Flask, render_template
import sqlite3
app = Flask(__name__) #Create flask object

DATABASE = '/Website-12DTP/Project/league.db'

def get_db_connection():
  conn = sqlite3.connect('league.db')
  conn.row_Factory = sqlite3.row
  return conn
  
@app.route('/char/<int:id>')
def char(id):
  conn = sqlite3.connect('league.db')
  cur = conn.cursor()
  cur.execute('SELECT * FROM Champions WHERE id?', (id,))
  champ = cur.fetchone()
  return render_template(champions.html", champ = champ)


@app.route('/')
def homepage():
  return render_template('Home.html')

@app.route('/about')
def aboutpage():
  return render_template('about.html')


if __name__=="__main__":
  app.run(debug=True)