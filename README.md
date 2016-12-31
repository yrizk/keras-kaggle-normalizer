# keras-kaggle-normalizer

Usage:
python get_data.py competition-sub-path [-valid 0.3]


Downloads data from kaggle. Normalizes data into keras compliant while adding validation and sampling directories. This can become particularly effective with the vgg16 model that can be trained for any image classification problem!
- uses kaggle cli to download the competition from kaggle [this is a requirement for this script to work] 
- creates filesystem structure in compliant with keras. The keras classifier expects a list of directories corresponding to each class in the classification problem
- data coming kaggle is only split into training data and test data. This script splices the training data into validation data (in a directory called valid/) , and
sample data. the heuristics about how to split the data is sourced here:
http://stackoverflow.com/questions/13610074/is-there-a-rule-of-thumb-for-how-to-divide-a-dataset-into-training-and-validatio

## For a complete example, please refer to the the header of the python script. 


