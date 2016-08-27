from Instagram_Spider import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from matplotlib import pyplot as plt
import math
import os
import csv


# This function is used to store the tag data into a local file such that you don't need to craw the data again
# when you are trying to analysis the same user. Of course, you can choose disable this function in the main part.
def store_tag_data(name, tag_data):
    file_name = 'user_tag_data/' +name + '_tag_data.json'
    file = open(file_name, 'w')
    json.dump(tag_data, file)
    file.close()


# This function is used to load the data about a specific tag from a local file.
def load_tag_data(name):
    file_name = 'user_tag_data/' +name + '_tag_data.json'
    file = open(file_name, 'r')
    tag_data = json.load(file)
    file.close()
    return tag_data


# This function is used to clean up the strange character such that we can use it for natural language processing.
def clean_up_string(old_string):
    characters = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    new_string = ''
    for char in old_string:
        if char in characters:
            new_string += char
    return new_string.lower()


# This function is used to predict the social influence of a specific user. Basically, we use data, which includes
# the number of followers, the average number of likes and tags used per post, to predict the social influence power
# of this specific user. We used linear regression and existing data to build the mechanism of the prediction.
# The score is 0 to 10 and 10 means the most influential people.
def get_user_influence_power(user):
    print('start to analyze the social influence power of this user...')
    data = spider.get_user_data(user)
    follower_number = data['followed_by']['count']
    media_list = spider.get_media_from_user(user)
    likes_number = 0
    current_number = 0
    tags_number = 0
    for media in media_list:
        current_number += 1
        print('analyzing user media: ' + media + '(' + str(current_number) + '/20)')
        media_data = spider.get_media_data(media)
        likes_number += media_data['likes']['count']
        tags_list = spider.get_tag_from_media(media)
        tags_number += len(tags_list)
    if len(media_list) > 0:
        likes_number /= len(media_list)
        tags_number /= len(media_list)
    quality = follower_number*0.000525 + likes_number*0.989 - tags_number*6.32
    if quality < 0:
        quality = 0
    if quality > 10000:
        quality = 10000
    if follower_number > 1000000:
        follower_number = 1000000
    if quality == 0 or follower_number == 0:
        power = 0
    else:
        power = math.log(quality*follower_number, 10)
    return power


# This function is used to store the dictionary when you are trying to modify the dictionary.
def store_dictionary(dict_name, dict_data):
    file = open(dict_name, 'w')
    json.dump(dict_data, file)
    file.close()


# This function is used to load the dictionary from a local file.
def load_dictionary(dict_name):
    file = open(dict_name, 'r')
    dict_data = json.load(file)
    file.close()
    return dict_data


