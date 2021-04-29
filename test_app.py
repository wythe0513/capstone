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
        self.database_path = "postgresql://{}/{}".format('postgres:XXXXX@localhost:5432',
                                                         self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_should_return_all_actors(self):
        # Insert dummy actor into database.
        actor = Actor(name="taro", age="13", gender="male")
        actor.insert()

        res = self.client().get('/actors', headers = casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_get_actors_dont_accept_post_request(self):
        res = self.client().post('/actors')
        self.assertEqual(res.status_code, 405)

    def test_should_return_all_movies(self):
        # Insert dummy actor into database.
        movie = Movie(title="kimetu", release="June 30, 2006")
        movie.insert()

        res = self.client().get('/movies', headers = casting_assistant_auth_header )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_get_movies_dont_accept_post_request(self):
        res = self.client().post('/movies')
        self.assertEqual(res.status_code, 405)

    def test_create_new_actor(self):
        """Test POST new actor."""

        json_create_actor = {
            'name': "New actor name",
            'age': "New actor age",
            'gender': "New actor gender"
        } 

        res = self.client().post('/add-actor',
                                 json=json_create_actor,
                                 headers = casting_director_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor']['name'], json_create_actor['name'])
        self.assertEqual(data['actor']['age'], json_create_actor['age'])
        self.assertEqual(data['actor']['gender'], json_create_actor['gender'])

        actor_added = Actor.query.get(data['actor']['id'])
        self.assertTrue(actor_added)
    
    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name': "age missing",
            'gender': "ng"            
            } 

        res = self.client().post('/add-actor',
                                 json = json_create_actor,
                                 headers = executive_producer_auth_header
                                 )

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'],422)
        self.assertFalse(data['success'])

    
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

   
#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#

    def test_edit_actor(self):
        """Test PATCH existing actors"""
        
        actor = Actor(name="kguyahime", age="20", gender="female")
        actor.insert()
        actor_id = actor.id
        
        json_edit_actor_with_new_age = {
            'age' : '30'
        } 
        
        res = self.client().patch(
           f'/actors/{actor_id}',
           json = json_edit_actor_with_new_age,
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

    
    def test_error_404_edit_actor(self):
        """Test PATCH with non valid id"""
        json_edit_actor_with_new_age = {
            'age' : 30
        } 
        res = self.client().patch('/actors/123412',
                                  json = json_edit_actor_with_new_age,
                                  headers = casting_director_auth_header
                                  )
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

        actor = Actor(name="unchi", age="5", gender="female")
        actor.insert()
        #actor_id = actor.id

        res = self.client().delete(f'/actors/{actor.id}',
                                   headers = casting_director_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['actor_id'], actor.id)

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
            'release' : "Fri, 20 Mar 1998 00:00:00 GMT"
        } 

        res = self.client().post('/add-movie', json = json_create_movie
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
            'release_date' : "June 30, 2006"
        } 

        res = self.client().post('/add-movie', json = json_create_movie
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

   
#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        
        movie = Movie(title="Invisible Man", release="March 20, 1998")
        movie.insert()
        movie_id= movie.id

        json_edit_movie = {
            'release' : "Tue, 30 Jun 2009 00:00:00 GMT"
        } 
        res = self.client().patch(
            f'/movies/{movie_id}',
            json = json_edit_movie,
            headers = executive_producer_auth_header
            )
        
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['movie']['title'], movie.title)
        self.assertEqual(data['movie']['release'], json_edit_movie['release'])

        movie_updated = Movie.query.get(data['movie']['id'])
        self.assertEqual(movie_updated.id, movie.id)

    
    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/123412',
                                  json = json_edit_movie,
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

        movie = Movie(title="Invisible Man", release="March 20, 1998")
        movie.insert()
       # movie_id= movie.id


        res = self.client().delete(f'/movies/{movie.id}',
                                   headers = executive_producer_auth_header
                                   )
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == movie.id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        #self.assertEqual(data['movie.id'], movie.id)

    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/151251', headers = executive_producer_auth_header) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'Item not found.')


if __name__ == "__main__":
    unittest.main()


