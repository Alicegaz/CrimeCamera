cd models
wget http://dlib.net/files/mmod_human_face_detector.dat.bz2
bzip2 -dk mmod_human_face_detector.dat.bz2
rm mmod_human_face_detector.dat.bz2
wget http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2
bzip2 -dk dlib_face_recognition_resnet_model_v1.dat.bz2
rm dlib_face_recognition_resnet_model_v1.dat.bz2
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -dk shape_predictor_68_face_landmarks.dat.bz2
rm shape_predictor_68_face_landmarks.dat.bz2
cd ..
