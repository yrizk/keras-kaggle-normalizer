import sys

"""
- uses kaggle cli to download the competition from kaggle 
- creates filesystem structure in compliant with keras. The keras classifier expects a list of directories corresponding to each class in the classification problem
- data coming kaggle is only split into training data and test data. This script splices the training data into validation data (in a directory called valid/) , and 
sample data. the heuristics about how to split the data is sourced here: 
http://stackoverflow.com/questions/13610074/is-there-a-rule-of-thumb-for-how-to-divide-a-dataset-into-training-and-validatio

By way of example, this is the filesystem you inherit when you download competition data from kaggle 
	catsanddogsredux/
		train/
			dog.001.jpg
			cat.001.jpg
			...
		test/
			001.jpg
			002.jpg
			003.jpg
			...
Becomes: 
	catsanddogsredux/
		train/
			cats/
				cat.005.jpg
				cat.006.jpg
				...
			dogs/
				dog.007.jpg
				dog.008.jpg
				...
		sample/
			cats/
				cat.003.jpg
				cat.004.jpg
				...
			dogs/
				dog.003.jpg
				dog.004.jpg
				...
		valid/
			cats/
				cat.001.jpg
				cat.002.jpg
				...
			dogs/
				dogs.001.jpg
				dogs.002.jpg
				...
		test/
			001.jpg
			002.jpg
			...
Usage: 
python keras_normalizer.py competition-sub-path [-valid 0.3]

-valid: a floating point number less than 1.0 indicating how much of the training 
should become validation data. 

"""
import sys
import os
import shutil
import random
import subprocess

debug = False 

competition = ''
home_dir = '/home/ubuntu'
tmp_dir = os.path.join(home_dir,'tmp')
data_dir = os.path.join(home_dir,'nbs/data')

training_dir = ''
validation_dir = ''
sample_dir = ''
validation_percentage = 0.2

def main():
	validate()
	init_tmp()
	get_comp(sys.argv[1])
	clean_tmp()	
	init_dirs()
	split_data()
	print 'done'

def mkdir(path):
	os.system('mkdir -p ' + path)

def split_data():
	training_classes = build_training_classes_dirs()
	for training_class in training_classes:
		split_for_validation(training_class)
		split_for_sample(training_class)

def build_training_classes_dirs():
	training_classes = [] # here, class is a mathematical definition 
	global training_dir
	os.chdir(training_dir)
	files = os.listdir('.')
	for f in files: 
		training_class = f.split('.')[0]
		class_dir = training_dir + '/' + training_class
		if training_class not in training_classes:
			mkdir(training_class)
			training_classes.append(training_class)	
		shutil.move(f,class_dir)
	return training_classes; 

def split_for_validation(training_class):
	os.chdir(os.path.join(training_dir,training_class))
	mkdir(os.path.join(validation_dir, training_class))
	training_data = os.listdir('.')
	for f in training_data:
		rand = random.random() 
		if rand <= validation_percentage:
			shutil.move(f,os.path.join(validation_dir,training_class))

def split_for_sample(training_class):
	os.chdir(os.path.join(training_dir,training_class))
	mkdir(os.path.join(sample_dir,training_class))
	files_taken = 0
	training_files = os.listdir('.')
	for f in training_files:
		if files_taken > 99: 
			break
		shutil.move(f,os.path.join(sample_dir,training_class))
		files_taken += 1
	
def validate():
	arg_len = len(sys.argv)
	if arg_len < 2:
		sys.exit('error. incorrect usage. See documentation.')
	if arg_len > 2 and arg_len is not 4: 
		sys.exit('error . incorrect usage')
	if arg_len is 4: 
		validation_percentage = sys.argv[3]
		if validation_percentage < 0 or validation_percentage > 1:
			sys.exit('incorrect validation percentage. See documentation.')


def init_tmp():
	mkdir(tmp_dir)
	os.chdir(tmp_dir)

def init_dirs():
	global training_dir
	training_dir = os.path.join(data_dir,'train')
	global validation_dir 
	validation_dir = os.path.join(data_dir,'valid')
	global sample_dir 
	sample_dir = os.path.join(data_dir,'sample')
	mkdir(validation_dir) 
	mkdir(sample_dir)

def clean_tmp():
	global data_dir
	os.system('cp -r ' + tmp_dir + ' ' + data_dir)
	shutil.rmtree(tmp_dir)
	data_dir += '/' + competition

def get_comp(comp_uri):	
	global competition, tmp_dir
	competition = comp_uri
	tmp_dir = os.path.join(tmp_dir, competition)
	mkdir(competition)
	os.chdir(competition)
	if debug:
		repo_dir = os.path.join(home_dir,'repo')
		os.system('cp ' + repo_dir + '/train.zip .')
		os.system('cp ' + repo_dir + '/test.zip  .')
	else:
		os.system('kg download -v -u yohanrizk -p Nomad123! -c' + comp_uri)
	os.system('unzip -q train.zip')
	os.system('unzip -q test.zip')
	os.remove('train.zip')
	os.remove('test.zip')

if __name__ == '__main__':
	main()
	
