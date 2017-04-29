# Endpoint				Result					CRUD	HTTP
# /api/songs			Returns all songs		Read	GET
# /api/song/<song_id>	Returns a single song	Read	GET
# /api/songs			Adds a single song		Create	POST
# /api/song/<song_id>	Updates a single song	Update	PUT
# /api/song/<song_id>	Deletes a single song	Delete	DELETE

import sqlite3
from flask import Flask, request, jsonify
import json


app = Flask(__name__)

# helper functions
def add_song(artist, title, rating):
	try:
		with sqlite3.connect('songs.db') as connection:
			cursor = connection.cursor()
			cursor.execute("""
				INSERT INTO songs (artist, title, rating) values (?, ?, ?);
				""", (artist, title, rating,))
			result = {'status': 1, 'message': 'Song Added'}
	except:
		# raise e
		result = {'status': 0, 'message': 'error'}
	return result

def get_all_songs():
	with sqlite3.connect('songs.db') as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM songs ORDER By id desc")
		all_songs = cursor.fetchall()
		return all_songs

def get_single_song(song_id):
	with sqlite3.connect('songs.db') as connection:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
		song = cursor.fetchone()
		return song

def edit_song(song_id, artist, title, rating):
	try:
		with sqlite3.connect('songs.db') as connection:
			connection.execute("UPDATE songs SET artist = ?, title = ?, rating = ? WHERE ID = ?;", (artist, title, rating, song_id,))
			result = {'status': 1, 'message': 'SONG Edited'}
	except:
		result = {'status': 0, 'message': 'Error'}
	return result

def delete_song(song_id):
	try:
		with sqlite3.connect('songs.db') as connection:
			connection.execute("DELETE FROM songs WHERE ID = ?;", (song_id,))
			result = {'status': 1, 'message': 'SONG Deleted'}
	except:
		result = {'status': 0, 'message': 'Error'}
	return result


@app.route('/api/songs', methods=['GET', 'POST'])
def collection():
	if request.method == 'GET':
		# pass
		all_songs = get_all_songs()
		return json.dumps(all_songs)
	elif request.method == 'POST':
		# pass
		data = request.form 
		result = add_song(data['artist'], data['title'], data['rating'])
		return jsonify(result)

@app.route('/api/song/<song_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(song_id):
	if request.method == 'GET':
		# pass
		song = get_single_song(song_id)
		return json.dumps(song)
		# return jsonify(song)
	elif request.method == 'PUT':
		# pass
		data = request.form
		result = edit_song(
			song_id, data['artist'], data['title'], data['rating']
			)
		return jsonify(result)
	elif request.method == 'DELETE':
		# pass
		result = delete_song(song_id)
		return jsonify(result)

if __name__ == '__main__':
	app.debug = True
	app.run()