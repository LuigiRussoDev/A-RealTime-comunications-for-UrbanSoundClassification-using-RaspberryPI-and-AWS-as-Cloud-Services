
import glob
import os
import librosa
import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

from sklearn.preprocessing import StandardScaler

duration = 0.1  # seconds
sample_rate=44100


'''0 = air_conditioner
1 = car_horn
2 = children_playing
3 = dog_bark
4 = drilling
5 = engine_idling
6 = gun_shot
7 = jackhammer
8 = siren
9 = street_music'''



def extract_features():
	X = np.loadtxt("scaricatoS3.txt")
	X= np.squeeze(X)

	stft = np.abs(librosa.stft(X))
	mfccs = np.array(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=8).T)
	
	chroma = np.array(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T)
	mel = np.array(librosa.feature.melspectrogram(X, sr=sample_rate).T)
	contrast = np.array(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T)
	tonnetz = np.array(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T)
	ext_features = np.hstack([mfccs,chroma,mel,contrast,tonnetz])
	
	#print "Lunghezza: ", len(ext_features.shape)
	#features = np.vstack([features,ext_features])
	return ext_features 

model_path = "model/model"

fit_params = np.load('fit_params.npy')

sc = StandardScaler()
sc.fit(fit_params)

n_dim = 161
n_classes = 2
n_hidden_units_one = 256
n_hidden_units_two = 256
sd = 1 / np.sqrt(n_dim)
learning_rate = 0.01

X = tf.placeholder(tf.float32,[None,n_dim])
Y = tf.placeholder(tf.float32,[None,n_classes])

W_1 = tf.Variable(tf.random_normal([n_dim,n_hidden_units_one], mean = 0, stddev=sd))
b_1 = tf.Variable(tf.random_normal([n_hidden_units_one], mean = 0, stddev=sd))
h_1 = tf.nn.tanh(tf.matmul(X,W_1) + b_1)

W_2 = tf.Variable(tf.random_normal([n_hidden_units_one,n_hidden_units_two], mean = 0, stddev=sd))
b_2 = tf.Variable(tf.random_normal([n_hidden_units_two], mean = 0, stddev=sd))
h_2 = tf.nn.sigmoid(tf.matmul(h_1,W_2) + b_2)

W = tf.Variable(tf.random_normal([n_hidden_units_two,n_classes], mean = 0, stddev=sd))
b = tf.Variable(tf.random_normal([n_classes], mean = 0, stddev=sd))
y_ = tf.nn.softmax(tf.matmul(h_2,W) + b)


init = tf.global_variables_initializer()
#init = tf.initialize_all_variables()

 
saver = tf.train.Saver()

print "Sono qui adesso"

y_true, y_pred = None, None
with tf.Session() as sess:

    saver.restore(sess, model_path)
    print "Model loaded"
    
    sess.run(tf.global_variables())
	
    feat = extract_features()
    feat = sc.transform(feat)
    y_pred = sess.run(tf.argmax(y_, 1), feed_dict={X: feat})    
    print y_pred
	

