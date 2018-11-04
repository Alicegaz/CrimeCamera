#
# Container to build Linux SEAL libraries, python wrapper, and examples
#
FROM ubuntu:17.10
MAINTAINER Todd Stavish <toddstavish@gmail.com>

# Install binary dependencies
RUN apt-get -qqy update && apt-get install -qqy \
	g++ \
	git \
	make \
	python3 \
	python3-dev \
	python3-pip \
	sudo \
        libdpkg-perl \
	--no-install-recommends

# Build SEAL libraries
RUN mkdir -p SEAL/
COPY /SEAL/ /SEAL/SEAL/
WORKDIR /SEAL/SEAL/
RUN chmod +x configure
RUN sed -i -e 's/\r$//' configure
RUN ./configure
RUN make
ENV LD_LIBRARY_PATH SEAL/bin:$LD_LIBRARY_PATH

# Build SEAL C++ example
COPY /SEALExamples /SEAL/SEALExamples
WORKDIR /SEAL/SEALExamples
RUN make

# Build SEAL Python wrapper
COPY /SEALPython /SEAL/SEALPython
COPY /SEALPythonExamples /SEAL/SEALPythonExamples
WORKDIR /SEAL/SEALPython
RUN pip3 install --upgrade pip
RUN pip3 install setuptools
RUN pip3 install -r requirements.txt
RUN pip3 install numpy
RUN sudo apt-get update
RUN pip3 install opencv-python==3.4.2.16
RUN pip3 install opencv-contrib-python==3.4.2.16
RUN pip3 install opencv-contrib-python
RUN pip3 install Pillow
RUN apt-get -y install libgl1-mesa-glx
RUN git clone https://github.com/pybind/pybind11.git
RUN sudo apt-get -y update
RUN sudo apt-get -y install libxss1 aptitude
RUN sudo aptitude search libxmu
RUN sudo aptitude -y install libxmu6
RUN sudo aptitude -y install libglib2.0-dev
RUN sudo apt-get -y install libfontconfig1 libxrender1
WORKDIR /SEAL/SEALPython/pybind11
RUN git checkout a303c6fc479662fd53eaa8990dbc65b7de9b7deb
WORKDIR /SEAL/SEALPython
RUN python3 setup.py build_ext -i
ENV PYTHONPATH $PYTHONPATH:/SEAL/SEALPython:/SEAL/bin
RUN cd /tmp \
&& apt-get update \
&& apt-get install -y curl apt-utils wget unzip\
&& rm -rf /var/lib/apt/lists/*
RUN mkdir dataset
RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=15EvLouh0GSqBk7m6E8w5t__Qpp5mNc01' -O image1.jpg
RUN apt-get clean && apt-get -y update && apt-get install -y locales && locale-gen en_US.UTF-8
RUN sudo locale-gen "en_US.UTF-8"
RUN echo 'LANG="en_US.UTF-8"' > /etc/profile.d/locale.sh
RUN echo 'LANGUAGE="en_US.UTF-8"' >> /etc/profile.d/locale.sh
RUN echo 'LC_ALL="en_US.UTF-8"' >> /etc/profile.d/locale.sh
RUN export LC_CTYPE=C.UTF-8
# Return to SEAL root directory
RUN sudo apt-get -y update
RUN sudo apt-get -y install libboost-dev
RUN sudo apt-get -y install libgsl0-dev libeigen3-dev
RUN pip3 install scikit-learn
RUN pip3 install scipy
RUN pip3 install emoji --upgrade
RUN pip3 install ipython
RUN pip3 install ipywidgets
RUN pip3 install --upgrade yaspin
RUN pip3 install prompt_toolkit
RUN jupyter nbextension enable --py widgetsnbextension
RUN cd dataset
RUN pwd
RUN apt-get update && apt-get install -y vim
WORKDIR /SEAL

# Clean-up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
