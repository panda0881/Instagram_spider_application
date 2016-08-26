from Instagram_Spider import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import words
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from sklearn import tree


def formatting_data(dict_pair):
    data_dict = dict_pair[0]
    data_list = list()
    category_list = ['art', 'food', 'life', 'fashion', 'travel', 'animal', 'family', 'others', 'unknown',
                     'technology', 'sport']
    for category in category_list:
        data_list.append(data_dict[category])
    result = (data_list, dict_pair[1])
    return result


def load_dictionary(dict_name):
    file = open(dict_name, 'r')
    dict_data = json.load(file)
    file.close()
    return dict_data


def store_dictionary(dict_name, dict_data):
    file = open(dict_name, 'w')
    json.dump(dict_data, file)
    file.close()


def combine_dictionary(official_word_list, dictionary):
    official_word_list1 = list(official_word_list)
    for category in dictionary:
        word_list = dictionary[category]
        for word in word_list:
            official_word_list1.append(word)
    official_word_list2 = set(official_word_list1)
    return official_word_list2


def clean_up_string(old_string):
    characters = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    new_string = ''
    for char in old_string:
        if char in characters:
            new_string += char
    return new_string.lower()


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


def analyze_words(my_words, dictionary):
    local_similarity_dictionary = dict()
    distribution_dictionary = dict()
    total_number = 0
    valid_word_count = 0
    for category in dictionary:
        local_similarity_dictionary[category] = 0
        distribution_dictionary[category] = list()
    distribution_dictionary['unknown'] = list()
    one_tenth = int(len(my_words) / 10)
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


wordlist = set(words.words())
wordnet_lemmatizer = WordNetLemmatizer()
brown_ic = wordnet_ic.ic('ic-brown.dat')
semcor_ic = wordnet_ic.ic('ic-semcor.dat')
my_dictionary = load_dictionary('Instagram_tag_dictionary.json')
wordlist = combine_dictionary(wordlist, my_dictionary)
spider = InstagramSpider()

file_name = 'train_data.json'
file = open(file_name, 'r')
train_data = json.load(file)
file.close()

file_name = 'test_data.json'
file = open(file_name, 'r')
test_data = json.load(file)
file.close()

train_list = list()
train_result = list()
test_list = list()
test_result = list()
for train_pair in train_data:
    tmp = formatting_data(train_pair)
    train_list.append(tmp[0])
    train_result.append(tmp[1])

for test_pair in test_data:
    tmp = formatting_data(test_pair)
    test_list.append(tmp[0])
    test_result.append(tmp[1])

clf = tree.DecisionTreeClassifier()
clf.fit(train_list, train_result)

result = clf.predict(test_list)

for data in test_data:
    print(data)
print(test_result)
print(result)
print(clf.score(test_list, test_result))

print('end')
