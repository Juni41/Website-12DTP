from flask import Flask, render_template
import sqlite3
app = Flask(__name__) #Create flask object

DATABASE = '/Website-12DTP/Project/league.db'

@app.route('/pizz/<int:id>')
def pizz(id):
  conn = sqlite3.connect('league.db')
  cur = conn.cursor()
  cur.execute('SELECT * FROM Pizza WHERE id?', (id,))
  pizza = cur.fetchone()
  return render_template("pizza.html", pizza = pizza)


@app.route('/')
def homepage():
  return render_template('Home.html')

@app.route('/about')
def aboutpage():
  return render_template('about.html')


if __name__=="__main__":
  app.run(debug=True)