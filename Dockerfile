FROM ubuntu:18.04

RUN apt update && apt install -y gcc

# needed dependencies for dlib
RUN apt install -y build-essential cmake
RUN apt install -y libopenblas-dev liblapack-dev
RUN apt install -y libx11-dev libgtk-3-dev
RUN apt install -y python python-dev python-pip
RUN apt install -y python3 python3-dev python3-pip

# set the working directory for containers
WORKDIR .

# Installing python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all the files from the project’s root to the working directory
COPY src/ /src/
COPY model/ /model/

# Running Python Application
CMD ["python3", "/src/main.py"]
