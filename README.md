# Bookmarks API - Flask RESTful CRUD  

This project is a Flask-based REST API that allows users to manage bookmarks with basic CRUD (Create, Read, Update, Delete) operations. It uses Flask, Flask Swagger UI, Waitress, Python-Dotenv and SQLAlchemy to store and retrieve bookmark records.  

## Demo  

- API Base URL: [https://bookmarks-api-flask.onrender.com/](https://bookmarks-api-flask.onrender.com/)  
 

## Sample  

![Image](https://github.com/user-attachments/assets/60ce9982-3356-46dc-83fb-33f62acc6835)
![Image](https://github.com/user-attachments/assets/91ab989c-37ca-41d4-90e6-4ba9466fb95c)
![Image](https://github.com/user-attachments/assets/135b929a-a7ff-4e31-8a55-064765a78195)  

## Table of Contents  

- [Installation](#installation)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [Contributing](#contributing)  
- [License](#license)  

## Installation  

1. Clone this repository:  

   ```bash
   git clone https://github.com/Okkar25/Bookmarks_API_FLASK
   ```

2. Navigate into the project folder:  

   ```bash
   cd Bookmarks_API
   ```

3. Set up a virtual environment and activate it:  

   ```bash
   python -m venv .venv
   source venv/bin/activate  # On Windows use `venv/Scripts/activate`
   ```

4. Install the dependencies:  

   ```bash
   pip install -r requirements.txt
   ```

## Usage  

Run the Flask application:  

```bash
python run.py
```
```bash
py -m run
```
```bash
flask run
```

Visit `http://localhost:8000` in your browser or use Postman/ThunderClient to interact with the API.  

## API Endpoints  

 **POST** `/api/v1/auth/login` - User Log In.  
 **POST** `/api/v1/auth/logout` - User Log Out.  
 **POST** `/api/v1/auth/register` - User Registration.  
 **POST** `/api/v1/auth/token/refresh` - Refresh Token.  
- **GET** `/api/v1/auth/user` - Retrieve the User's Info.  

- **GET** `/api/v1/bookmarks` - Retrieve all bookmarks.  
- **POST** `/api/v1/bookmarks` - Create a new bookmark.  
- **GET** `/api/v1/bookmarks/<id>` - Retrieve a specific bookmark by ID.  
- **PATCH** `/api/v1/bookmarks/<id>` - Update a specific info of an existing bookmark by ID.  
- **PUT** `/api/v1/bookmarks/<id>` - Update an existing bookmark by ID.  
- **DELETE** `/api/v1/bookmarks/<id>` - Delete a bookmark by ID.  

## Contributing  

Feel free to fork this repository, submit issues, and make pull requests. Contributions are always welcome!  

## License  

This project is licensed under the MIT License.  
