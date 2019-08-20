import os
import json
import random


from enum import Enum

"""Label
All the labels we made are in Label class.
Each labels is mapped as a number.
"""
class Label(Enum):
    B_2param  = 0
    B_2param2 = 1
    B_3param  = 2
    B_param   = 3
    B_param2  = 4
    B_param3  = 5
    I_2param  = 6
    I_2param2 = 7
    I_3param  = 8
    I_param   = 9
    I_param2  = 10
    O         = 11


"""get_data
Import data that is correspoding to categories.
We have 3 categories, "train", "valid", and "test".

@split_lenth  : Default value is 62. We have 307 data in total. 
			   Train-set, validation-set, and test-set have 186, 62, and 59 data, respectively.
@original_key : Get all question numbers as keys. It is shuffled to split into datasets.



return two lists. 
train_lex, valid_lex, test_lex : Questions(queries) mapped to a number in the voca-set
train_y,   valid_y,   test_y   : Answers mapped to the label (Label Class)
"""
def get_data(data_category):

	with open('./is13/data/data.json') as f:
		data_query = json.load(f)

	with open('./is13/data/label.json') as f:
		data_slots = json.load(f)
    
	split_length = 62
    
	original_key = list(data_query.keys())
	random.shuffle(original_key)

    
	if (data_category == 'train'):  
		#split train_data
		train_keys = original_key[:split_length*3]
		# select data by keys
		train_data = [data_query[i] for i in train_keys if i in data_query] 

		train_lex = get_query(train_keys, train_data)
		train_y   = get_slot(train_keys, train_data)

		return train_lex, train_y

        
	elif (data_category == 'valid'):  
		#split valid_keys
		valid_keys   = original_key[split_length*3: split_length*4]
		# select data by keys
		valid_data = [data_query[i] for i in valid_keys if i in data_query] 

		valid_lex = get_query(valid_keys, valid_data)
		valid_y   = get_slot(valid_keys, valid_data)

		return valid_lex, valid_y

	elif (data_category == 'test'):  
		#split test_keys
		test_keys  = original_key[split_length*4:]
		# select data by keys
		test_data = [data_query[i] for i in test_keys if i in data_query]

		test_lex = get_query(test_keys, test_data)
		test_y   = get_slot(test_keys, test_data)

		return test_lex, test_y
    


"""
make_slot : Make the data which contain slots (slot name)
@query : The labels we set.
@label : Each problem has different labels. Therefore, Fetch the label which is set for each questions.
@slots : Using class Label, replace query to slots
"""

def get_slot(input_keys, input_data):

	with open('./is13/data/label.json') as f:
		data_slots = json.load(f)

	total_slot = []
    
	for idx in range(len(input_keys)):
		query = [] # we assigned before per question 
		label = data_slots[input_keys[idx]] # label in each question
		slots = []  # integrate label : the output

		for l in input_data[idx]: # l : label
			int_label = int(l[1]) # if it is "O"
			if(int_label == 0):
				slots.append(Label.O.value)
	            #query.append(int(l[1]))
			else:                 # if it is not "O", such as "B" and "I"
				label_name = label[int_label-1]
				label_name = label_name.replace("-", "_") # we have "-" in string, so change it as "_"
				slots.append(Label[label_name].value)

	            #query.append(int(l[1]))
	            
		total_slot.append(slots)
	    #print(query)

	return total_slot

        
        

    
"""
make_query : Make the data which contain query, the word vector
@query : It is an output. It takes the query of question(word vector)
@label : Each problem has different labels. Therefore, Fetch the label which is set for each questions.
"""

def get_query(input_keys, input_data):
	total_query = []
	voca = get_voca()

	for idx in range(len(input_keys)):
		query = []
		for l in input_data[idx]: # l : label
			word = l[0]
	
			if word.isdigit():
				word = "DIGIT" * len(word)
			else:
				word = word.lower()
	  
			index = voca.index(word)
			query.append(index)
	    
		total_query.append(query)


	    
	return total_query
	    
"""
make_voca : To make vocabulary, collect all words, remove duplicates, and create vocabulary set. 
Number is represented as DIGIT * len(number)
"""    
def get_voca():

	with open('./is13/data/data.json') as f:
		data_query = json.load(f)

	with open('./is13/data/label.json') as f:
		data_slots = json.load(f)

	keys = data_query.keys()

	voca = []
	for key in keys:
		words = data_query.values()
		for i in data_query[key]:
			word = (i[0]).lower()
			if word.isdigit():
				word = "DIGIT" * len(word)

			voca.append(word)

	voca = list(set(voca))
	voca.sort(reverse = False) 


	return voca



