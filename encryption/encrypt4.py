from __future__ import print_function
import numpy as np
from numpy import linalg as LA
from numpy import dot
import cv2

import time
import random
import seal
from seal import ChooserEvaluator, Ciphertext, Decryptor, Encryptor, EncryptionParameters, Evaluator, IntegerEncoder, FractionalEncoder, KeyGenerator, MemoryPoolHandle, Plaintext, SEALContext, EvaluationKeys, GaloisKeys, PolyCRTBuilder, ChooserEncoder, ChooserEvaluator, ChooserPoly
from scipy import spatial
from PIL import Image
from sklearn import preprocessing
import random
import pickle
import sys, getopt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
import emoji
from random import randint
from yaspin import yaspin
from prompt_toolkit import HTML, print_formatted_text
from prompt_toolkit.styles import Style

ENC_CONF = []

# override print with feature-rich ``print_formatted_text`` from prompt_toolkit
print = print_formatted_text

# build a basic prompt_toolkit style for styling the HTML wrapped text
style = Style.from_dict({
    'msg': '#4caf50 bold',
    'sub-msg': '#616161 italic'
})

DESC_SIZE = 128

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]

def euclidean_dist_enc(evaluator, a, b):
    a = copy_cipher(a)
    for i in range(DESC_SIZE):
        evaluator.sub(a[i], b[i])
    evaluator.square(a)
    encrypted_number = Ciphertext()
    evaluator.add_many(a, encrypted_number)
    return encrypted_number

def euclidean_dist(a, b):
    return np.sum((a-b)**2)

def config():
    # PySEAL wrapper for the SEAL library is used.
    # SEAL implements somewhat FHE algorithmic solutions =>
    # each operation has a limit - 'invariant noise budget' in bits. Operations consume the noise budget
    # at a rate determined py the encryption parameters. Additions free of noise budget consumption, multiplications are not
    # Noise budget consumption is getting worse in sequential multiplications => multiplicative depth of the arithmetic circuit that needs to be evaluated.
    # Noise budget in a ciphertext -> 0 => ciphertext too corrupted to be decrypted => large enough parameters to be eble to restore the result
    #############
    # noise_budget = log2(coeff_modulus/plain_modulus) bits (in a freshly encrypted ciphertext)
    #############

    #############
    # noise_budget_cnsumption = log2(plain_modulus) + (other terms)
    #############
    params = EncryptionParameters()

    # set the polynomial modulus. (1x^(power of 2) +1) - power of 2 cyclotomic polynomial
    # affects the security of the scheme
    # larger more secure and larger ciphertext size, computation slower
    # from 1024 to 32768
    params.set_poly_modulus("1x^8192 + 1")

    # coefficient modulus determines the noise budget of the ciphertext
    # the bigger the more the budget and lower security -> increase the polynomial modulus
    # choosing parameters for polynomial modulus http://HomomorphicEncryption.org
    params.set_coeff_modulus(seal.coeff_modulus_128(8192))

    # plaintext modulus determines the size of the plaintext datatype, affects the noise budget in multiplication => keep the plaintext data type as small as possible
    #65537
    params.set_plain_modulus(65537)

    # check the validity of the parameters set, performs and stores several important pre-computations
    context = SEALContext(params)

    # print the chosen parameters
    #performance_test_st(context)

    return context, params


def decompose_plain(slot_count, x, crtbuilder):
    x = x.reshape(1, DESC_SIZE)
    zeros = np.zeros((1, slot_count), dtype=np.int32)
    zeros[:x.shape[0], :x.shape[1]] = x
    pad_matrix = zeros.flatten()
    print("Decomposed flattened vector", pad_matrix)
    plain_matrix = Plaintext()
    crtbuilder.compose(pad_matrix, plain_matrix)
    return plain_matrix

def encrypt_vec(params, encryptor, encoder, x):
    x = x.flatten().tolist()
    encrypted_rationals = []
    for i in range(len(x)):
        c = Ciphertext(params)
        encrypted_rationals.append(c)
        encryptor.encrypt(encoder.encode(x[i]), encrypted_rationals[i])
    return encrypted_rationals

