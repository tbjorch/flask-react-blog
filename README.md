# flask-react-blog
Simple blog using Python Flask as backend and React as frontend

# About the project
MVC style backend split into routes, controllers and models. Models and controllers extend superclasses (BaseController and BaseModel) containing generalzed methods to keep code base DRY, which also leads to slim subclasses.

Pytest is used for testing, and the tests uses a simple custom context manager to make sure each test can run isolated and independently on the outcome of other tests. 

Github actions is used to automatically run the backend tests whenever a change is pushed to the backend directory of the repo.

The application is deployed using Docker containers, one Nginx container with static frontend files, and configured to forward api requests to a backend container.

# Keywords
- Python
- Flask
- SQLAlchemy
- Docker
- Shellscript
- JavaScript
- ReactJS
- Nginx
- Github Actions running tests on push
