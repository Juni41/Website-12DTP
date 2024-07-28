from flask import Flask, render_template
import sqlite3
app = Flask(__name__)  # Create flask object

DATABASE = '/Website-12DTP/league.db'  # DataBase is located outside the project folder


def get_db_connection():
    conn = sqlite3.connect('league.db')
    conn.row_Factory = sqlite3.row
    return conn


@app.route('/char/<int:id>')  # route for champions
def char(id):
    conn = sqlite3.connect('league.db')  # Get connection to Database
    cur = conn.cursor()
    cur.execute('SELECT * FROM Champions WHERE id=?', (id,))
    champ = cur.fetchone()
    return render_template("champions.html", champ=champ)
    if char is None:
        return render_template("404.html")


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
    return render_template('champion_list.html')


def get_item_combinations_for_champions():
    conn = get_db_connection()
    query = '''
    'SELECT FROM Champions where Champ_name'

def get_champion_runes()
    conn = get_db_connection()
    query = '''
    'SELECT FROM Champions where Champ_name'


if __name__ == "__main__":
    app.run(debug=True)
