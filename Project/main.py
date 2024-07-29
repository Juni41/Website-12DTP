from flask import Flask, abort, render_template
import sqlite3
app = Flask(__name__)  # Create flask object

DATABASE = '/Website-12DTP/league.db'  # DataBase is located outside the project folder


def get_db_connection():
    conn = sqlite3.connect('league.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/char/<int:id>')  # route for champions
def char(id):
    conn = sqlite3.connect('league.db')  # Get connection to Database
    cur = conn.cursor()
    cur.execute('SELECT * FROM Champions WHERE id=?', (id,))
    champ = cur.fetchone()
    if champ is None:
        abort(404)
    return render_template("champions.html", champ=champ)



@app.route('/gear/<int:id>')  # route for items
def gear(id):
    conn = sqlite3.connect('league.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Items WHERE id=?', (id,))
    item = cur.fetchone()
    return render_template("items.html", item=item)
    if gear is None:
        return render_template("404.html")


@app.route('/')  # Homepage template
def homepage():
    return render_template('Home.html')


@app.route('/about')  # About page template that is placed between block content of the home page
def aboutpage():
    return render_template('about.html')


@app.route('/items')
def item_listpage():
    return render_template('item_list.html')


@app.route('/champions')
def champion_listpage():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name FROM Champions')
    champions = cur.fetchall()
    conn.close()
    return render_template('champion_list.html', champions=champions)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True)
