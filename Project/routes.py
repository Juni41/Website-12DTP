from flask import Flask, abort, render_template
import sqlite3
app = Flask(__name__)  # Create flask object

DATABASE = 'league.db'  # Path to Database


def get_db_connection():  # Establish Database Connection
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def get_best_items_for_champion(champion_id):  # Function for 3 best items for champion
    with get_db_connection() as conn:
        items = conn.execute('''
            SELECT Items.name
            FROM Items
            JOIN Champions_Item_Combinations ON Items.id =
            Champions_Item_Combinations.item_id
            WHERE Champions_Item_Combinations.champion_id = ?
            LIMIT 3
        ''', (champion_id,)).fetchall()
    return items


@app.route('/char/<int:id>')  # Route for champion details
def char(id):
    with get_db_connection() as conn:
        champ = conn.execute('SELECT * FROM Champions WHERE id=?', (id,)).fetchone()
    if champ is None:  # If no champion is found, return 404 error
        abort(404)
    items = get_best_items_for_champion(id)
    return render_template("champions.html", champ=champ, items=items)


@app.route('/gear/<int:id>')  # route for items
def gear(id):
    with get_db_connection() as conn:
        item = conn.execute('SELECT * FROM Items WHERE id=?', (id,)).fetchone()
    if item is None:  # If no item is found, return 404 error
        abort(404)
    return render_template("items.html", item=item)


@app.route('/')  # layout template
def templatepage():
    return render_template('home.html')


@app.route('/Guide')
def guidepage():
    return render_template('guide.html')


@app.route('/items')
def item_listpage():
    return render_template('item_list.html')


@app.route('/synergies')
def champion_synergies():
    with get_db_connection() as conn:
        query = """
        SELECT adc.name AS adc_name,
               champions.name AS champion_name
        FROM champion_synergies
        JOIN adc ON champion_synergies.adc_id = adc.id
        JOIN champions ON champion_synergies.champion_id = champions.id;
        """
        synergies = conn.execute(query).fetchall()

    synergies = [  # Put results in this dictionary
        {
            # Dictionary contents
            'adc_name': synergy['adc_name'],
            'champion_name': synergy['champion_name'],
            # Image paths
            'adc_icon': f"/static/images/ADC_Icons/{synergy['adc_name']}Square.png",
            'support_icon': f"/static/images/Champion_Icons/{synergy['champion_name']}Square.png"
        }
        for synergy in synergies  #Iterate
    ]
    return render_template('synergies.html', synergies=synergies)


@app.route('/champions')  # Champions List
def champion_listpage():
    # Fetch the list of champions
    with get_db_connection() as conn:
        champions = conn.execute('SELECT id, name FROM Champions').fetchall()
    return render_template('champion_list.html', champions=champions)


# 404 error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 500 error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)
