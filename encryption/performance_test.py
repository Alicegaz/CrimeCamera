#!/usr/bin/python
import random
import numpy as np
import sys
from sklearn.preprocessing import normalize
import pandas as pd
from encrypt4 import unison_shuffled_copies, euclidean_dist, config, decompose_plain, encrypt_vec, keygen, copy_cipher, search_for_centroids, euclidean_dist_enc
import sqlite3
from sqlite3 import Error
import time
from yaspin import yaspin
from prompt_toolkit import HTML, print_formatted_text
from seal import ChooserEvaluator, Ciphertext, Decryptor, Encryptor, EncryptionParameters, Evaluator, IntegerEncoder, FractionalEncoder, KeyGenerator, MemoryPoolHandle, Plaintext, SEALContext, EvaluationKeys, GaloisKeys, PolyCRTBuilder, ChooserEncoder, ChooserEvaluator, ChooserPoly
from prompt_toolkit.styles import Style
import io
import pandas as pd
import ast
import pickle
import os.path
from pympler import asizeof

print = print_formatted_text

style = Style.from_dict({
    'msg': '#4caf50 bold',
    'sub-msg': '#616161 italic'
})

ENC_CONF = []

security_module = None

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

sqlite3.register_adapter(np.ndarray, adapt_array)
sqlite3.register_converter("array", convert_array)

class SecurityModule:
    def __init__(self, batching=False):
        self.context, self.params = config()
        self.batching = batching

    def __setattr__(self, key, value):
        if hasattr(self, key):
            raise Exception("Attempting to alter read-only value")

        self.__dict__[key] = value

    def generate_keys(self):
        with yaspin(text='Generating public/private key pair', spinner='dots') as sp1:
            if self.batching:
                self.public_key, self.secret_key, self.ev_keys, self.gal_keys = keygen(self.context, self.batching)
            else:
                self.public_key, self.secret_key = keygen(self.context, self.batching)

            sp1.hide()
            print(HTML(
                u'<b>></b> <msg>public/private key pair </msg> <sub-msg>is generated</sub-msg>'
            ), style=style)
            sp1.show()
            sp1.ok("✔")

    def configure_params(self):
        with yaspin(text='Initializing Encryptor, Eavaluator, Decryptor with generated parameters.....',
                    spinner='dots') as sp2:
            self.frac_encoder = FractionalEncoder(self.context.plain_modulus(), self.context.poly_modulus(), 64, 32, 3)
            self.encryptor = Encryptor(self.context, self.public_key)
            self.evaluator = Evaluator(self.context)
            self.decryptor = Decryptor(self.context, self.secret_key)
            if self.batching:
                self.crtbuilder = PolyCRTBuilder(self.context)
            sp2.hide()
            print(HTML(
                u'<b>></b> <msg> The system is ready to start encryption.</msg>'
            ), style=style)
            sp2.show()
            sp2.ok("✔")

    def get_params(self):
        return self.params

    def get_encryptor(self):
        return self.encryptor

    def get_frac_encoder(self):
        return self.frac_encoder

    def get_crtbuilder(self):
        if self.batching:
            return self.crtbuilder
        else:
            return None
    def is_batching(self):
        return self.batching

    def get_decryptor(self):
        return self.decryptor

    def get_evaluator(self):
        return self.evaluator

    def get_ev_keys(self):
        return self.ev_keys


def utf8len(s):
    return len(s.encode('utf-8'))

def create_data_base():
    conn = sqlite3.connect('EncryptedDescriptors.db', detect_types=sqlite3.PARSE_DECLTYPES)
    cur = conn.cursor()
    cur.execute("CREATE TABLE ENCDESCRIPTORS (id TEXT PRIMARY KEY, ciphertext pickle);")
    conn.commit()
    cur.close()
    conn.close()

