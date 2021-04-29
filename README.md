# FSND Capstone Project
## content
This is a final project of Udacity FSND that covers following items.
1. Relational Database Architecture
2. Modeling Data Objects with SQLAlchemy
3. Internet Protocols and Communication
4. Developing a Flask API
5. Authentication with Auth0 (RBAC)
6. Testing Flask Applications
7. Deploying Applications to Heroku

## Database
Two tables are created;
1. `actors` table(name, age and gender)
2. `movies`table(name and release) 

## Authentification
Three roles and permissions are set in Auth0;

**Casting Assistant :** <br>
- view actors and movies(GET '/actors', GET '/movies')<br>

**Casting Director :** <br>
- view actors and movies(GET '/actors', GET '/movies')<br>
- add or delete an actor(POST '/add-actor', DELETE '/actors/\<int:actor_id>')<br>
- modify actors or movies(PATCH '/acotrs/\<int:movie_id>, PATCH '/movies/\<int:movie_id>) <br>

**Executive Producer :**<br>
- view actors and movies(GET '/actors', GET '/movies')<br>
- add or delete an actor(POST '/add-actor', DELETE '/actors/\<int:actor_id>')<br>
- modify actors or movies(PATCH '/acotrs/\<int:movie_id>, PATCH '/movies/\<int:movie_id>) <br>
- add or delete a movie(POST '/add-movie', DELETE '/movies/\<int:movie_id>')<br> 


## Run locally
It works under windows10 python 3.7.8 environment. <br>
To run the following commands;

`$ cd ./starter`<br>
`$ python -m virtualenv env`<br>
`$ .\env\Scripts\activate`<br>
`$ pip install -r requirements.txt`<br>
`$ set FLASK_APP=app.py && set FLASK_ENV=development && python app.py`<br>

## Get Auth JWT tokens for each Role

Acess [Auth0 here](https://tomascap.jp.auth0.com/authorize?audience=agency&response_type=token&client_id=53BPJctnRYyC5bBVLQhRwxZRrFTO9Wgf&redirect_uri=https://heichi.herokuapp.com/)
, JWT is availabe for each role. E-mail adress and password are as follows;<br>

In case if the above link does not work, access to the following url;<br>

https://tomascap.jp.auth0.com/authorize?audience=agency&response_type=token&client_id=53BPJctnRYyC5bBVLQhRwxZRrFTO9Wgf&redirect_uri=https://heichi.herokuapp.com/

\<< e-mail adress >><br>

**Casting Assistant :** casting_assistant@udacity.com<br>
**Casting Director :** casting_director@udacity.com<br>
**Executive Producer :** executive_producer@udacity.com<br>

\<< Password >>

Udacity!

## Running Tests

To run the unittests, first get valid JWT for each role, then run the following commands:

`$ cd ./starter`<br>
`$ python test_app.py`<br>


## Deployment to Heroku

Deployed to :

https//heichi.herokuapp.com/