# This function is used to visualize the analysis result of the user. Basically, we use matplotlib to do the work
# and the result will be stored as a png file.
def display_result(data_dict, confidence, username, tag_name):
    plt.figure(figsize=(9, 9))
    labels = ['family', 'sport', 'animal', 'art', 'technology', 'life', 'fashion', 'food', 'travel']
    colors = ['green', 'blue', 'cyan', 'purple', 'orange', 'pink', 'seagreen', 'red', 'yellow']
    sizes = list()
    explode_list = list()
    max_label = ''
    current_value = 0
    total_value = 0
    for label in labels:
        sizes.append(data_dict[label])
        total_value += data_dict[label]
        if data_dict[label] > current_value:
            current_value = data_dict[label]
            max_label = label
    for label in labels:
        if label == max_label:
            explode_list.append(0.1)
        else:
            explode_list.append(0)
    final_sizes = list()
    if total_value == 0:
        return
    for size in sizes:
        final_sizes.append(size/total_value)
    explode = tuple(explode_list)
    patches, l_text, p_text = plt.pie(final_sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%3.1f%%', shadow=False, startangle=90, pctdistance=0.7)
    for t in l_text:
        t.set_size = 12
    for t in p_text:
        t.set_size = 4
    plt.axis('equal')
    plt.text(-1.2, 1.2, 'username: ' + username, fontsize=15)
    plt.text(-1.2, 1.1, 'confidence: %.2f%%' % (confidence * 100), fontsize=15)
    file_name = 'tag_analysis_result/' + tag_name + '/samples/' + username + '_analysis.png'
    plt.savefig(file_name, format='png')


# This function is used to visualize the analysis overall result of this tag. Basically, we use matplotlib to do the
# work and the result will be stored as a png file.
def display_tag_result(data_dict, confidence, tag_name):
    plt.figure(figsize=(9, 9))
    labels = ['family', 'sport', 'animal', 'art', 'technology', 'life', 'fashion', 'food', 'travel']
    colors = ['green', 'blue', 'cyan', 'purple', 'orange', 'pink', 'seagreen', 'red', 'yellow']
    sizes = list()
    explode_list = list()
    max_label = ''
    current_value = 0
    total_value = 0
    for label in labels:
        sizes.append(data_dict[label])
        total_value += data_dict[label]
        if data_dict[label] > current_value:
            current_value = data_dict[label]
            max_label = label
    for label in labels:
        if label == max_label:
            explode_list.append(0.1)
        else:
            explode_list.append(0)
    final_sizes = list()
    if total_value == 0:
        return
    for size in sizes:
        final_sizes.append(size/total_value)
    explode = tuple(explode_list)
    patches, l_text, p_text = plt.pie(final_sizes, explode=explode, labels=labels, colors=colors,
                                      autopct='%3.1f%%', shadow=False, startangle=90, pctdistance=0.7)
    for t in l_text:
        t.set_size = 12
    for t in p_text:
        t.set_size = 4
    plt.axis('equal')
    plt.text(-1.2, 1.2, 'tag_name: ' + tag_name, fontsize=15)
    plt.text(-1.2, 1.1, 'confidence: %.2f%%' % (confidence * 100), fontsize=15)
    file_name = 'tag_analysis_result/' + tag_name + '/' + 'tag_analysis.png'
    plt.savefig(file_name, format='png')


# This function combine our own dictionary into the overall dictionary such that some special words
# can be recognised by the function.
def combine_dictionary(official_word_list, dictionary):
    official_word_list1 = list(official_word_list)
    for category in dictionary:
        word_list = dictionary[category]
        for word in word_list:
            official_word_list1.append(word)
    official_word_list2 = set(official_word_list1)
    return official_word_list2


# This function converts the tags into words using the maximum recognition algorithm.
def tag2word(tag_list):
    result_list = list()
    for tag_pair in tag_list:
        tag = clean_up_string(tag_pair[0]).lower()
        tag = clean_up_string(tag)
        pos = len(tag)
        while pos > 1:
            word = wordnet_lemmatizer.lemmatize(tag[0:pos])
            if word in wordlist:
                result_list.append((word, tag_pair[1]))
                tag = tag[pos:]
                pos = len(tag)
            else:
                pos -= 1
    print('done...')
    return result_list


# This function analyze all the words that we get from the tags and calculate the similarity of those words with what
# we already got in the dictionary and thus this function will use those results to produce an interest distribution
# map of this user.
def analyze_words(my_words, dictionary):
    local_similarity_dictionary = dict()
    distribution_dictionary = dict()
    total_number = 0
    valid_word_count = 0
    for category in dictionary:
        local_similarity_dictionary[category] = 0
        distribution_dictionary[category] = list()
    distribution_dictionary['unknown'] = list()
    one_tenth = int(len(my_words)/10)
    current_number = 0
    progress = 0
    total_words = 0
    for word_pair in my_words:
        find_category = False
        current_number += 1
        if current_number > one_tenth:
            progress += 1
            current_number = 0
            print('finish ' + str(progress) + '0%')
        for category in dictionary:
            if word_pair[0] in dictionary[category]:
                if not find_category:
                    valid_word_count += 1
                total_number += word_pair[1]
                distribution_dictionary[category].append(word_pair)
                find_category = True
        if find_category:
            continue
        try:
            word = wn.synsets(word_pair[0])[0]
            total_number += word_pair[1]
            valid_word_count += 1
        except:
            continue
        for category in dictionary:
            word_list = dictionary[category]
            total_similarity = 0
            total_categary_words = 0
            for test_word in word_list:
                try:
                    test = wn.synsets(test_word)[0]
                except:
                    continue
                try:
                    total_similarity += word.res_similarity(test, brown_ic)
                    total_categary_words += 1
                except:
                    continue
            if total_categary_words > 0:
                local_similarity_dictionary[category] = total_similarity / total_categary_words
        final_category = 'others'
        for category in local_similarity_dictionary:
            if local_similarity_dictionary[category] > local_similarity_dictionary[final_category]:
                final_category = category
        if local_similarity_dictionary[final_category] > 2.5:
            if local_similarity_dictionary[final_category] > 4:
                if word_pair[0] not in dictionary[final_category]:
                    dictionary[final_category].append(word_pair[0])
            find_category = True
            distribution_dictionary[final_category].append(word_pair)
        if not find_category:
            distribution_dictionary['unknown'].append(word_pair)
    percentage_dictionary = dict()
    for category in distribution_dictionary:
        percentage_dictionary[category] = 0
        for word_pair2 in distribution_dictionary[category]:
            percentage_dictionary[category] += word_pair2[1]
            total_words += word_pair2[1]
    for category in percentage_dictionary:
        if total_words != 0:
            percentage_dictionary[category] /= total_words
    print('done...')
    store_dictionary('Instagram_tag_dictionary.json', dictionary)
    return distribution_dictionary, percentage_dictionary


# This function helps filter out all the characters that can't be encoded by 'UTF-8'.
def strange_character_filter(input_string):
    if input_string is None:
        return ' '
    output_string = ''
    for character in input_string:
        if character != '\n':
            try:
                character.encode("gbk")
                output_string += character
            except UnicodeEncodeError:
                output_string = output_string
    return output_string


# This function records the data about all the people under this tag into a local file.
def record_info(tag_dict, spider, file_name):
    my_file = open(file_name, 'a', newline='')
    my_writer = csv.writer(my_file)
    for user in tag_dict:
        data = spider.get_user_data(user)
        tags = tag_dict[user]
        tag_string = ''
        for tag in tags:
            tag_string = tag_string + '#' + tag[0] + ':' + str(tag[1]) + ' '
        tag_string = strange_character_filter(tag_string)
        row = [strange_character_filter(user), strange_character_filter(data['country_block']),
               strange_character_filter(data['full_name']), strange_character_filter(data['biography']),
               data['followed_by']['count'], tag_string]
        try:
            my_writer.writerow(row)
        except UnicodeEncodeError:
            print('There is something wrong with the data about ' + user)
    my_file.close()

# Setting up all the necessary preparation
wordlist = set(words.words())
wordnet_lemmatizer = WordNetLemmatizer()
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
my_dictionary = load_dictionary('Instagram_tag_dictionary.json')
wordlist = combine_dictionary(wordlist, my_dictionary)
spider = InstagramSpider()
sample_tag_name = 'airbnb'
# Create the folder to store the data
if not os.path.exists('tag_analysis_result/' + sample_tag_name + '/samples'):
    os.makedirs('tag_analysis_result/' + sample_tag_name + '/samples')

field_names = ['username', 'location', 'fullname', 'biography', 'followed by', 'tags']
file_name = 'tag_analysis_result/' + sample_tag_name + '/User_data.csv'
my_file = open(file_name, 'w', newline='')
my_writer = csv.writer(my_file)
my_writer.writerow(field_names)
my_file.close()


top_media_list, full_media_list = spider.get_media_from_tag(sample_tag_name)
user_list = list()
# Pick 100 users from this tag. Of course, you can change the number if you want.
for media in full_media_list:
    data = spider.get_media_data(media)
    user_list.append(data['owner']['username'])
    print('Current user list number: ' + str(len(user_list)))
    user_list = list(set(user_list))
    if len(user_list) >= 100:
        break

total_data_list = list()
confidence_list = list()
tag_result = dict()
for username in user_list:
    data = spider.get_tag_from_user(username)
    print('data got...')
    print('analyzing tags from user: ' + username)
    words_from_tags = tag2word(tag_list=data)
    print('analyzing words from tags from user: ' + username)
    if len(words_from_tags) < 5:
        print('The sample size is too small, so we have to discard this user...')
        continue
    distribute_result, percentage_result = analyze_words(my_words=words_from_tags, dictionary=my_dictionary)
    print('percentage result: ')
    print(percentage_result)
    recognize_rate = 1 - percentage_result['unknown']
    print("our machine's current recognize rate is：%.2f%%" % (recognize_rate * 100))
    if recognize_rate < 0.4:
        print('The recognition rate is too low, so we have to discard this user.')
        continue
    display_result(data_dict=percentage_result, confidence=recognize_rate, username=username, tag_name=sample_tag_name)
    total_data_list.append(distribute_result)
    confidence_list.append(recognize_rate)
    tag_result[username] = data
    print('Current result is: ' + str(len(total_data_list)))
    # pick 50 valid examples to analyze the tag
    if len(total_data_list) >= 50:
        break
# Calculate the overall recognition rate of this tag.
tag_distribute_result = dict()
for category in total_data_list[0]:
    tag_distribute_result[category] = 0
for user_data in total_data_list:
    for category in user_data:
        for word_pair in user_data[category]:
            tag_distribute_result[category] += word_pair[1]
total_words = 0
for category in tag_distribute_result:
    total_words += tag_distribute_result[category]
for category in tag_distribute_result:
    tag_distribute_result[category] /= total_words
total_confidence = 0
for confidence in confidence_list:
    total_confidence += confidence
confidence = total_confidence/len(confidence_list)
# Visualize the data
display_tag_result(data_dict=tag_distribute_result, confidence=confidence, tag_name=sample_tag_name)
# Record the data into a local file
record_info(tag_dict=tag_result, spider=spider, file_name=file_name)

print('end')
