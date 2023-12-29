
# Friender Backend

A RESTful API for a friend finding platform where you can match with people near you

Deployed on: https://friender.michaellngriffin.com/ <br>
**User:** guest <br>
**Password:** password <br>

Frontend codebase: https://github.com/michael-griffin/Friender-frontend

<br>

### Built with

- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
- ![postgresql](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)

<br>



## Local Setup

1. Navigate to base directory. Create virtual environment and activate.

  ```Shell
  python3 -m venv venv
  source venv/bin/activate
  ```

2. Install dependencies.

  ```Shell
  pip3 install -r requirements.txt
  ```

3. Create postgresQL Database and seed data
  - Create a .env file, add: `DATABASE_URL=postgresql:///warbler`
  - Run `seed.py` to create database

<br>

### Images Setup

1. Setup AWS S3 Bucket for user photos
   Friender uses S3 object storage to store and access user photos.
   Create an S3 bucket with CORS enabled.

2. Add AWS Credentials to .env
   You will need:

   - `'AWS_ACCESS_KEY_ID'`
   - `'AWS_SECRET_ACCESS_KEY'`

3. Upload user images from `/images` to your S3 bucket and ensure the file names match those used in `seed.py`.

<br>

## Running the App

Within the virtual environment, can start app with:
  ```Shell
  flask run
  ```
<br>