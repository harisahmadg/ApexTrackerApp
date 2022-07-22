FROM fedora:latest

WORKDIR /apex-tracker-app

COPY requirements.txt .

# regular python 3.10 works but slim doesnt have build essentials it seems like
# RUN apt update && sudo apt install build-essential
RUN dnf install gcc-c++ -y
RUN dnf install python3-devel -y
RUN dnf install -y python3.10 python3-pip
RUN pip3 install -r requirements.txt

RUN dnf autoremove

COPY .env .
COPY README.md .
COPY ./data ./data
COPY ./ApexTracker ./ApexTracker

CMD ["python3", "-m", "ApexTracker"]