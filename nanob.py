import sqlite3
from flask import *
from contextlib import closing

#Put the database in the /tmp directory
DATABASE = '/tmp/nanob.db'
DEBUG = True
#session key
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
	#retrieve all posts from the db and pass them to the all_posts.html template
	cur = g.db.execute('select title, content, id from posts order by id asc')
	posts = [dict(title=row[0], content = row[1], post_id = row[2]) for row in cur.fetchall()]
	return render_template('all_posts.html', posts = posts)

@app.route('/make', methods=['POST'])
def make_post():
	title = request.form['title']
	if title == "":
		flash('Your post has no title')
		return redirect(url_for('all_posts'))

	g.db.execute('insert into posts (title, content) values (?, ?)',
					[title, request.form['content']])
	g.db.commit()
	flash('New post added')
	return redirect(url_for('all_posts'))

@app.route('/delete_post', methods=['POST'])
def delete_post():
	post_id = request.form['post_to_delete']
	g.db.execute('delete from posts where id = ?;', [post_id])
	g.db.commit()
	flash('Post successfully deleted')
	return redirect(url_for('all_posts'))

if __name__ == '__main__':
	app.run()
