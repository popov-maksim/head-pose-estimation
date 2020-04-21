FROM ubuntu:18.04

RUN apt update && apt install -y gcc unzip curl

# Dependencies for opencv
RUN apt install -y \
    gfortran \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libavcodec-dev \
    libavformat-dev \
    libboost-all-dev \
    libjpeg-dev \
    libswscale-dev \
    pkg-config \
    python-protobuf \
    python3-protobuf \
    software-properties-common

# Needed dependencies for dlib
RUN apt install -y build-essential cmake
RUN apt install -y libopenblas-dev liblapack-dev
RUN apt install -y libx11-dev libgtk-3-dev
RUN apt install -y python python-dev python-pip
RUN apt install -y python3 python3-dev python3-pip

# Set the working directory for containers
WORKDIR .

# Installing python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Installing opencv
RUN cd ~ && \
    mkdir -p ocv-tmp && \
    cd ocv-tmp && \
    curl -L https://github.com/opencv/opencv/archive/4.2.0.zip -o ocv.zip && \
    unzip ocv.zip && \
    cd opencv-4.2.0 && \
    mkdir release && \
    cd release && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D BUILD_PYTHON_SUPPORT=ON \
          .. && \
    make -j8 && \
    make install && \
    rm -rf ~/ocv-tmp

# Installing dlib
RUN pip3 install dlib

# Copy all the files from the project’s root to the working directory
COPY src/ /src/
COPY model/ /model/

# Running Python Application
#CMD ["python3", "/src/main.py"]
ENTRYPOINT ["python3", "/src/main.py"]