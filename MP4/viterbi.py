"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
from collections import Counter
import time
import math
import numpy as np

def baseline(train, test):
    '''
    TODO: implement the baseline algorithm. This function has time out limitation of 1 minute.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
            test data (list of sentences, no tags on the words)
            E.g  [[word1,word2,...][word1,word2,...]]
    output: list of sentences, each sentence is a list of (word,tag) pairs.
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''
    predicts=[]
    tag=train[0][0][1]
    for sentence in test :
        list=[]
        for word in sentence :
            list.append((word, tag))
        predicts.append(list)
    return predicts

    """
    #start= time.time()

    predicts = []
    tags = []

    for sentence in train :
        for word in sentence :
            if word[1] in tags :
                pass
            else :
                tags.append(word[1])

    list1 = []
    for i in range(0, len(tags)) :
         list1.append([])


    for sentence in train :
        for word in sentence :
            for i in range(0, len(tags)):
                if tags[i] == word[1] :
                    list1[i].append(word[0])

    counter = []
    for i in range(0, len(tags)) :
        counter.append(Counter(list1[i]))

    nb_tag = 0
    best_tag = None
    for i in range(0, len(tags)) :
        nb_word_tag = sum(counter[i].values())
        if nb_word_tag > nb_tag :
            best_tag = tags[i]
            nb_tag = nb_word_tag

    for sentence in test :
        list2=[]
        for word in sentence :
            nb_more = 0
            tag_found = None
            for i in range(0, len(counter)) :
                if word in counter[i] :
                    nb_found = counter[i][word]
                    if nb_found > nb_more :
                        nb_more = nb_found
                        tag_found = tags[i]
            if tag_found == None :
                tag_found = best_tag
            list2.append((word, tag_found))
        predicts.append(list2)
    #end=time.time()
    #print(end-start)

    return predicts
    """
def viterbi_p1(train, test):
    '''
    TODO: implement the simple Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''

    start= time.time()

    laplace = 0.1 #sur de ça ? peut etre ça passera pas les tests avec 0.1

    predicts = [] #les prédictions à retourner
    list_occur = [] #la liste avec les tags
    tag_occurences = [] #le nombre de fois que les tags apparaissent
    tag_pairs = [] #les pairs de tags à la suite
    tag_pairs_counter = [] #la liste pour conter les pairs de tags
    tag_word_pairs = Counter() #le compteur des pairs de tags
    tags = [] #la liste de tag
    list_initial = [] #liste avec les tags des premiers mots de phrase
    list_p_initial = [] #liste avec les probas que le tag soit en premier
    list_p_transition = [] #liste des probas que une pair se suive
    list_p_emission = [] #liste avec les probas des emissions
    list_counter_word = [] #liste avec le nombre de fois qu'un tag a un mot

    for sentence in train :
        list_initial.append(sentence[0][1])
        for i in range(0, len(sentence)) :
            tag = sentence[i][1]
            if tag in tags :
                tag_occurences[tags.index(tag)] +=1
            else :
                tags.append(tag)
                tag_occurences.append(1)
            list_occur.append(tag)

    end=time.time()
    print("First loop", end-start)
    start= time.time()

    p_initial = Counter(list_initial) #counter de combien de fois les tags sont en premiers dans la phrase
    nb_initial = len(p_initial)
    nb_word = sum(p_initial.values())

    for i in range(0, nb_initial) :
        list_p_initial.append(math.log((p_initial[tags[i]] + laplace) / (nb_word + laplace * nb_initial)))

    for tag_1 in tags :
        for tag_2 in tags :
           tag_pairs.append((tag_1, tag_2))

    for i in tag_pairs :
        tag_pairs_counter.append(0)

    end=time.time()
    print("Second loop", end-start)
    start= time.time()

    for sentence in train :
        for i in range(0, len(sentence)-1) :
            pair = (sentence[i][1], sentence[i+1][1])
            tag_pairs_counter[tag_pairs.index(pair)] +=1
        tag_word_pairs += Counter(tag_pairs)

    end=time.time()
    print("Third loop", end-start)
    start= time.time()

    nb_pairs = sum(tag_word_pairs.values())
    for i in range(0, len(tag_pairs)) :
        list_p_transition.append(math.log((tag_pairs_counter[i]+laplace)/(nb_pairs + laplace*len(tag_word_pairs))))

    end=time.time()
    print("Fourth loop", end-start)
    start= time.time()

    list_word_from_tag = []
    list_emission_word = []
    for i in range(0, len(tags)) :
         list_word_from_tag.append([])
         list_p_emission.append([])
         list_emission_word.append([])


    for sentence in train :
        for word in sentence :
            for i in range(0, len(tags)):
                if tags[i] == word[1] :
                    list_word_from_tag[i].append(word[0])

    for i in range(0, len(tags)) :
        list_counter_word.append(Counter(list_word_from_tag[i]))
        counter_length = len(list_counter_word[i])
        counter_tag = sum(list_counter_word[i].values())
        for counter in list_counter_word[i] :
            list_emission_word[i].append(counter)
            list_p_emission[i].append(math.log((list_counter_word[i][counter]+laplace)/(counter_tag+laplace*counter_length+1)))
    end=time.time()
    print("Last one", end-start)
    start= time.time()

    p_tag = []
    t_two = []

    list_word = []
    for j in range(0, len(list_emission_word)):
        for i in range(0, len(list_emission_word[j])) :
            list_word.append(list_emission_word[j][i])

    for sentence in test :
        print("sentence")
        for i in range(0, len(tags)) :
            p_tag.append([])
            t_two.append([])
            for j in range(0, len(sentence)) :
                p_tag[i].append(0)
                t_two[i].append(0)
            if sentence[0] in list_emission_word[i] :
                p_tag[i][0]=(list_p_initial[i]+list_p_emission[i][list_emission_word[i].index(sentence[0])])
            else :
                p_tag[i][0]=(list_p_initial[i])
        for j in range(1, len(sentence)) :
            for i in range(0, len(tags)):
                max_val = 0
                max_arg_val = None
                for k in range(0, len(tags)):
                    if sentence[j] in list_word :
                        val = p_tag[k][j-1]+list_p_emission[i][list_emission_word[i].index(sentence[0])]+list_p_transition[k][i]
                        if val > max_val :
                            max_val = val
                            max_arg_val = tags[k]
                p_tag[i][j] = max_val
                t_two[i][j] = max_arg_val

        proba_max = -float("inf")
        arg_proba_max = None
        for i in range(0, len(tags)) :
            if p_tag[i][-1] > proba_max :
                proba_max = p_tag[i][-1]
                arg_proba_max = tags[i]
        serie_tags = []
        serie_tags.append(arg_proba_max)
        for j in reversed(range(0, len(sentence))):
            serie_tags.insert(0, tags[t_two[tags.index(arg_proba_max)][j]])
            arg_proba_max = t_two[tags.index(arg_proba_max)][j]
        predicts.append(serie_tags)

    end = time.time()
    print("Dev", end-start)

    raise Exception("You must implement me")
    return predicts

def viterbi_p2(train, test):
    '''
    TODO: implement the optimized Viterbi algorithm. This function has time out limitation for 3 mins.
    input:  training data (list of sentences, with tags on the words)
            E.g. [[(word1, tag1), (word2, tag2)], [(word3, tag3), (word4, tag4)]]
            test data (list of sentences, no tags on the words)
            E.g [[word1,word2...]]
    output: list of sentences with tags on the words
            E.g. [[(word1, tag1), (word2, tag2)...], [(word1, tag1), (word2, tag2)...]...]
    '''


    predicts = []
    raise Exception("You must implement me")
    return predicts
