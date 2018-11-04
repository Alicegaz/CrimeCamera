### Prerequisites
cmake-3.11.4
gmp-6.1.2
HElib
ntl-11.3.0
docker
SEAL_2.3.1
git clone https://github.com/Alicegaz/CrimeCamera.git
cd CrimeCamera
cd encryption
git clone https://github.com/Lab41/PySEAL.git
cp Dockerfile /PySEAL/
cp docker-run.sh /PySEAL/
cp docker-build.sh /PySEAL/
cp encrypt4.py /PySEAL/SEALPythonExamples/
cd PySEAL
./docker-build.sh
docker run -it crime-camera-save
export LC_CTYPE=C.UTF-8
python3 ./SEALPythonExamples/encrypt4.py -i ./SEALPythonExamples/all_descriptors.npy
