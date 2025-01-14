A Blog REST API which uses flask and mongodb under the hood

This project is a Flask-based RESTful API built with the MongoEngine ORM, serving as the backend for a blog. It provides endpoints for managing blog posts, along with user authentication and CRUD operations for articles.


## Features

- **JWT Authentication**  
  Secure user authentication using JSON Web Tokens (JWT).

- **CRUD Operations for Articles**  
  Supports Creating, Reading, Updating, and Deleting articles.

- **User Management**  
  Allows user signup and login functionality.

- **SQLite Database**  
  Utilizes SQLite as the database backend for lightweight and easy data storage.


## API Endpoints

### Articles

| Method | Route                  | Auth Required | Description                 |
|--------|------------------------|---------------|-----------------------------|
| GET    | `/articles/:id`        | Yes           | Get a single article by ID  |
| GET    | `/articles`            | Yes           | Get all articles            |
| POST   | `/articles`            | Yes           | Create a new article        |
| DELETE | `/articles/:id`        | Yes           | Delete an article by ID     |
| PUT    | `/articles/:id`        | Yes           | Update an article by ID     |

### Users

| Method | Route       | Description                     |
|--------|-------------|---------------------------------|
| POST   | `/register` | Register a new user             |
| POST   | `/login`    | Authenticate user and get token |


## Structure

```plaintext
.
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
├── run.py                        # Main entry point for running the Flask application
├── config.py                     # Configuration file for the application
├── app/                          # Core application directory
│   ├── __init__.py               
│   ├── db.py                     # MongoDB connection setup
│   ├── errors.py                 # Custom error handlers
│   ├── utils.py                  # Utility functions
│   ├── models/                   # Database models directory
│   │   ├── __init__.py           
│   │   ├── article.py            # Article model
│   │   └── user.py               # User model
│   ├── routes/                   # API routes directory
│   │   ├── __init__.py           
│   │   ├── articles.py           # Routes for article-related endpoints
│   │   ├── users.py              # Routes for user-related endpoints
│   │   ├── docs/                 # Swagger documentation for API endpoints
│   │   │   ├── delete_article.yml
│   │   │   ├── get_article.yml
│   │   │   ├── get_articles.yml
│   │   │   ├── login.yml
│   │   │   ├── post_article.yml
│   │   │   ├── register.yml
│   │   │   └── update_article.yml
│   └── tests/                    # Unit tests directory
│       ├── __init__.py           
│       └── test_models.py        # Unit tests for database models
└── http_tests/                   # HTTP request examples for testing API
    ├── delete_article.http
    ├── get_article.http
    ├── get_articles.http
    ├── get_users.http
    ├── home.http
    ├── login.http
    ├── post_article.http
    ├── register.http
    └── update_article.http


```


TODO:
- [X] Add routes for creating, updating and deleting posts
- [X] Add pagination for viewing posts
- [X] Add documentation
- [X] Add optional image url for user profiles
- [X] Add tests
