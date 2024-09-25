from flask import Flask, abort, render_template
import sqlite3
import os

app = Flask(__name__)  # Create flask object

DATABASE = 'league.db'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'league.db')


def get_db_connection():  # Function for database connection
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Queries
def get_champion_by_id(champion_id):
    """Fetch champion details by id"""
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM Champions WHERE id=?',
                            (champion_id,)).fetchone()


def get_adc_by_id(adc_id):
    """Fetch ADC details by id"""
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM ADC WHERE id=?',
                            (adc_id,)).fetchone()


def get_item_by_id(item_id):
    """Fetch item details by id"""
    with get_db_connection() as conn:
        return conn.execute('SELECT * FROM Items WHERE id=?',
                            (item_id,)).fetchone()


def get_best_items_for_champion(champion_id):
    """Fetch the best items for a support"""
    with get_db_connection() as conn:
        return conn.execute('''
            SELECT Items.name
            FROM Items
            JOIN Champions_Item_Combinations ON Items.id =
            Champions_Item_Combinations.item_id
            WHERE Champions_Item_Combinations.champion_id = ?
            LIMIT 3
        ''', (champion_id,)).fetchall()


def get_champion_list():
    """Fetch the list of champions."""
    with get_db_connection() as conn:
        return conn.execute('SELECT id, name FROM Champions').fetchall()


def get_adc_list():
    """Fetch the list of ADCs."""
    with get_db_connection() as conn:
        return conn.execute('SELECT id, name FROM ADC').fetchall()


def get_items_list():
    """Fetch the list of items."""
    with get_db_connection() as conn:
        return conn.execute('SELECT id, name FROM Items').fetchall()


def get_champion_synergies():
    """Fetch champion synergies."""
    query = """
    SELECT adc.name, champions.name
    FROM champion_synergies
    JOIN adc ON champion_synergies.adc_id = adc.id
    JOIN champions ON champion_synergies.champion_id = champions.id;
    """
    with get_db_connection() as conn:
        synergies = conn.execute(query).fetchall()

    # Prepare synergy data for rendering
    return [
        {
            'adc_name': adc,
            'champion_name': champ,
            'adc_icon': f"/static/images/ADC_Icons/{adc}Square.png",
            'support_icon': f"/static/images/Champion_Icons/{champ}Square.png"
        }
        for adc, champ in synergies
    ]


# Routes
@app.route('/champions/<int:id>/<string:name>')  # Route for champion details
def char(id, name):
    champ = get_champion_by_id(id)
    if champ is None or champ['name'].lower() != name.lower():
        abort(404)  # If no champion is found, return 404 error
    items = get_best_items_for_champion(id)
    return render_template("champions.html", champ=champ, items=items)


@app.route('/adc/<int:id>/<string:name>')  # Route for adc details
def ADC(id, name):
    adc = get_adc_by_id(id)
    if adc is None or adc['name'].lower() != name.lower():
        abort(404)  # If no adc is found, return 404 error
    return render_template("ADCS.html", adc=adc)


@app.route('/items/<int:id>/<string:name>')  # Route for items
def gear(id, name):
    item = get_item_by_id(id)
    if item is None:  # If no item is found, return 404 error
        abort(404)
    return render_template("items.html", item=item)


@app.route('/')  # Layout template
def templatepage():
    return render_template('home.html')


@app.route('/Guide')
def guidepage():
    return render_template('guide.html')


@app.route('/items')
def item_listpage():
    gear = get_items_list()
    return render_template('item_list.html', gear=gear)


@app.route('/synergies')
def champion_synergies():
    synergies = get_champion_synergies()
    return render_template('synergies.html', synergies=synergies)


@app.route('/champions')  # Champions List
def champion_listpage():
    champions = get_champion_list()
    ADC = get_adc_list()
    return render_template('champion_list.html', champions=champions, ADC=ADC)


# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