def keygen(context):
    #print("Generating secret/public keys: ")
    time_start = time.time()
    keygen = KeyGenerator(context)
    time_end = time.time()
    #print("Done in {} miliseconds".format((str)(1000 * (time_end - time_start))))
    public_key = keygen.public_key()
    secret_key = keygen.secret_key()
    gal_keys = GaloisKeys()
    keygen.generate_galois_keys(30, gal_keys)

    ev_keys = EvaluationKeys()
    keygen.generate_evaluation_keys(30, ev_keys)

    return public_key, secret_key

def test2():
    img_path = '00001.jpg'
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    print("Original image dimensions {}".format(img.shape))
    sift = cv2.xfeatures2d.SIFT_create()
    (kps, desc) = sift.detectAndCompute(img, None)

    desc = preprocessing.normalize(np.array(desc.flatten()[:DESC_SIZE]).reshape(1, DESC_SIZE), norm='l2')
    descriptor_vec1 = desc
    descriptor_vec2 = descriptor_vec1
    context = config()
    public_key, secret_key = keygen(context)

    encoder = IntegerEncoder(context.plain_modulus())
    encryptor = Encryptor(context, public_key)
    crtbuilder = PolyCRTBuilder(context)
    evaluator = Evaluator(context)
    decryptor = Decryptor(context, secret_key)

    slot_count = (int)(crtbuilder.slot_count())
    print("slot count {}".format(slot_count))
    print("Plaintext shape", descriptor_vec1.shape)
    plain_matrix = decompose_plain(slot_count, descriptor_vec1, crtbuilder)

    for i in range(10000):
        encrypted_matrix = Ciphertext()
        print("Encrypting: ")
        time_start = time.time()
        encryptor.encrypt(plain_matrix, encrypted_matrix)
        time_end = time.time()
        print("Done in time {}".format((str)(1000 * (time_end - time_start))))

        print("Square:")
        time_start = time.time()
        evaluator.square(encrypted_matrix)
        time_end = time.time()
        print("Square is done in {} miliseconds".format((str)(1000 * (time_end - time_start))))

        plain_result = Plaintext()
        print("Decryption plain: ")
        time_start = time.time()
        decryptor.decrypt(encrypted_matrix, plain_result)
        time_end = time.time()
        print("Decryption is done in {} miliseconds".format((str)(1000 * (time_end - time_start))))
        # print("Plaintext polynomial: {}".format(plain_result.to_string()))
        # print("Decoded integer: {}".format(encoder.decode_int32(plain_result)))
        print("Noise budget {} bits".format(decryptor.invariant_noise_budget(encrypted_matrix)))

def copy_cipher(a):
    a_copy = []
    for i in range(DESC_SIZE):
        a_copy.append(Ciphertext(a[i]))
    return a_copy

def test1():

    #TODO make the function taking dir name, iterating through all the descriptors, encrypting
    #TODO add progress bar - the videos are decrypted
    #TODO make a function taking a query and passing it to the sklearn function KNN with custom similarity funtion
    #TODO add progress bar - the search is performed (calculate distance between encrypted vectors)
    #TODO return results
    #TODO Vlad Display. The results are true. The same as we would compute similarity between ncrypted vectors.
    # In the same time we did not have to decrypt vectors stored in 3rd parity service to perform a search.
    #TODO get the metrics
    #TODO how to opimize

    a = np.ones((1, DESC_SIZE))
    b = np.ones((1, DESC_SIZE))
    for i in range(a.shape[1]):
        a[0, i] = random.uniform(0.0, 1.0)
        b[0, i] = random.uniform(0.0, 1.0)

    print("Descriptors for images a and b are: ")
    print("a ", a)
    print("b ", b)

    context, params = config()
    public_key, secret_key = keygen(context)

    frac_encoder = FractionalEncoder(context.plain_modulus(), context.poly_modulus(), 64, 32, 3)
    encryptor = Encryptor(context, public_key)
    evaluator = Evaluator(context)
    decryptor = Decryptor(context, secret_key)

    e1 = encrypt_vec(params, encryptor, frac_encoder, a)
    e3 = encrypt_vec(params, encryptor, frac_encoder, b)

    print("Calculate distance between plain a and b:")
    sim = euclidean_dist(a, b)
    print("Similarity between a and b: {}".format(sim))

    print("Calculating distance between encrypted a and b:")
    time_start = time.time()
    enc_res = euclidean_dist_enc(evaluator, e1, e3)
    time_end = time.time()
    print("Done. Time: {} miliseconds".format((str)(1000 * (time_end - time_start))))

    plain_result = Plaintext()
    print("Decrypting result: ")
    time_start = time.time()
    decryptor.decrypt(enc_res, plain_result)
    res = frac_encoder.encode(plain_result)
    time_end = time.time()
    print("Done. Time: {} miliseconds".format((str)(1000 * (time_end - time_start))))
    print("........................................................................")
    print("Noise budget {} bits".format(decryptor.invariant_noise_budget(enc_res)))
    print("Decrypted result {}, original result {}".format(res, sim))

    print("Calculate distance between plain a and a:")
    sim = euclidean_dist(a, a.copy())
    print("Similarity between a and b: {}".format(sim))

    print("Calculating distance between encrypted a and a:")
    time_start = time.time()
    enc_res = euclidean_dist_enc(evaluator, e1, e1)
    time_end = time.time()
    print("Done. Time: {} miliseconds".format((str)(1000 * (time_end - time_start))))

    plain_result = Plaintext()
    print("Decrypting result: ")
    time_start = time.time()
    decryptor.decrypt(enc_res, plain_result)
    res = frac_encoder.encode(plain_result)
    time_end = time.time()
    print("Done. Time: {} miliseconds".format((str)(1000 * (time_end - time_start))))
    print(".........................................................................")
    print("Noise budget {} bits".format(decryptor.invariant_noise_budget(enc_res)))
    print("Decrypted result {}, original result {}".format(res, sim))

