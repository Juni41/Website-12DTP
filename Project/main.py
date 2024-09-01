from flask import Flask, abort, render_template
import sqlite3
app = Flask(__name__)  # Create flask object

DATABASE = '/Website-12DTP/league.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_best_items_for_champion(champion_id):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''
        SELECT Items.name
        FROM Items
        JOIN Champions_Item_Combinations ON Items.id = Champions_Item_Combinations.item_id
        WHERE Champions_Item_Combinations.champion_id = ?
        LIMIT 3
    ''', (champion_id,))
    items = cur.fetchall()
    conn.close()
    return items


@app.route('/char/<int:id>')  # route for champions
def char(id):
    conn = sqlite3.connect(DATABASE)  # Get connection to Database
    cur = conn.cursor()
    cur.execute('SELECT * FROM Champions WHERE id=?', (id,))
    champ = cur.fetchone()
    if champ is None:
        abort(404)
    
   
    items = get_best_items_for_champion(id)
    return render_template("champions.html", champ=champ, items=items)


@app.route('/gear/<int:id>')  # route for items
def gear(id):
    conn = sqlite3.connect('league.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM Items WHERE id=?', (id,))
    item = cur.fetchone()
    if gear is None:
        abort(404)
    return render_template("items.html", item=item)


@app.route('/')  # layout template
def templatepage():
    return render_template('layout.html')


@app.route('/Home')
def homepage():
    render_template('home.html')


@app.route('/Guide')
def guidepage():
    return render_template('guide.html')


@app.route('/about')
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
