import nltk 
import spacy
import utility_word as noise
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim import corpora
import gensim
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('omw-1.4')
nltk.download('stopwords')
nlp = spacy.load('fr_core_news_md')

def get_top_n_words(corpus, n=10):
  vec = CountVectorizer(preprocessor=None,lowercase = False).fit(corpus)
  bag_of_words = vec.transform(corpus)
  sum_words = bag_of_words.sum(axis=0) 
  words_freq = [(word, sum_words[0, idx]) for word, idx in   vec.vocabulary_.items()]

  return words_freq # return a list of tuple

def parse_requirement(searched_word, lst_sentence, lst_date):
    lst_frequency = []
    word_searched = dict()
    it = 0
    dt = 0

    for i in range(len(lst_sentence)):
        sentence = tokenise_lemmentise(lst_sentence[i])
        lst_frequency.append(get_top_n_words(sentence, 20))
    for frequency in lst_frequency:
        date = lst_date[it]
        for ws in searched_word:
            if not ws in word_searched.keys():
                word_searched[ws] = []
            word_searched[ws].append((date, 0))
        for word, occ in frequency:
            if word in searched_word:
                word_searched[word][it] = (date, occ)
        it += 1

    return word_searched # return a dict with in key the date and with in the value a list of tuple 

def tokenise_lemmentise(sentence):
    nlp = spacy.load('fr_core_news_md')
    sentence = sentence.lower()
    tokeni = []
    token = nlp(sentence)
    stopw = nltk.corpus.stopwords.words('french')
    stopw.extend(noise.frenchNoiseWords)
    stopw.extend(noise.frenchVerbEtre)
    stopw.extend(noise.frenchVerbAvoir)

    for tkn in token:
        tokeni.append(tkn.lemma_)
    tokeni = [word for word in tokeni if len(word) > 2 ]
    tokeni = [wd for wd in tokeni if not wd in stopw]

    return tokeni # return a lst of token

def tokenise_lemmentise_topic(sentence):
    nlp = spacy.load('fr_core_news_md')
    sentence = sentence.lower()
    tokeni = []
    clean_txt = []
    token = nlp(sentence)
    stopw = nltk.corpus.stopwords.words('french')
    stopw.extend(noise.frenchNoiseWords)
    stopw.extend(noise.frenchVerbEtre)
    stopw.extend(noise.frenchVerbAvoir)

    for tkn in token:
        tokeni.append(tkn.lemma_)
    tokeni = [word for word in tokeni if len(word) > 2 ]
    clean_txt = [wd for wd in tokeni if not wd in stopw]

    return clean_txt # return a lst of token

def processWordFrequency(contribGroup, searched_word):
    ncontribGroup = dict()
    for da, con in contribGroup:
        if not da in ncontribGroup:
            ncontribGroup[da] = ""
        ncontribGroup[da] += "".join(con)
    date = [n for n in ncontribGroup]
    lst_sentence = [ncontribGroup[s] for s in ncontribGroup ]
    result = parse_requirement(searched_word, lst_sentence, date)
    return result, date # return a lst and a lst of date

def LDA_prep(lst):
    bag_word =  [lst]
    num_topic = 2
    dicti = corpora.Dictionary(bag_word)
    corpus = [dicti.doc2bow(txt) for txt in bag_word]

    pickle.dump(corpus, open('corpus.pkl', 'wb'))
    dicti.save('dictionary.gensim')
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topic, id2word=dicti, passes = 20)
    ldamodel.save('model10.gensim')
    topics = ldamodel.print_topics(num_words = 20)
    return ldamodel #return a type of gensim

def processTopicModelling(contribGroup):
    chunked_list = list()
    list_txt = []
    chunk_size = 230 # the size of element i want in each list
    for i in range(0, len(contribGroup), chunk_size):
        chunked_list.append(contribGroup[i:i+chunk_size])
    # separate the contib in a number of sub_list
    for chunked in chunked_list:
        list_txt.append("".join(chunked))
    result = []
    for sentence in list_txt:
        result.extend(tokenise_lemmentise(sentence))
    lda = LDA_prep(result)
    return lda.show_topic(0, 20) #return a lst of word in topic