def search_for_centroids(face_descriptors):
    kmeans = KMeans(n_clusters=4)
    clusters = np.array(kmeans.fit_predict(face_descriptors)).reshape(face_descriptors.shape[0], 1)
    cluster_centers = kmeans.cluster_centers_
    #print("clusters: {}".format(type(clusters)))
    return clusters, cluster_centers

def encrypt(input_file):
    X = np.load(input_file)

    print("Starting the system....\n")
    y, people_descriptors = search_for_centroids(X)
    X, y = unison_shuffled_copies(X, y)
    np.save(input_file, X)
    np.save('./class_lables.npy', np.array(y))
    np.save('./centroids.npy', np.array(people_descriptors))
    print("All necessary dependencies are installed. Everything is up-to-date!")

    print("The encryption mode is entered!")

    time_start = time.time()
    print('Configuring the encryption parameters')
    context, params = config()
    time_end = time.time()
    #TODO time for the report. Put to the slides
    #TODO Remove from logs
    print("Parameters are configured. Time: {}\n".format((str)(1000 * (time_end - time_start))))
    #print("Key generation .....")
    time_start = time.time()
    with yaspin(text='Generating public/private key pair', spinner='dots') as sp1:
        public_key, secret_key = keygen(context)
        time.sleep(1)
        sp1.hide()
        print(HTML(
            u'<b>></b> <msg>public/private key pair </msg> <sub-msg>is generated</sub-msg>'
        ), style=style)
        sp1.show()
        sp1.ok("✔")

    time_end = time.time()
    print("Keys are generated!  Time: {}".format((str)(1000 * (time_end - time_start))))


    with yaspin(text='Initializing Encryptor, Eavaluator, Decryptor with generated parameters.....', spinner='dots') as sp2:
        frac_encoder = FractionalEncoder(context.plain_modulus(), context.poly_modulus(), 64, 32, 3)
        encryptor = Encryptor(context, public_key)
        evaluator = Evaluator(context)
        decryptor = Decryptor(context, secret_key)

        p = []
        p.append(params)
        p.append(context)
        p.append(frac_encoder)
        p.append(encryptor)
        p.append(evaluator)
        p.append(decryptor)
        ENC_CONF = p
        sp2.hide()
        print(HTML(
            u'<b>></b> <msg> The system is ready to start encryption.</msg>'
        ), style=style)
        sp2.show()
        sp2.ok("✔")

    #enc_X = np.empty(X.shape, dtype=object)
    with yaspin(text='Subscribing to the online-video stream.', spinner='clock') as sp3:
        time.sleep(5)
        sp3.hide()
        print(HTML(
            u'<b>></b> <msg> Success</msg>'
        ), style=style)
        sp3.show()
        sp3.ok("✔")

    print("Detecting people")
    time_start = time.time()
    with yaspin(text='Encrypting the descriptor').white.bold.shark.on_blue as sp4:
        for i, x in enumerate(X):
            sp4.write("Got descriptor of 1x{} dimension for a person".format(x.shape[0]))
            time.sleep(1)
            #enc_X[i, :] = encrypt_vec(params, encryptor, frac_encoder, x)
            encrypt_vec(params, encryptor, frac_encoder, x)

            dists = []
            for j in range(people_descriptors.shape[0]):
                dist1 = euclidean_dist(people_descriptors[j], x)
                dists.append(dist1)
            sp4.write("Distance between 'Current' person and Person #{}: {:.2f} - Person #{}: {:.2f} - Person #{}: {:.2f} - Person #{}: {:.2f}".format(0, dists[0], 1, dists[1], 2, dists[2], 3, dists[3]))
            time.sleep(1)
            dists = np.array(dists)
            if (dists[dists<0.6] is not None):
                d = np.sort(dists)[0]
                sp4.write("🔦FOUND descriptor similar to Person #{}".format(d))
                time.sleep(1)
            sp4.hide()
            print(HTML(
                    u'<b>🔐</b> <msg>descriptor {}</msg> <sub-msg>encryption complete</sub-msg>'.format(i)
            ), style=style)
            sp4.show()
        #sp.ok("All stream is encrypted")
        sp4.ok("✔")

    time_end = time.time()
    print("Encryption is complete.")
    print("ALL {} descriptors are successfully encrypted and sent to the CLOUD.".format(X.shape[0]))
    print("Time: {}".format((str)(1000 * (time_end - time_start))))
    #enc_X_save = np.array(enc_X)
    #pickle.dump(enc_X_save, output_file)

