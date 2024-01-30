# AvanzaTech Blog 💻️
AvanzaTech Blog is a blogging platform built with Django in the backend, utilizing a RESTful architecture. The backend offers services such as user authentication, permission management for resource access, and CRUD operations for blog posts. Additionally, users can create, read, and delete likes and comments associated with the posts.
## Setup Environment 🛠️
**1**. Clone the repository in your local environment
```sh
# Clone repository
$ git clone git@github.com:mariovelandiac/avanzatech_blog
```
**2**. Create a database in your local environment, Postgresql is recommended, however, any relational database engine could be used
```SQL
CREATE DATABASE avanzatech_blog_db;
```
**3**. Create your own ```.env``` file based on ```.envexample``` file in the repository
```sh
# Copy the .envexample file to create your own .env file
$ cp .envexample .env
```
Set the ```.env``` file with the required fields. The database's user should have permissions to create tables and insert rows in the database
```text
DB_NAME=avanzatech_blog_db
DB_USER=username
DB_PASSWORD=password
DB_HOST=host
DB_PORT=port
SECRET_KEY=secret_key
```
**4**. Start the virtual environment with ```pipenv```
```sh
# Create virtual environment
$ pipenv --python $(which python3) install
```
This project requires Python version 3.10 or 3.11. If you don't have either of these versions in your local environment, you can install it with:
```sh
# Install Python version 3.x.y
$ pipenv --python 3.x.y install
```
**5**. Start the virtual environment
```sh
# Start virtual environment
$ pipenv shell
```
**6**. Install dependencies
```sh
# Install dependencies
$ pipenv install
```
**7**. Generate the migrations in the database and apply them
```sh
# Generate migrations
$ python manage.py makemigrations
# Apply the migrations
$ python manage.py migrate
```
**8**. Create a superuser to access the admin panel. When you run this command, the prompt will ask you for an email, a password, and a username. The email and the password will be used for logging in to the site admin.
```sh
# Create Superuser
$ python manage.py createsuperuser
```
**9**. Now you can run the development server
```sh
# Run development server
$ python manage.py runserver
```
**Note**: By default, the Django development server (`runserver`) will be listening on port 8000 on localhost.
## Admin Panel 🚔
Once you have created a superuser in the 8th step in the last section, you can now log in with your email and password. The admin panel allows you to create, edit, list, and delete entities for every application related to the project. The related applications include:
- User
- Post
- Team
- Comment
- Like

Additionally, from this panel, an admin user can be created by activating the `is_staff` attribute in the User-panel creation. To log in into the Django admin panel site you need to access
```text
http://localhost:8000/admin
```
**Note**: When logged in as a superuser in the admin panel, you are also gain admin access to the Blog post API, granting you unrestricted access to all resources.
## Log in ✅
From the admin panel, you can create a non-admin user and log in with their credentials at:
```text
http://localhost:8000/user/login
```
Once you log in as a `blogger`, the admin session will be closed automatically. If you want manually logout, you can access to this endpoint:
```text
http://localhost:8000/user/logout
```
## Endpoints 🚪
### Create a Blog Post 📝
### Edit a Blog Post ✏️
### List Blog Posts 📋
### Retrieve a Blog Post 🔍
### Delete a Blog Post 🗑️
### Create a Like for a Blog Post ❤️
### List Likes for a Blog Post 👍
```text
http://localhost:8000/like/?post=3&user=5
```
### Delete a Like from a Blog Post ❌
### Create a Comment for a Blog Post 💬
### List Comments for a Blog Post 💬
### Delete a Comment from a Blog Post ❌
## Database Design 🗃️
## Edit Permissions ✏️
## Read Permissions 🔍
