for word in movie :
    index = train_set.index(movie)
    nb_words+=1
    #print("je regarde le word")
    if word in words_list :
        #word déjà dans words_list -> prendre son index
        if train_labels[index] == 1 :
             #le mot est classé positif ici :
             for i in words_list :
                 if i == word :
                    words_pos[words_list.index(i)]+=1
                    nb_pos+=1
                    #print("blocked 1")
                    #print(i)
        else :
            #le mot est classé négatif ici :
            for i in words_list :
                if i == word :
                    words_neg[words_list.index(i)]+=1
                    nb_neg+=1
                    #print("blocked 2")
                    #print(i)
    else :
        words_list.append(word)
        #mot pas dans la world_list :
        if train_labels[index] == 1 :
             #le mot est classé positif ici :
             words_pos.append(1)
             words_neg.append(0)
             nb_pos+=1
             #print("blocked 3")
             #print(word)
        else :
            #le mot est classé négatif ici :
            words_neg.append(1)
            words_pos.append(0)
            nb_neg+=1
            #print("blocked 4")
            #print(word)

prob_pos = nb_pos/nb_words
prob_neg = nb_neg/nb_words

words_prob_pos = [] #liste avec toutes les probabilités que les mots soient dans une review positif
words_prob_neg = [] #idem negative, celui qu'on devra multiplier
for word in words_list :
i = word_list.index(word)
# Bayesian way, not complete
#prob_pos = (words_pos[i]/(words_pos[i]+words_neg[i]))/((words_pos[i]/(words_pos[i]+words_neg[i])) + )
#direct way :
words_prob_pos.append(words_pos(i)/nb_pos)
words_prob_neg.append(words_pos(i)/nb_neg)

#Fini de train, maintenant on construit les results


        #proba_pos *= (words_pos(words_list.index(word))+k)/(size + k * len(words_list))
        #proba_neg *= (words_pos(words_list.index(word))+k)/(size + k * len(words_list))
        #proba_pos = log(proba_pos * words_prob_pos[words_list.index(train)])
        #proba_neg = log(proba_neg * words_prob_neg[words_list.index(train)])
