# generic-flask-api
A generic API built using Flask, Redis, MySQL, Gunicorn, and NGINX.

## Goal
To, as a learning experience, create an API that I can easily spin up with the minimal requirements I feel I will frequently need, and to design the controllers (API endpoint code) in such a way that I only need to add/remove/modify the database models code to add/remove/modify API endpoints.

# Setup
Steps to start running this API...

## Initial Setup
1. Clone the repo
    ```
    git clone https://github.com/wafer-bw/generic-flask-api.git
    ```
2. Enter the repo directory
    ```
    cd generic-flask-api
    ```
3. Setup a virtual environment
    ```
    python3 -m virtualenv env
    ```
4. Activate the virtual environment
    ```
    . env/bin/activate
    ```
5. Install requirements/dependencies
    ```
    pip install -r api/requirements.txt
    ```

## Devlopment Environment
Run API in a dev environment with Flask's debug mode features
1. Configure database name, username, and password by updating the below environment variables in [/api/environments/dev.env](/api/environments/dev.env).
    * `DB_NAME`
    * `DB_USER`
    * `MYSQL_ROOT_PASSWORD`
2. Get the MySQL and Redis docker containers going.
    ```
    docker-compose -f docker-compose-dev.yml up --build -d
    ```
3. Enter API app directory.
    ```
    cd api
    ```
4. Run API app.
    ```
    python run_app_dev.py
    ```
5. View usage help.
    ```
    python run_app_dev.py -h
    ```

## Production Environment
Run API in a production environment setting using `NGINX` and `Gunicorn`.
1. Configure database name, username, and password by updating the below environment variables in [/api/environments/prod.env](/api/environments/prod.env).
    * `DB_NAME`
    * `DB_USER`
    * `MYSQL_ROOT_PASSWORD`
2. Run API - Flask APP (Gunicorn), Redis, MySQL, and NGINX.
    ```
    docker-compose up --build -d
    ```

## ARM (Raspberry Pi) Development Environment 
Run API in a dev environment with Flask's debug mode features on an ARM device like a Raspberry Pi.
1. Configure database name, username, and password by updating the below environment variables in [/api/environments/dev.env](/api/environments/dev.env).
    * `DB_NAME`
    * `DB_USER`
    * `MYSQL_ROOT_PASSWORD`
2. Get the MySQL and Redis docker containers going.
    ```
    docker-compose -f docker-compose-arm-dev.yml up --build -d
    ```
3. Enter API app directory.
    ```
    cd api
    ```
4. Run API app.
    ```
    python run_app_dev.py
    ```
5. View usage help.
    ```
    python run_app_dev.py -h
    ```

## ARM (Raspberry Pi) Production Environment
Run API in a production environment setting using `nginx` and `gunicorn` on an ARM device like a Raspberry Pi.
1. Configure database name, username, and password by updating the below environment variables in [/api/environments/prod.env](/api/environments/prod.env).
    * `DB_NAME`
    * `DB_USER`
    * `MYSQL_ROOT_PASSWORD`
2. Run API - Flask APP (Gunicorn), Redis, MySQL, and NGINX.
    ```
    docker-compose -f docker-compose-arm-prod.yml up --build -d
    ```

# Interacting with the API
Once the app is up and running, try going through these examples. The examples are given assuming you are running the API on port 8000 (Development Environment Defaults).

1. Check that things are working at http://localhost:8000. You should see something like this:
    ```
    {"http_code":200,"msg":"Hello World!","pagination":{},"results":[],"success":true}
    ```
2. Create a couple fruits. Run this a second time to see what happens when you try to create something that already exists.
    ```
    curl --request POST -H "Content-Type: application/json" -d '{"name":"Bananas"}' "http://localhost:8000/fruits"
    curl --request POST -H "Content-Type: application/json" -d '{"name":"Blueberry"}' "http://localhost:8000/fruits"
    ```
2. Query the fruits by ID. These pages are cached as per the `CACHE_DEFAULT_TIMEOUT` environment variable defined in either [/api/environments/dev.env](/api/environments/dev.env) or [/api/environments/prod.env](/api/environments/prod.env).
    * http://localhost:8000/fruits/1
    * http://localhost:8000/fruits/2
    * http://localhost:8000/fruits/3 (Unless you created more than two, this will respond with a 404 message stating the fruit doesn't exist)
