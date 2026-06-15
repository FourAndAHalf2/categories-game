# Categories Game

A small React + Flask app for practicing categories.\
Frontend is a Vite React app; backend is a Flask API.

## Prerequisites

- Node.js (20+)
- Python 3.13+
- pip
- (optional) Docker & Docker Compose

## Quick start

### Using Docker

1. download the code
2. run `docker-compose up` in the project directory
3. open `http://localhost:5173` in your browser

### Without Docker

1. download the code
2. install dependencies for the backend:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. install dependencies for the frontend:

   ```bash
   cd frontend
   npm install
   ```

4. run the backend:

   ```bash
   cd backend
   python app.py
   ```

5. run the frontend:

   ```bash

   cd frontend
   npm run dev
   ```

6. open `http://localhost:5173` in your browser

## used technologies

- vite
- react
- flask and flask-cors
- bootstrap
- docker

## Used data sources

- https://raw.githubusercontent.com/FinNLP/cities-list/refs/heads/master/list.txt - dataset used for cities, data originally from https://www.geonames.org/
- https://restcountries.com/ - API used for countries
- https://raw.githubusercontent.com/sroberts/wordlists/refs/heads/master/animals.txt - dataset used for list of animals
