import cv2
import dlib

import numpy as np
import pandas as pd
from tqdm import tqdm

import base64
import time

import sys


DATASET_PATH = '../data/FaceImageCroppedWithAlignment.tsv'
FACES_DUMP_PATH = '../data/faces.npy'

face_rec_model_path = '../models/dlib_face_recognition_resnet_model_v1.dat'
predictor_path = '../models/shape_predictor_68_face_landmarks.dat'

shape_predictor = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


def _dump_descriptors(face_ids, descriptors, dump_path):
    face_ids = np.vstack(face_ids)
    descriptors = np.vstack(descriptors)
    faces = np.hstack([face_ids, descriptors])
    
    np.save(dump_path, faces)
    

max_num_lines = 8456240
num_lines = 1000000000000
dump_freq = 100000

face_ids = []
descriptors = []

start_time = time.time()

with open(DATASET_PATH, 'r') as tsv_f:
    for i, row_str in tqdm(enumerate(tsv_f), total=min(num_lines, max_num_lines)):
        
        if i >= num_lines:
            break
        
        row = row_str.split('\t')
        mid, face_id, data = row[0], row[4], base64.b64decode(row[-1][:-1])
        
        with open('../data/tmp.png', 'wb') as f:
            f.write(data)
        img = cv2.imread('../data/tmp.png')[..., ::-1]
        
        face_id = int(face_id.split('FaceId-')[-1])
        face_ids.append(face_id)
        
        shape = shape_predictor(img, dlib.rectangle(0, 0, img.shape[1], img.shape[0]))
                
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        
        face_descriptor = np.array(face_descriptor)
        descriptors.append(face_descriptor)
        
        if i % dump_freq == 1:
            cur_time = time.time()
            print('time spent: {} secs'.format(cur_time - start_time))
            sys.stdout.flush()
            _dump_descriptors(face_ids, descriptors, FACES_DUMP_PATH)
        
    cur_time = time.time()
    print('time spent: {} secs'.format(cur_time - start_time))
    sys.stdout.flush()
    _dump_descriptors(face_ids, descriptors, FACES_DUMP_PATH)
