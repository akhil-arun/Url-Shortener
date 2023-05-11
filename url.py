from flask import Flask, request, jsonify
import sqlite3
import string
import random, math

app = Flask(__name__)
DB_NAME = 'url.db'


def create_table():
    # SQLite Database setup if required
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS url (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT NOT NULL, short_url TEXT NOT NULL)")
    conn.commit()
    conn.close()

def shorten_url(length):
    # There will be one character for every 4 characters in the original url
    shorten_len = math.ceil(length / 4)
    
    # The new url will contain alphanumeric characters
    char_set = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(char_set) for _ in range(shorten_len))
    
    # Add http back to the shortend url
    short_url = "http://" + short_url
    return short_url

@app.route('/encode')
def encode():
    # Get the url to be encoded
    long_url = request.args.get('url')
    
    # If nothing is passed in, throw 400 error
    if not long_url:
        return jsonify({'error': 'No url found'}), 400
    
    short_url = ""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Check if the long URL already exists in the database
    c.execute("SELECT short_url FROM url WHERE long_url=?", (long_url,))
    
    # Get the first row of the result
    result = c.fetchone()
    
    # If result is not none, then long_url already has decoding
    if result:
        short_url = result[0]
    else:
        # Get url after the http(s)://
        second_half_url = long_url.split("://")[1]
        
        # Shorten the url and add the mapping to the database
        short_url = shorten_url(len(long_url))
        c.execute("INSERT INTO url (long_url, short_url) VALUES (?, ?)",
                  (long_url, short_url))
        conn.commit()
    
    conn.close()
    
    # Return encoded url in JSON
    return jsonify({'encoded_url': short_url}), 200

@app.route('/decode')
def decode():
    # Get the url to be decoded
    short_url = request.args.get('url')

    if not short_url:
        return jsonify({'error': 'No url found'}), 400
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Check if the short URL exists in the database
    c.execute("SELECT long_url FROM url WHERE short_url=?", (short_url,))
    result = c.fetchone()
    long_url = ""

    # If shortened url exists in DB, then get the long_url. Else, throw an error
    if result:
        long_url = result[0]
    else:
        return jsonify({'error': 'A mapping from this url to an original url does not exist'}), 400

    conn.close()
    
    # Return decoded url in JSON
    return jsonify({'decoded_url': long_url}), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
