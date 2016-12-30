# keras-kaggle-normalizer
Downloads data from kaggle. Normalizes data into keras compliant while adding validation and sampling directories


- uses kaggle cli to download the competition from kaggle [this is a requirement for this script to work] 
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
python get_data.py competition-sub-path [-valid 0.3]
