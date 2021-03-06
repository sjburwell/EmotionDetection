########################################################################################
# Author: Amrit Singhal, Year: 2018                                                    #
# Emotion Extraction from Images in the Circumplex model: Arousal and Valence values   #
# Details:                                                                             #
# Python Implementation of the paper 'Building Emotion Machines: Recognizing Image     #
# Emotion through Deep Neural Networks' by Hye-Rin Kim, Yeong-Seok Kim, Seon Joo Kim,  #
# and In-Kwon Lee.                                                                     #
# Model from https://github.com/amr4i/EmotionDetection                                 #
########################################################################################


import os
import sys
import json
import pickle
import numpy as np
import tensorflow as tf
from extract_features import get_prediction_features

parameter_file = "test_params.json"
params = json.loads(open(parameter_file).read())

test_file = sys.argv[1]
data_directory = sys.argv[2]


if params['extract_features'] == 'true':
    x_pred = get_prediction_features(test_file, data_directory, params['vgg_file'], params['gistFile'], params['semF_file'])
    with open('x_pred.pickle', 'wb') as f:
        pickle.dump(x_raw, f, protocol=pickle.HIGHEST_PROTOCOL)
else:
    with open(params['x_file'], 'rb') as f:
        x_pred = pickle.load(f)

# x_pred = get_prediction_features(test_file, data_directory, params['vgg_file'], params['gistFile'], params['semF_file'])

timestamp = sys.argv[3]

out_dir = os.path.abspath(os.path.join( os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "modelData/trained_model_" + timestamp))
checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))

with tf.Session() as sess:    
	saver = tf.train.import_meta_graph(checkpoint_dir+"/"+params["best_model"]+".meta")
	saver.restore(sess,tf.train.latest_checkpoint(checkpoint_dir))

	graph = tf.get_default_graph()
	# for i in graph.get_operations():
	# 	if 'prediction' in str(i):
	# 		print i
	input_x = graph.get_tensor_by_name("input_x:0")
	prediction = graph.get_tensor_by_name("prediction/BiasAdd:0")
	output = sess.run(prediction , feed_dict={input_x: x_pred})
	# print output

with open(test_file, 'r') as f:
	names = f.readlines()

with open("results.txt", "w") as g:
	for i in range(0,len(names)):
		g.write(names[i].strip()+","+str(output[i][0]*100.0)+"\n")