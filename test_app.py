# ---------------------------------------------------------
# Imports
# ---------------------------------------------------------

import json
import os
import unittest
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie
from config import bearer_tokens
from datetime import date

# Create dict with Authorization key and Bearer token as values. 
# Later used by test classes as Header

casting_assistant_auth_header = {
    'Authorization': bearer_tokens['casting_assistant']
}

casting_director_auth_header = {
    'Authorization': bearer_tokens['casting_director']
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens['executive_producer']
}


# ---------------------------------------------------------
# Tests
# ---------------------------------------------------------


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency's test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "henana"
        self.database_path = "postgresql://{}/{}".format('postgres:wythenshawe0513@localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_new_actor(self):
        """Test POST new actor."""

        json_create_actor = {
            'name': "New actor name worked.",
            'age': "New actor age worked.",
            'gender': "New actor gender worked."
        } 

        res = self.client().post('/add-actor', data = json.dumps(json_create_actor), headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], json_create_actor['name'])
        self.assertEqual(data['actor']['age'], json_create_actor['age'])
        self.assertEqual(data['actor']['gender'], json_create_actor['gender'])
    
    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name': "New actor name worked.",
            'age': "New actor age worked.",
            'gender': "New actor gender worked."
        } 

        res = self.client().post('/add-actor', data = json.dumps(json_create_actor))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header not found.')

    #def test_error_422_create_new_actor(self):
    #    """Test Error POST new actor."""
    #
    #    json_create_actor_without_name_gender = {
    #        'age': "New actor age worked."
    #    } 
    #
    #    res = self.client().post('/add-actor', data = json.dumps(json_create_actor_without_name_gender),
    #                            headers = casting_director_auth_header)
    #    data = json.loads(res.data)
    #
    #    self.assertEqual(res.status_code, 422)
    #    self.assertFalse(data['success'])
    #    self.assertEqual(data['message'], 'Request could not be processed.')

#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#

    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        """Test GET all actors w/o Authorization."""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header not found.')

    def test_error_404_get_actors(self):
        """Test Error GET all actors."""
        res = self.client().get('/actors/1125125125', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'no actors found in database.')

#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#

    def test_edit_actor(self):
        """Test PATCH existing actors"""
        
        actor = Actor(name="Anne Hathaway", age="50", gender="female")
        actor.insert()
        actor_id = actor.id
        
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        
        res = self.client().patch(
           f'/actors/{actor_id}',
           data = json.dums(json_edit_actor_with_new_age),
           headers = casting_director_auth_header
           )
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], actor.name)
        self.assertEqual(data['actor']['age'],  json_edit_actor_with_new_age['age'])
        self.assertEqual(data['actor']['gender'], actor.gender)

        actor_updated = Actor.query.get(data['actor']['id'])
        self.assertEqual(actor_updated.id, actor.id)

    #def test_error_400_edit_actor(self):
    #        """Test PATCH with non json body"""
    #
    #        res = self.client().patch('/actors/123412', headers = casting_director_auth_header)
    #        data = json.loads(res.data)
    #
    #        self.assertEqual(res.status_code, 400)
    #        self.assertFalse(data['success'])
    #        self.assertEqual(data['message'] , 'request does not contain a valid JSON body.')

    def test_error_404_edit_actor(self):
        """Test PATCH with non valid id"""
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/123412', json = json_edit_actor_with_new_age, headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Item not found.')

#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header not found.')

    def test_error_403_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Request is forbidden.')

    def test_delete_actor(self):
        """Test DELETE existing actor"""
        res = self.client().delete('/actors/1', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_actor(self):
        """Test DELETE non existing actor"""
        res = self.client().delete('/actors/15125', headers = casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Item not found.')

#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#

    def test_create_new_movie(self):
        """Test POST new movie."""

        json_create_movie = {
            'title' : 'Crisso Movie',
            'release_date' : date.today()
        } 

        res = self.client().post('/add-movie', data = json.dumps(json_create_movie)
                                 , headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], json_create_movie['title'])
        self.assertEqual(data['movie']['release'], json_create_movie['release'])

        movie_added = Movie.query.get(data['movie']['id'])
        self.assertTrue(movie_added)

    def test_error_422_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie = {
            'release_date' : date.today()
        } 

        res = self.client().post('/add-movie', data = json.dumps(json_create_movie)
                                 , headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#

    def test_get_all_movies(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        """Test GET all movies w/o Authorization."""
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header not found.')

    def test_error_404_get_movies(self):
        """Test Error GET all movies."""
        res = self.client().get('/movies/1125125125', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Item not found.')

#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        
        movie = Movie(title="Invisible Man", release="March 20, 1998")
        movie.insert()
        movie_id= movie.id

        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch(
            f'/movies/{movie_id}',
            data = json.dumps(json_edit_movie),
            headers = executive_producer_auth_header
            )
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], json_edit_movie['release'])

        movie_updated = Movie.query.get(data['movie']['id'])
        self.assertEqual(movie_updated.id, movie.id)

        """Test PATCH with non valid id json body"""
    #def test_error_400_edit_movie(self):
    #    res = self.client().patch('/movies/1', headers = executive_producer_auth_header)
    #    data = json.loads(res.data)
    #
    #    self.assertEqual(res.status_code, 400)
    #    self.assertFalse(data['success'])
    #    self.assertEqual(data['message'] , 'request does not contain a valid JSON body.')

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/123412',
                                  data = json.dums(json_edit_movie),
                                  headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Item not found.')

#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_movie(self):
        """Test DELETE existing movie w/o Authorization"""
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Authorization header not found.')

    def test_error_403_delete_movie(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Request is forbidden.')

    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1', headers = executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], '1')

    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/151251', headers = executive_producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Item not found.')

# Make the tests conveniently executable.
# From app directory, run 'python test_app.py' to start tests
if __name__ == "__main__":
    unittest.main()


