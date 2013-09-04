import sqlite3
from flask import *
from contextlib import closing

DATABASE = r'C:\Users\liam\AppData\Local\Temp\flaskr.db'
DEBUG = True
SECRET_KEY = 'super secret development key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

@app.route('/')
def all_posts():
	cur = g.db.execute('select title, content from posts order by id asc')
	posts = [dict(title=row[0], content = row[1]) for row in cur.fetchall()]
	return render_template('all_posts.html', posts = posts)

@app.route('/make', methods=['POST'])
def make_post():
	g.db.execute('insert into posts (title, content) values (?, ?)',
					[request.form['title'], request.form['content']])
	g.db.commit()
	flash('New post added')
	return redirect(url_for('all_posts'))

if __name__ == '__main__':
	app.run()