3. View all existing fruits (paginated and cached per query params):
    * http://localhost:8000/fruits
    * http://localhost:8000/fruits?per_page=1
    * http://localhost:8000/fruits?per_page=1&page=2
4. Update a fruit by id:
    * Check the fruit by id here http://localhost:8000/fruits/1, this result will now be cached.
    * Update the fruit.
        ```
        curl --request PUT -H "Content-Type: application/json" -d '{"name":"Banana"}' http://localhost:8000/fruits/1
        ```
    * See that it's still cached here http://localhost:8000/fruits/1
    * After the default cache expiry time (`CACHE_DEFAULT_TIMEOUT`) has passed, check back at http://localhost:8080/fruits/1 - it will be updated!
6. Delete a fruit by id:
    ```
    curl --request DELETE http://localhost:8000/fruits/1
    ```
7. This API also has a users model as an example. You can create a user with:
    ```
    curl --request POST -H "Content-Type: application/json" -d '{"email":"someemail@gmail.com", "password": "somepassword"}' "http://localhost:8000/users"
    ```

# Generic Models
An example of how the models in this API are generic using the Development Environment...

1. Copy the fruits model, creating a veggies model:
    ```
    cp api/app/models/fruits.py api/app/models/veggies.py
    ```
2. Edit [api/app/models/veggies.py](api/app/models/veggies.py)
    * Modify the line `class Fruits(Model):` to `class Veggies(Model):`
3. Edit [api/app/models/\_\_init\_\_.py](api/app/models/__init__.py)
    * Add `from app.models.veggies import Veggies` to the imports.
    * Add `"veggies": Veggies` to the `models` dictionary.
4. Create a veggie:
    ```
    curl --request POST -H "Content-Type: application/json" -d '{"name":"Potato"}' "http://localhost:8000/veggies"
    ```

# Backup & Restore DB
Steps to get a backup mysqldump `.sql` file and apply it to a running mysql database, thanks to `spalladino`'s suggestion [here](https://gist.github.com/spalladino/6d981f7b33f6e0afe6bb).
1. You can obtain the `mysql_container_id` mentioned in the following steps using `docker ps`
2. Get a mysqldump backup `.sql` file by using:
    ```
    docker exec {mysql_container_id} /usr/bin/mysqldump -u{user} -p{password} {database_name} > backup.sql
    ```
3. You may need to remove a line at the top of your `backup.sql` file warning you about CLI password usage, it will look like this:
    >mysqldump: [Warning] Using a password on the command line interface can be insecure.
4. To restore / apply the dump to a database, use:
    ```
    cat backup.sql | docker exec -i {mysql_container_id} /usr/bin/mysql -u{user} -p{password} {database_name}
    ```

# Migrate DB
Steps to use [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) to apply schema changes.
1. Make sure you're in the repo directory then...
    ```
    cd api
    ```
2. Set the FLASK_APP environment variable for Flask-Migrate to use like:
    ```
    export FLASK_APP='app.factory:create_app("Dev")'
    ```
3. Initialize in case it isn't initialized already with:
    ```
    flask db init
    ```
4. Generate migrations with
    ```
    flask db migrate
    ```
    * If you get an error like: `Error: Can't locate revision identified by` then you'll need to run this while selecting your DB in the mysql CLI
        ```
        delete from alembic_version;
        ```
5. As per the Flask-Migrate documentation:
    >The migration script needs to be reviewed and edited, as Alembic currently does not detect every change you make to your models. In particular, Alembic is currently unable to detect table name changes, column name changes, or anonymously named constraints.
6. Apply the migration using:
    ```
    flask db upgrade
    ```

# Resources
* [Docker Docs](https://docs.docker.com/)
* [Flask Docs](http://flask.pocoo.org/docs/1.0/)
* [Flask Extensions](/app/utilities/extensions/db.py)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/)
* [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/en/latest/)
* [Gunicorn Docs](https://gunicorn.org/#docs)
* MySQL
    * [MySQL DockerHub](https://hub.docker.com/_/mysql)
    * [ARM MySQL DockerHub](https://hub.docker.com/r/arm32v7/redis)
* Redis
    * [Redis DockerHub](https://hub.docker.com/_/redis)
    * [ARM Redis Dockerhub](https://hub.docker.com/r/hypriot/rpi-mysql/)
* NGINX
    * [NGINX DockerHub](https://hub.docker.com/_/nginx)
    * [NGINX Config](https://www.nginx.com/resources/wiki/start/topics/examples/full/)
