# AvanzaTech Blog 💻️
AvanzaTech Blog is a blogging platform built with Django in the backend, utilizing a RESTful architecture. The backend offers services such as user authentication, permission management for resource access, and CRUD operations for blog posts. Additionally, users can create, read, and delete likes and comments associated with the posts.
___
### Table of Contents 🗒️
1. [Setup Environment](#setup)
2. [Admin Panel](#admin)
3. [Log In](#login)
4. [Endpoints](#endpoints)
5. [Create a Blog Post](#create-post)
6. [Edit a Blog Post](#edit-post)
7. [List Blog Posts](#list-post)
8. [Retrieve a Blog Post](#retrieve-post)
9. [Delete a Blog Post](#delete-post)
10. [Create a Like for a Blog Post](#create-like)
11. [List Likes for a Blog Post](#list-like)
12. [Delete a Like from a Blog Post](#delete-like)
13. [Create a Comment for a Blog Post](#create-comment)
14. [List Comments for a Blog Post](#list-comment)
15. [Delete a Comment from a Blog Post](#delete-comment)
16. [Database Design](#db)
17. [Edit Permissions](#edit-permissions)
18. [Read Permissions](#read-permissions)
___
## Setup Environment 🛠️ <a name="setup"></a>
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
___
## Admin Panel 🚔 <a name="admin"></a>
Once you have created a superuser in the 8th step in the last section, you can now log in with your email and password. The admin panel allows you to create, edit, list, and delete entities for every application related to the project. The related applications include:
- User
    - Blogger
    - Admin
- Post
- Team
- Comment
- Like

Additionally, from this panel, an admin user can be created by activating the `is_staff` attribute in the User-panel creation. To log in into the Django admin panel site you need to access
```text
http://localhost:8000/admin/
```
**Note**: Just superusers have access to admin panel. When logged in as a superuser in the admin panel, you also gain admin access to the Blog post API, granting you unrestricted access to all resources. Admin users have special permissions but they don't have access to admin panel
___
## Log in ✅ <a name="login"></a>
From the admin panel, you can create a blogger user and log in with their credentials at:
```text
http://localhost:8000/user/login/
```
Once you log in as a `blogger`, the admin session will be closed automatically. If you want manually logout, you can access to this endpoint:
```text
http://localhost:8000/user/logout/
```
___
## Endpoints 🚪 <a name="endpoints"></a> 
The following endpoints allow to interact with the resources through the RESTful API
### Create a Blog Post 📝 <a name="create-post"></a>
- To create a blog post, you need to be authenticated and send an `HTTP POST` request to this endpoint:
```text
http://localhost:8000/blog/
```
- The payload must follow this template
```json
{
    "title": "post title",
    "content": "post content",
    "read_permission": "public"
}
```
- `title` field must not be empty
- For the `read_permission` field, you can set it to one of the following options. Any other option will return in a bad request response
    - `public`
    - `authenticated`
    - `team`
    - `author`
- The author of the post will be automatically set to the logged in user
- The response of the RESTful API looks like this:
```json
{
    "id": 1,
    "title": "post title",
    "content": "post content",
    "user": 1,
    "read_permission": "public",
    "created_at": "2024-01-30T17:07:53.962903Z"
}
```
- The create a post operation returns an `HTTP 201` status code
___
### Edit a Blog Post ✏️ <a name="edit-post"></a>
- To edit a blog post, you need to be authenticated as the owner of the post or as an admin user and send an `HTTP PUT` request to this endpoint:
```text
http://localhost:8000/blog/<int:pk>
```
- Replace `<int:pk>` with the integer that identifies the post
- The payload must follow this template
```json
{
    "title": "post title",
    "content": "post content",
    "read_permission": "public"
}
```
- Partial updates with `HTTP PATCH` are also supported by the API
- `title` field must not be empty
- For the `read_permission` field, you can set it to one of the following options. Any other option will return in a bad request response
    - `public`
    - `authenticated`
    - `team`
    - `author`
- The edit a post operation returns an `HTTP 200` status code
___
### List Blog Posts 📋 <a name="list-post"></a>
- To retrieve a list of blog posts,  send an `HTTP GET` request to this endpoint:
```text
http://localhost:8000/blog/
```
- If you are not authenticated, you will only see `public` posts
- If you are authenticated, you will see:
    - `authenticated` posts.
    - Posts of your own team with `read_permission` set as `team`.
    - Your own posts marked as author
- The response of the API looks like this:
```json
{
    "count": 23,
    "next": "http://localhost:8000/blog/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Post Title",
            "content": "This is the title of the post",
            "user": 5,
            "read_permission": "authenticated",
            "created_at": "2024-01-30T17:07:53.962903Z"
        },
        {
            "id": 2,
            "title": "Public POst",
            "content": "This is the title of a public post",
            "user": 5,
            "read_permission": "public",
            "created_at": "2024-01-30T17:07:45.379470Z"
        },
        "..."
    ]
}
```
- `count`: Returns the total number of available posts
- `next` and `previous`: Provide links to the next and previous pages of results, respectively. The API returns `10` results per page by default. You can adjust the page size up to `50` results with the query parameter `page_size`, like this
```text
http://localhost:8000/blog/?page_size=23
```
- The order of the results is by the most recent post by default
- The list posts operation returns an `HTTP 200` status code
___
### Retrieve a Blog Post 🔍 <a name="retrieve-post"></a>
- To retrieve a single blog post, send an `HTTP GET` request to this endpoint:
```text
http://localhost:8000/blog/<int:pk>/
```
- Replace `<int:pk>` with the integer that identifies the post
- If you are not authenticated, you will only retrieve `public` post
- If you are authenticated, you can retrieve:
    - `authenticated` posts.
    - Posts of your own team with `read_permission` set as `team`.
    - Your own posts, whether marked as `author` or not.
- The response of the API looks like this:
```json
{
    "id": 1,
    "title": "Post title",
    "content": "Post content",
    "read_permission": "public",
    "user": 1,
    "last_modified": "2024-01-23T20:59:24.830718Z"
}
```
- To retrieve a post, you don't need to be the owner or an admin user, but you need to have view access to that post
- Retrieve a post successfully return an `HTTP 200` status code
___
### Delete a Blog Post 🗑️ <a name="delete-post"></a>
- To delete a blog post, you need to be authenticated as the owner of the post or as an admin user and send an `HTTP DELETE` request to this endpoint:
```text
http://localhost:8000/blog/<int:pk>/
```
- Replace `<int:pk>` with the integer that identifies the post
- No payload is required for this operation
- Deleting a post will will also delete associated likes and comments
- The delete post operation returns an `HTTP 204` status code
___
### Create a Like for a Blog Post ❤️ <a name="create-like"></a>
- To create a like in a blog post, you need to be authenticated and send an `HTTP POST` request to this endpoint:
```text
http://localhost:8000/like/
```
- The payload must follow this template
```json
{
    "post": 1,
    "user": 1,
}
```
- `post` represents the `id` of the post in the database
- `user` represents the `id` of the user in the database
- The `user` in the payload must be the same as the logged-in user
- Invalid `post` or `user` will return an `HTTP 400` status code
- To create a like, you must have read permissions on the post
- The response of the RESTful API looks like this:
```json
{
    "id": 1,
    "post": "post title",
    "user": 1,
    "is_active": "true"
}
```
- You can not create a like that already exists as active
- However, you can, in this endpoint, reactivate a like that was previously deactivated (deleted)
- The create a like operation returns an `HTTP 201` status code
___
### List Likes for a Blog Post 👍 <a name="list-like"></a>
- To retrieve a list of likes,  send an `HTTP GET` request to this endpoint:
```text
http://localhost:8000/like/
```
- If you are not authenticated, you will only see `public` likes
- If you are authenticated, you will see:
    - `authenticated` likes.
    - Likes associated with a `post` of your own team with `read_permission` set as `team`.
    - Your likes associated with your own posts marked as `author`.
- Only `active` likes are listed
- The response of the API looks like this:
```json
{
    "count": 4,
    "next": "http://localhost:8000/like/?page=2",
    "previous": null,
    "results": [
        {
            "id": 4,
            "user": 7,
            "post": 1,
            "is_active": true
        },
        {
            "id": 3,
            "user": 6,
            "post": 3,
            "is_active": true
        },
        "..."
    ]
}
```
- `count`: Returns the total number of available likes
- `next` and `previous`: Provide links to the next and previous pages of results, respectively. The API returns `20` results per page by default. You can adjust the page size up to `50` results with the query parameter `page_size`, like this
```text
http://localhost:8000/like/?page_size=23
```
- The order of the results is by the most recent like by default
- You can filter likes by `post` or `user` using query parameters, just like this:
```text
http://localhost:8000/like/?post=3&user=5
```
- The list likes operation returns an `HTTP 200` status code
___
### Delete a Like from a Blog Post ❌ <a name="delete-like"></a>
- To delete a like in a blog post, you need to be authenticated as the owner of the like or as an admin user and send an `HTTP DELETE` request to this endpoint:
```text
http://localhost:8000/like/<int:user>/<int:post>/
```
- Replace `<int:post>` with the integer that identifies the post with the like
- Replace `<int:user>` with the integer that identifies the owner of the like
- The `user` in the URL must be the same as the logged-in user or an admin user
- No payload is required for this operation
- The delete like operation returns an `HTTP 204` status code
___
### Create a Comment for a Blog Post 💬 <a name="create-comment"></a>
- To create a comment in a blog post, you need to be authenticated and send an `HTTP POST` request to this endpoint:
```text
http://localhost:8000/comment/
```
- The payload must follow this template
```json
{
    "content": "content of the comment",
    "post": 1,
    "user": 1,
}
```
- `content` represents the body of the comment
- `post` represents the `id` of the post in the database
- `user` represents the `id` of the user in the database
- The `user` in the payload must be the same as the logged-in user
- Invalid `post` or `user` will return an `HTTP 400` status code
- To create a comment, you must have read permissions on the post
- The response of the RESTful API looks comment this:
```json
{
    "id": 1,
    "content": "content of the comment",
    "user": 1,
    "username": "user's username",
    "post": 1,
    "is_active": "true",
    "created_at": "2024-01-30T17:07:53.962903Z" 
}
```
- You can create several comments in a single `post`
- The create a comment operation returns an `HTTP 201` status code
___
### List Comments for a Blog Post 💬 <a name="list-comment"></a>
- To retrieve a list of comments,  send an `HTTP GET` request to this endpoint:
```text
http://localhost:8000/comment/
```
- If you are not authenticated, you will only see `public` comments
- If you are authenticated, you will see:
    - `authenticated` comments.
    - Comments associated with a `post` of your own team with `read_permission` set as `team`.
    - Your comments associated with your own posts marked as `author`.
- Only `active` comments are listed
- The response of the API looks comment this:
```json
{
    "count": 23,
    "next": "http://localhost:8000/comment/?page=2",
    "previous": null,
    "results": [
        {
            "id": 2,
            "content": "comment number one",
            "user": 7,
            "username": "mariovelandiac",
            "post": 3,
            "is_active": true,
            "created_at": "2024-01-30T00:41:59.033330Z"
        },
        {
            "id": 3,
            "content": "comment number two",
            "user": 6,
            "username": "anotheruser23",
            "post": 3,
            "is_active": true,
            "created_at": "2024-01-30T00:42:35.033330Z"
        }
        "..."
    ]
}
```
- `count`: Returns the total number of available comments
- `next` and `previous`: Provide links to the next and previous pages of results, respectively. The API returns `10` results per page by default. You can adjust the page size up to `50` results with the query parameter `page_size`, comment this
```text
http://localhost:8000/comment/?page_size=23
```
- The order of the results is by the most recent comment by default
- You can filter comments by `post` or `user` using query parameters, just comment this:
```text
http://localhost:8000/comment/?post=3&user=5
```
- The list comments operation returns an `HTTP 200` status code
___
### Delete a Comment from a Blog Post ❌ <a name="delete-comment"></a>
- To delete a comment in a blog post, you need to be authenticated as the owner of the comment or as an admin user and send an `HTTP DELETE` request to this endpoint:
```text
http://localhost:8000/comment/<int:pk>/
```
- Replace `<int:pk>` with the integer that identifies the comment
- No payload is required for this operation
- The delete comment operation returns an `HTTP 204` status code
___
## Read Permissions 🔍 <a name="read-permissions"></a>
To access a resource, `Avanzatech Blog` RESTful API implements the following read permissions:
    **public**: Anyone can access the post.
    **authenticated**: Any authenticated user can access the post.
    **team**: Any user on the same team as the post author can access the post.
    **author**: Only the author can access the post.
### Made by
[<img src="https://avatars.githubusercontent.com/u/103077180?v=4" width=115><br><sub>Mario Velandia Ciendúa</sub>]