def encrypt_db():
    descriptors10 = pd.read_csv('./fake_descriptors10.csv', sep='\t')
    df = descriptors10.drop(descriptors10.columns[[0]], axis=1)
    X = np.array(df)
    total_encrypt_time = 0

    time_start = time.time()
    try:
        conn = sqlite3.connect('EncryptedDescriptors.db', detect_types=sqlite3.PARSE_DECLTYPES)
        cur = conn.cursor()
        #descriptors10 = pd.read_csv('./fake_descriptors10.csv', sep='\t')
        #df = descriptors10.drop(descriptors10.columns[[0]], axis=1)
        # exclude the headers line
        #X = np.array(df)

        params, encryptor, frac_encoder = security_module.get_params(), security_module.get_encryptor(), security_module.get_frac_encoder()
        is_batching = security_module.is_batching()
        decryptor = security_module.get_decryptor()
        evaluator = security_module.get_evaluator()
        if is_batching:
            crtbuilder = security_module.get_crtbuilder() #enable packing of several pieces of data in a single message, and using the Single Inxtruction Multiple Data paradigm to operate on this message
            ev_keys = security_module.get_ev_keys()

        #time_start = time.time()
        #total_encrypt_time = 0
        with yaspin(text='Encrypting the descriptor').white.bold.shark.on_blue as sp4:
            for i in range(0, len(X)):
                id_d = str(int(X[i][0]))
                descriptor = np.array(ast.literal_eval(' '.join(X[i][1].split()).replace(" ", ", ")))
                time_start1 = time.time()
                if is_batching:
                    ciphertext = encrypt_vec(params, encryptor, frac_encoder, descriptor, crtbuilder)
                else:
                    ciphertext = encrypt_vec(params, encryptor, frac_encoder, descriptor)
                time_end1 = time.time()
                total_encrypt_time+= (time_end1-time_start1)
                serialized_list_new_protocol = pickle.dumps(ciphertext, protocol=-1)
                print("Ciphertext ", str(ciphertext))
                print("Serialized list size by the new protocol {} KB\n".format(asizeof.asizeof(serialized_list_new_protocol)/1024.0))

                ############# JUST For DEBUG REMOVE  IMMITATE SEARCH
                #print("Noise budget in encrypted1: " + (str)(decryptor.invariant_noise_budget(ciphertext)) + " bits")
                #for i in range(1000000):
                #    ciphertext2 = encrypt_vec(params, encryptor, frac_encoder, np.array(ast.literal_eval(' '.join(X[i+1][1].split()).replace(" ", ", "))), crtbuilder)
                #    encrypted = euclidean_dist_enc(evaluator, ciphertext, ciphertext2, is_batching, ev_keys)

                #   print("Noise budget in encrypted1 after {} comparisons: ".format(i+1) + (str)(decryptor.invariant_noise_budget(ciphertext)) + " bits")
                ###################################
                cur.execute("INSERT INTO ENCDESCRIPTORS (id, ciphertext) values(?, ?)", (id_d, serialized_list_new_protocol))
                #deserialized_a = pickle.loads(serialized)
                print(HTML(
                    u'<b>🔐</b> <msg> {} / {} descriptors</msg> <sub-msg>encrypted</sub-msg>'.format(str(i), str(len(X)))
                ), style=style)
            sp4.ok("✔")
    except sqlite3.DatabaseError as e:
        if conn:
            conn.rollback()
            print('Error {}'.format(e))
            sys.exit(1)
    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()
            time_end = time.time()
            print("Encryption is complete.")
            print("ALL {} descriptors are successfully encrypted and sent to the CLOUD.".format(X.shape[0]))
            print("Mean time to encrypt {}".format(total_encrypt_time/len(X)))
            print("Time to encrypt and write to the database: {}".format((str)(1000 * (time_end - time_start))))

def search_immitation(df):
    descriptors = np.array(df)
    graph = []  # stores (number of descriptors, time to search)
    mean_comparison_times = 0
    comparison_times = np.zeros(1, 1000000)  # dependency of time to compare two descriptors and the number of comparisons done for one vector. Depends on the noise budget
    N = 100000
    for i in range(N):
        idx = random.randint(0, 999999)
        start_time = time.time()
        comp_times, mean_comp_times = search(df[idx], df)
        comparison_times += comp_times
        mean_comparison_times += mean_comp_times
        end_time = time.time()
        total = end_time - start_time
        graph.append((i, total))
    mean_search_time = [sum(y) / len(y) for y in zip(*graph)][1]
    mean_comparison_times /= N
    comparison_times = comparison_times / len(comparison_times)
    print("It takes {} in average to search a person descriptor over the 1M other descriptors".format(
        (str)(1000 * (mean_search_time))))
    return mean_search_time, mean_comparison_times, graph, comparison_times


def search(person, df):
    p_id = person[0]
    descriptor = person[1]
    graph = []  # (number of comparisons, time)
    for i, cand in enumerate(df):
        cand_id = cand[0]
        cand_desc = cand[1]
        start_time = time.time()
        dist = euclidean_dist(cand_desc, descriptor)
        end_time = time.time()
        total = end_time - start_time
        graph.append(total)
        if dist < 0.001:
            print("Match found. For id - {} id - {} is a match".format(p_id, cand_id))
            break
    mean_dist_time = np.array(graph).mean()
    return graph, mean_dist_time

def generate_fake_descriptors():
    descriptors10 = []
    for i in range(1000000):
        list10 = normalize(np.array(random.sample(range(0, 255), 10))[:, np.newaxis], axis=0).ravel()
        descriptors10.append([i, list10])

    descriptors10 = pd.DataFrame(descriptors10, columns=['id', 'descriptor'], dtype=float)

    np.save('./fake_descriptors10.npy', descriptors10)
    descriptors10.to_csv('./fake_descriptors10.csv', sep='\t')

def start():
    global security_module
    security_module = SecurityModule(batching=True)
    security_module.generate_keys()
    security_module.configure_params()
    if not os.path.isfile('EncryptedDescriptors.db'):
        create_data_base()
        encrypt_db()

def main():
    start()

if __name__ == '__main__':
    main()

