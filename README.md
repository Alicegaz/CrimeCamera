# A secure Video Management System for crime detection and tracking
## First run on Linux
### Requirements
The basic dependency is Anaconda, so [install it](https://www.anaconda.com/download/).
```
pip install opencv-python   # or https://docs.opencv.org/3.4/d7/d9f/tutorial_linux_install.html
pip install dlib    # or http://dlib.net/compile.html
```
### Getting started
```
git clone https://github.com/Alicegaz/CrimeCamera.git
chmod +x ./download_models.sh
./download_models.sh
```
Download data and additional descriptors data from [Google Drive](https://drive.google.com/drive/folders/17HKUUJT5S8u4idA5ChQagZxBefNmjqBN?usp=sharing).  
Move the `data`'s content into existing `data` folder. Do the same with the `descriptors`s content.

### Running
From project root run:
```bash
cd gui/
```
```python
python gui/window.py
```
