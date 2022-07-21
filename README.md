### How to set it up
pip install "hikari[speedups]" uvloop apscheduler aiosqlite aiofiles psutil 
- had problems with uvloop got around it by doing
    - sudo apt update && sudo apt install build-essential
- since im on WSL i can install uvloop but Ubuntu didnt have basic system tools installed

### Virtual Environment Setup
VENV
python3.10 -m venv .venv
then to run it go to folder where activate file is
source .venv/bin/activate

### Setup
pip install requirements.txt
DotEnv is a lightweight npm package that automatically loads 
environment variables from a . env file into the process

### Server
REDIS SERVER
sudo apt-get install redis-server
type redis-server in cmd ubuntu to get the server running

### Apex Legends API
API
https://portal.apexlegendsapi.com/
key = int(os.environ["API_KEY_ID"])