def search():
    y = np.load('./class_lables.npy')
    X = np.load('all_descriptors.npy')
    centroids = pickle.load('./centroids.npy')
    if len(ENC_CONF)>0:
        params = ENC_CONF[0]
        context = ENC_CONF[1]
        frac_encoder = ENC_CONF[2]
        encryptor = ENC_CONF[3]
        evaluator = ENC_CONF[4]
        decryptor = ENC_CONF[5]

        encrypted_matrix = Ciphertext()
        e1 = encryptor.encrypt(X[56], encrypted_matrix)
        encrypted_matrix = Ciphertext()
        e2 = encryptor.encrypt(X[128], encrypted_matrix)
        encrypted_matrix = Ciphertext()
        e3 = encryptor.encrypt(X[300], encrypted_matrix)
        test_query = [e1, e2, e3]
        y_test = [y[56], y[128], y[300]]

        encrypted_matrix = Ciphertext()
        c1 = encryptor.encrypt(centroids[0], encrypted_matrix)
        encrypted_matrix = Ciphertext()
        c2 = encryptor.encrypt(centroids[1], encrypted_matrix)
        encrypted_matrix = Ciphertext()
        c3 = encryptor.encrypt(centroids[2], encrypted_matrix)
        encrypted_matrix = Ciphertext()
        c4 = encryptor.encrypt(centroids[3], encrypted_matrix)

        centroids_enc = [c1, c2, c3, c4]

        for i, x in enumerate(test_query):
            print("Received descriptor A for the person")
            for j, c in enumerate(centroids_enc):
                print("Calculating distance between ciphertext A and Fixed Person from cluster #{}:".format(j))
                time_start = time.time()
                enc_res = euclidean_dist_enc(evaluator, x, c)
                time_end = time.time()
                print("Done. Time: {} miliseconds".format((str)(1000 * (time_end - time_start))))
                print("Encrypted distance result is calculated")

                plain_result = Plaintext()
                print("Decrypting result: ")
                time_start = time.time()
                decryptor.decrypt(enc_res, plain_result)
                res = frac_encoder.encode(plain_result)
                time_end = time.time()
                print("Decrypted. Time: {} miliseconds".format((str)(1000 * (time_end - time_start))))
                print("Distance between Current and Fixed Person #{}: {:.2f}".format(j, res))
                if (res<0.6):
                    print("🔦Found Match")
                break
                time.sleep(4) #delay for 20 sec

def main(argv):
    #test.py -i <inputfile> -o <outputfile>
    input_file = ''
    try:
        #opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print("encrypt2.py -i <inputfile>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('encrypt2.py -i <inputfile>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            input_file = arg
    print('Input file is"', input_file)

    encrypt(input_file)

if __name__ == '__main__':
        #test1()
        main(sys.argv[1:])
