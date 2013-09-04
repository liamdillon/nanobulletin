import os
import nanob
import unittest
import tempfile

class NanobTestCase(unittest.TestCase):

    def setUp(self):
        #create an empty database for testing and store its file descriptor
        #use the flask test client
        self.db_fd, nanob.app.config['DATABASE'] = tempfile.mkstemp()
        nanob.app.config['TESTING'] = True
        self.app = nanob.app.test_client()
        nanob.init_db()

    def tearDown(self):
        #destroy the test database
        os.close(self.db_fd)
        os.unlink(nanob.app.config['DATABASE'])

    def test_black_database(self):
        #test the app's default state
        assert 'No posts found' in self.app.get('/').data

    def test_make_post(self):
        #test that you can make a post
        page = self.app.post('/make', data = {'title':'Test title', 'content':'Test content'}, follow_redirects=True)
        assert 'No posts found' not in page.data
        assert 'Test title' in page.data
        assert 'Test content' in page.data

    def test_no_title(self):
        #make sure you can't make a post without a title
        page = self.app.post('/make', data = {'title':'', 'content':'whatever'},follow_redirects=True)
        assert 'No posts found' in page.data
        assert 'Your post has no title' in page.data
        assert 'whatever' not in page.data

if __name__ == '__main__':
    unittest.main()
