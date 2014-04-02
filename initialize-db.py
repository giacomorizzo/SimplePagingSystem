import sqlite3
import hashlib

with sqlite3.connect('sqlite3storage.db') as db:
	dbHandler = db.cursor()
	dbHandler.execute("CREATE TABLE notifications (id integer primary key, status varchar, message varchar, requester integer, receiver integer, created varchar, expires varchar)")
	dbHandler.execute("CREATE TABLE users (uid integer primary key, username varchar, password varchar)")

	dbHandler.execute("INSERT INTO users(username, password) values (?, ?)", ('giacomo', hashlib.md5('giacomo'.encode('utf-8')).hexdigest()))
	dbHandler.execute("INSERT INTO users(username, password) values (?, ?)", ('alarming', hashlib.md5('system'.encode('utf-8')).hexdigest()))
	dbHandler.execute("INSERT INTO users(username, password) values (?, ?)", ('username', hashlib.md5('password'.encode('utf-8')).hexdigest()))
