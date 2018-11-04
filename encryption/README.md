### Prerequisites
cmake-3.11.4
gmp-6.1.2
HElib
ntl-11.3.0
docker
SEAL_2.3.1
### Installation
```
git clone https://github.com/Alicegaz/CrimeCamera.git
cd CrimeCamera
cd encryption
```
Clone the repository containing code wraping the SEAL build in a docker container and providing Python API's to the encryption library.
```
git clone https://github.com/Lab41/PySEAL.git
```
Override some files necessary to build the wrapped Python version of SEAL.
```
cp Dockerfile /PySEAL/
cp docker-build.sh /PySEAL/
```
Copy encryption script to the ```PySEAL``` directory
```
cp docker-run.sh /PySEAL/
cp encrypt4.py /PySEAL/SEALPythonExamples/
```
Build a docker image, creating a seal package that can be imported in Python
```
cd PySEAL
./docker-build.sh
```
Run the docker container from the built image
```
docker run -it crime-camera-save
```
Run the encryption script
```
export LC_CTYPE=C.UTF-8
python3 ./SEALPythonExamples/encrypt4.py -i ./SEALPythonExamples/all_descriptors.npy
```
