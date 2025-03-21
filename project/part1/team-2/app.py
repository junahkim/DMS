from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
DATABASE_URL = "postgresql://neondb_owner:npg_M5sVheSzQLv4@ep-shrill-tree-a819xf7v-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.route('/')
def index():
    return redirect('/team2_flowers')

@app.route('/team2_flowers')
def manage_flowers():
    print("Rendering team2_flowers.html")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM team2_flowers")
    flowers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('team2_flowers.html', flowers=flowers)

@app.route('/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    last_watered = request.form['last_watered']
    water_level = int(request.form['water_level'])
    min_water_required = int(request.form['min_water_required'])

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO team2_flowers (name, last_watered, water_level, min_water_required) VALUES (%s, %s, %s, %s)",
                (name, last_watered, water_level, min_water_required))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/team2_flowers')

@app.route('/delete_flower/<int:flower_id>')
def delete_flower(flower_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM team2_flowers WHERE id = %s", (flower_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/team2_flowers')

@app.route('/team2_flowers_water_loss')
def water_loss():
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Run the SQL update query to decrease the water level
        cur.execute("""
            UPDATE team2_flowers
            SET water_level = water_level - (5 * (CURRENT_DATE - last_watered))
        """)
        conn.commit()
        print("Water levels updated successfully.")
    except Exception as e:
        print(f"Error updating water levels: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect('/team2_flowers')  # Redirect back to the flowers page to see updated values

if __name__ == '__main__':
    app.run(debug=True)
