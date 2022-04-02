# Seashell Anatomy

## Setup Instructions (Unix)

1. clone this repo (use ssh please!)
2. create a python virtual environment
    1. `python -m venv venv`
    2. `source venv/bin/activate`

3. Install all packages
    1. `python -m pip install -r requirements.txt`

4. Initialize the `.env` files
    1. `touch spotify_api/.env`
    2. `touch db/.env`
    3. copy spotify credentials into `spotify_api/.env`
    4. copy db credentials into `db/.env`

. Run the server
    1. `chmod +x ./run_server.sh`
    2. `./run_server.sh`
