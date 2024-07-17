from flask import Flask, request, jsonify, send_from_directory
from config import Config
import os
import time
import json
import sqlite3
import secrets

app = Flask(__name__)
app.config.from_object(Config)

#Initialize DB
DATABASE = 'player.db'
def create_table():
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS player (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            banned BIT,
                            rating REAL,
                            data TEXT
                        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS rank (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            player_id TEXT,
                            key TEXT,
                            score INTEGER,
                            isFC BOOLEAN,
                            FOREIGN KEY (player_id) REFERENCES player (id)
                        )''')

create_table()

#Helper function for api
def get_player_data(user_id, data_field):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        query = f"SELECT {data_field} FROM player WHERE id = ?"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result
    
def set_player_data(user_id, data_field, new_data):
    with sqlite3.connect(DATABASE) as connection:
        cursor = connection.cursor()
        query = f"UPDATE player SET {data_field} = ? WHERE id = ?"
        cursor.execute(query, (new_data, user_id))
        connection.commit()

#Serving CDN files
root_folder = os.path.dirname(os.path.abspath(__file__))
allowed_folders = ["OverRide", "Resources"]

@app.route('/<path:path>', methods=['GET'])
def get_file(path):
    file_folder = path.split("/")[0]
    if file_folder not in allowed_folders:
        return jsonify({"error": "Access denied"}), 403
    file_path = os.path.join(root_folder, path)
    if os.path.exists(file_path):
        return send_from_directory(root_folder, path)
    else:
        return jsonify({"error": "File not found"}), 404

#API Call functions
@app.route('/Api', methods=['POST'])
def api():
    try:
        #app.logger.info(f"Request data: {request.get_data(as_text=True)}")
        data = request.get_json(force=True)
        content = data.get("Content", "")
        name = data.get("Name", "")
        user_id = data.get("UserId", "")

        if name == "dataDownload":
            content_dict = json.loads(content)
            user_id = content_dict.get("key", "")
            player_data = get_player_data(user_id, "data")
            if player_data:
                return player_data[0]
            else:
                 return jsonify({})

        if name == "UIDCheck":
            content_dict = json.loads(content)
            uid = content_dict.get("key", "")
            with sqlite3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT EXISTS(SELECT 1 FROM player WHERE id = ?)", (uid,))
                result = cursor.fetchone()[0]
            if result:
                return jsonify({"exists": True})
            else:
                return jsonify({"exists": False})

        elif name == "dataUpload":
            try:
                content_json = json.loads(content)["jsonString"]
            except json.JSONDecodeError as e:
                return jsonify({"dummy": False}), 400
            player_exist = get_player_data(user_id, "id")
            if player_exist:
                set_player_data(user_id, "data", json.dumps(content_json))
            elif app.config['REGISTRATION']:
                with sqlite3.connect(DATABASE) as connection:
                    cursor = connection.cursor()
                    cursor.execute('''INSERT INTO player (id, name, banned, rating, data) 
                            VALUES (?, ?, ?, ?, ?)''', (user_id, content_json["name"], 0, 0.0, json.dumps(content_json)))
                    connection.commit()
            return jsonify({"dummy": True})    

        elif name == "nameCheck":
            content_dict = json.loads(content)
            player_name = content_dict.get("name", "")
            with sqlite3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT EXISTS(SELECT 1 FROM player WHERE name = ?)", (player_name,))
                result = cursor.fetchone()[0]
            if app.config['REGISTRATION'] == False:
                return jsonify({"regClosed": True})
            elif result:
                return jsonify({"exists": True})
            else:
                return jsonify({"exists": False})

        elif name == "getName":
            result = get_player_data(user_id, "name")
            banned = get_player_data(user_id, "banned")
            if result:
                if isinstance(banned[0], str) or banned is None:
                    return jsonify({"banned": banned[0]})
                else:
                    return jsonify({"name": result[0]})
            else:
                return jsonify({})

        elif name == "rename":
            try:
                new_name = json.loads(content).get("name", "")
            except ValueError:
                return jsonify({"banned": True})
            banned = get_player_data(user_id, "banned")
            if banned > 0 or banned is None:
                return jsonify({"banned": True})
            else:
                set_player_data(user_id, "name", new_name)
                return jsonify({"banned": False})

        elif name == "rankUpload":
            content_data = json.loads(content)
            key = content_data.get("key", "")
            score = content_data.get("score", 0)
            isFC = content_data.get("isFC", False)
            with sqlite3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT score FROM rank WHERE player_id = ? AND key = ?", (user_id, key))
                result = cursor.fetchone()
                if result is not None:
                    if result[0] < score:
                        cursor.execute('''UPDATE rank SET score = ?, isFC = ? 
                                          WHERE player_id = ? AND key = ?''', (score, isFC, user_id, key))
                        connection.commit()
                else:
                    cursor.execute('''INSERT INTO rank (player_id, key, score, isFC) 
                                VALUES (?, ?, ?, ?)''', (user_id, key, score, isFC))
                    connection.commit()
            return jsonify({"dummy": True})

        elif name == "rankLeaderboard":
            content_data = json.loads(content)
            key_to_match = content_data.get("key", "")
            max_key = content_data.get("maxKey", 99)
            with sqlite3.connect(DATABASE) as connection:
                cursor = connection.cursor()
                cursor.execute('''SELECT player_id, score, isFC FROM rank WHERE key = ?''', (key_to_match,))
                qualified_ranks = cursor.fetchall()
                qualified_ranks.sort(key=lambda x: x[1], reverse=True)
                top_scores = qualified_ranks[:max_key]
                result_list = []
                for player_id, score, isFC in top_scores:
                    cursor.execute('''SELECT name FROM player WHERE id = ?''', (player_id,))
                    player_name = cursor.fetchone()[0]
                    result_list.append({"name": player_name, "score": score, "isFC": bool(isFC)})
                return jsonify(result_list)

    except Exception as e:
        app.logger.info(f"error: {str(e)}")
        return jsonify({"error": str(e)}), 400

#Main
if __name__ == '__main__':
    if app.config['SSL_CERT'] and app.config['SSL_KEY']:
        app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'], ssl_context=(app.config['SSL_CERT'], app.config['SSL_KEY']))
    else:
        app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])

# Made By Tony  2024.1.4