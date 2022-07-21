FROM python:3.10

WORKDIR /apex-tracker-app

COPY requirements.txt .

# regular python 3.10 works but slim doesnt have build essentials it seems like
# RUN apt update && sudo apt install build-essential
RUN pip install -r requirements.txt

COPY .env .
COPY README.md .
COPY ./data ./data
COPY ./ApexTracker ./ApexTracker

CMD ["python", "-m", "ApexTracker"]