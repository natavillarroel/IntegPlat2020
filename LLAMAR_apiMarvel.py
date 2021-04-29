import hashlib
import requests
import json
import sqlite3

def main_api():

	public = '09f373fcfa768e430d222371bb8fa72b'
	private = '938bec35fe455307d428886cfb9053c448604669'
	ts = '1'
	hash = hashlib.md5((ts + private + public).encode()).hexdigest()

	base = 'http://gateway.marvel.com/v1/public/'
	caracter = requests.get(base + 'characters',
							params={'apikey': public, 'ts': ts, 'hash' : hash, 'name': 'hulk'}).json()
	nombre = (caracter ['data']['results'][0]['name'])	
	description = (caracter ['data']['results'][0]['description'])

	con = sqlite3.connect("/home/ec2-user/API/bd")
	cursor  = con.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS MARVEL
					(NOMBRE TEXT NOT NULL, 
					 DESCRIPTION TEXT NOT NULL)''')
	cursor.execute('''INSERT  INTO MARVEL (NOMBRE, DESCRIPTION) VALUES (?,?)''', (nombre, description))
	con.commit() #los cambios se guardan
	cursor.execute('''SELECT * FROM MARVEL''')
	print(cursor.fetchall()) #muestro por pantalla
	con.close()

if __name__ == '__main__':
	main_api()