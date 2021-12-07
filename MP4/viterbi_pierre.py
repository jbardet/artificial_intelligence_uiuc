"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""
import collections

import time

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
    # Train
    cnt = {}
    mostTagged = {}
    for sentence in train:
        for word, tag in sentence:
            try:
                cnt[(word,tag)] += 1
            except KeyError:
                cnt[(word,tag)] = 1
            try:
                mostTagged[tag] += 1
            except KeyError:
                mostTagged[tag] =1

    # CNT is a dict for the number of apparitions for each pair (word, tag)

    tags = {}
    best = {}
    for w, tag in cnt:
        if w in best:
            if cnt[(w, tag)] > best[w]:
                tags[w] = tag
                best[w] = cnt[(w, tag)]
        else:
            best[w] = cnt[(w, tag)]
            tags[w] = tag

    overallMax = 0
    for elem in mostTagged:
        if overallMax <= mostTagged[elem]:
            overallMax = mostTagged[elem]
            universal = elem

    # Generate predictions for test set
    predicts = []
    idx=0
    start= time.time()
    for sen in test:
        predicts.append([])
        for w in sen:
            try:
                predicts[idx].append((w, tags[w]))
            except KeyError:
                predicts[idx].append((w, universal))
        idx += 1
    end = time.time()
    #print("Time for for list in test is {}".format(end-start))
    #print(universal)
    #raise Exception("You must implement me")
    return predicts

def comp_init_proba(tag, cnt_init, k_smooth, summation_init_proba, num_tags):
    denom = cnt_init[tag] + k_smooth

    num = summation_init_proba + k_smooth * num_tags

    return denom / num

def comp_transition_proba(prev_tag, curr_tag, cnt_tag_pairs, cnt_tags, k_smooth, num_tags):
    try:
        return (cnt_tag_pairs[(prev_tag, curr_tag)] + k_smooth) / (cnt_tags[prev_tag] + k_smooth * num_tags)
    except KeyError:
        return k_smooth / (cnt_tags[prev_tag] + k_smooth * num_tags)

def comp_emission_proba(count_word_tag, word, tag, k_smooth, count_tag, vocab_size):
    try:
        return (count_word_tag[(word, tag)] + k_smooth) / (count_tag[tag] + k_smooth * (vocab_size+1))
    except KeyError:
        return k_smooth / (count_tag[tag] + k_smooth * (vocab_size+1))

# Inspired of wikipedia of Viterbi Algorithm : https://en.wikipedia.org/wiki/Viterbi_algorithm
def core_viterbi(obs, states, init_proba, transmission_proba, emission_proba, count_tag, k, vocab_size):
    viterbi = [{}]
    for state in states:
        try:
            viterbi[0][state] = {"proba": init_proba[state] * emission_proba[(obs[0], state)], "prev": None}
        except KeyError:
            viterbi[0][state] = {"proba": init_proba[state] * k / (count_tag[state] + k * (vocab_size+1)), "prev": None}
        '''
        except KeyError:
            viterbi[0][state]["proba"] = 0
        viterbi[0][state]["prev"] = None
        '''
    for t, curr_word in enumerate(obs, 1):
        viterbi.append({})

        for state in states:
            maxViterbi = 0
            best_prev_state = state
            for prev_state in states:
                multiply = viterbi[t-1][state]["proba"] * transmission_proba[(prev_state, state)]
                if maxViterbi < multiply:
                    maxViterbi = multiply
                    best_prev_state = prev_state
            try:
                maxViterbi *= emission_proba[(curr_word, state)]
            except KeyError:
                maxViterbi *= k / (count_tag[state] + k * (vocab_size+1))

            viterbi[t][state] = {"proba": maxViterbi, "prev": best_prev_state}


    return viterbi

def backtrack(viterbi):
    optimal_path = []
    optimal_proba = 0.0
    prev = None
    best_state = viterbi[-1].items()[x]
    for state, val in viterbi[-1].items():
        if val["proba"] > optimal_proba:
            optimal_proba = val["proba"]
            best_state = state
    optimal_path.append(best_state)
    prev = best_state

    for t in range(len(viterbi)-2, -1, -1):
        optimal_path.insert(0, viterbi[t+1][prev]["prev"])
        prev = viterbi[t+1][prev]["prev"]

    return optimal_path





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

    k_smooth = 0.1

    # Count occurences of tags, tag pairs, tag/word pairs
    cnt_init = {}
    cnt_tags = {}
    cnt_tag_pairs = {}
    cnt_w_t = {}
    cnt_words = {}
    for sentence in train:
        (init_w, init_tag) = sentence[0]
        try:
            cnt_init[init_tag] += 1
        except KeyError:
            cnt_init[init_tag] = 1

        for i, (word, tag) in enumerate(sentence):
            (word, tag) = sentence[i]
            # Count the tags
            try:
                cnt_tags[tag] += 1
            except KeyError:
                cnt_tags[tag] = 1

            # Count the tag pairs (current tag preceding the next tag)
            if i < len(sentence)-1:
                (next_word, next_tag) = sentence[i+1]
            try:
                cnt_tag_pairs[(tag, next_tag)] += 1
            except:
                cnt_tag_pairs[(tag, next_tag)] = 1

            # Count the word / tag pairs
            try:
                cnt_w_t[(word,tag)] += 1
            except KeyError:
                cnt_w_t[(word,tag)] = 1

            # Count the words (eg to obtain vocab_size)
            try:
                cnt_words[word] += 1
            except KeyError:
                cnt_words[word] = 1

    num_tags = len(cnt_tags)
    vocab_size = len(cnt_words)

    #Computer smoothed proba
    init_proba = {}
    trans_proba = {}
    emission_proba = {}

    # Initialization
    summation_init_proba = sum(cnt_init.values())
    for tag in cnt_tags:
        init_proba[tag] = comp_init_proba(tag, cnt_init, k_smooth, summation_init_proba, num_tags)

    # Transition
    for prev_tag in cnt_tags:
        for curr_tag in cnt_tags:
            trans_proba[(prev_tag, curr_tag)] = comp_transition_proba(prev_tag, curr_tag, cnt_tag_pairs, cnt_tags, k_smooth, num_tags)

    # Emission
    for word in cnt_words:
        for tag in cnt_tags:
            emission_proba[(word, tag)] = comp_emission_proba(cnt_w_t, word, tag, k_smooth, cnt_tags, vocab_size)


    # Take log of each proba


    # Construct the trellis
    # Return the best path through the trellis
    predicts = []
    for sentence in test:
        viterbi = core_viterbi(sentence, cnt_tags, init_proba, trans_proba, emission_proba, cnt_tags, k_smooth, vocab_size)
        predicts.append(backtrack(viterbi))



    #raise Exception("You must implement me")
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
