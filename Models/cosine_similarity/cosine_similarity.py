# 
# 
# Code to predict the author name and the poem era given on the testing data
# based on the training data.
# The Model used here is Cosine similarity. Which finds the vector with the smallest
# dot product with the given vector
# 
# 

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity 

vectorizer = TfidfVectorizer() 

train_input_file = input("Enter training file name: ")
test_input_file = input("Enter test file name: ")

# Used to load the TfIdf vectors 
with open(train_input_file,"rb") as f:
    train_data = pickle.load(f)

train_data_vectors = []

map_poem_era = {}
map_poem_author = {}

# Store the author names and poem eras for the training data vectors
poem_index = 0
for element in train_data:
	author_name = element[0]
	poem_era = element[3]
	map_poem_author[poem_index] = author_name
	map_poem_era[poem_index] = poem_era
	poem = element[4]
	poem_vector = element[5]
	train_data_vectors.append(poem_vector)
	poem_index = poem_index + 1

with open(test_input_file,"rb") as f:
    test_data = pickle.load(f)

correct_poem_eras_detected = 0
correct_poem_authors_detected = 0

poem_count_so_far = 1

test_data_vectors = []

map_correct_poem_era = {}
map_correct_poem_author = {}

# Store the correct author names and poem eras for the testing data vectors
poem_index = 0 
for element in test_data:
	correct_author_name = element[0]
	correct_poem_era = element[3]
	correct_poem = element[4]
	correct_poem_vector = element[5]

	map_correct_poem_era[ poem_index ] = correct_poem_era
	map_correct_poem_author[ poem_index ] = correct_author_name
	poem_index = poem_index + 1

	test_data_vectors.append(correct_poem_vector)

# Compute the cosine similarity using the function included in sklearn library
cos_sim = cosine_similarity(test_data_vectors,train_data_vectors)
print(cos_sim)

# For all poems in the testing data
# Find the vector which is most similar to the vector in the training set
poem_index = 0
for elem in cos_sim:
	max_similarity = elem[0]
	max_index = 0
	index = 0
	for val_similarity in elem:
		if val_similarity > max_similarity:
			max_similarity = val_similarity
			max_index = index
		index = index + 1

	predicted_author_name = map_poem_author[max_index]
	predicted_poem_era = map_poem_era[max_index]

	correct_author_name = map_correct_poem_author[poem_index]
	correct_poem_era = map_correct_poem_era[poem_index]

	print("Index: " + str(poem_index))	
	poem_index = poem_index + 1
	if predicted_poem_era == correct_poem_era:
		print("Poem Era: Correct")	
		correct_poem_eras_detected = correct_poem_eras_detected + 1
	else:
		print("Poem Era: Wrong")	

	if predicted_author_name == correct_author_name:
		print("Author Name: Correct")	
		correct_poem_authors_detected = correct_poem_authors_detected + 1
	else:
		print("Author Name: Wrong")	
	print("\n")

# Show necessary outputs
print("Total Poems in testing data: " + str(len(test_data)))
print("Correct Eras determined: " + str(correct_poem_eras_detected))
print("Correct Authors testing data: " + str(correct_poem_authors_detected))
print("\n\n")

print("Accuracy for era detection: " + str(correct_poem_eras_detected/len(test_data)))
print("Accuracy for authors detection: " + str(correct_poem_authors_detected/len(test_data)))
print("\n\n")
