import json
import csv

file_name = 'Instagram_tag_dictionary.json'
file = open(file_name, 'r')
dictionary = json.load(file)
file.close()

field_names = ['category', 'words']
file_name = 'Instagram_tag_dictionary.csv'
my_file = open(file_name, 'w', newline='')
my_writer = csv.writer(my_file)
my_writer.writerow(field_names)

for category in dictionary:
    word_list = dictionary[category]
    tmp_word_list = list()
    for word in word_list:
        if len(tmp_word_list) == 20:
            word_string = ''
            for tmp_word in tmp_word_list:
                word_string += tmp_word
                word_string += ', '
            word_string = word_string[:-2]
            my_writer.writerow([category, word_string])
            tmp_word_list = list()
        tmp_word_list.append(word)
    word_string = ''
    for tmp_word in tmp_word_list:
        word_string += tmp_word
        word_string += ', '
    word_string = word_string[:-2]
    my_writer.writerow([category, word_string])
    tmp_word_list = list()


my_file.close()

print('end')
