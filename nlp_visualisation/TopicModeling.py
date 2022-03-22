from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from turtle import pos
import nltk 
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
from nltk.corpus import wordnet 
from nltk.corpus import stopwords
import pandas as pd

sentence = 'Mme Christine Albanel, ministre. Je suis tr\u00e8s attach\u00e9e \u00e0 la r\u00e9mun\u00e9ration pour copie priv\u00e9e, qui est effectivement une source essentielle de revenus pour les artistes et le financement de la cr\u00e9ation dans son ensemble. Il s\u2019agit d\u2019ailleurs d\u2019un dispositif de plus en plus \u00e9tendu, qui s\u2019applique dans vingt et un\u00a0pays de l\u2019Union europ\u00e9enne. Pour autant, la d\u00e9termination de l\u2019assiette de cette r\u00e9mun\u00e9ration soul\u00e8ve des questions tr\u00e8s complexes, comme en t\u00e9moigne la r\u00e9cente annulation contentieuse d\u2019une des d\u00e9cisions de la Commission de la copie priv\u00e9e, charg\u00e9e de d\u00e9limiter une telle assiette et de fixer les taux qui lui sont applicables. Par ailleurs, dans le cadre du plan\u00a0Num\u00e9rique\u00a02012, les modalit\u00e9s du fonctionnement de cette commission sont sur le point d\u2019\u00e9voluer. Monsieur\u00a0Lagauche, j\u2019ai bien conscience que votre proposition est motiv\u00e9e par le souci de mieux r\u00e9mun\u00e9rer les artistes. Cependant, le Gouvernement ne peut pas \u00eatre favorable \u00e0 la cr\u00e9ation d\u2019une nouvelle modalit\u00e9 de calcul, en l\u2019occurrence proportionnelle, sans qu\u2019il ait pu \u00eatre proc\u00e9d\u00e9 au pr\u00e9alable \u00e0 une large concertation aupr\u00e8s des repr\u00e9sentants des ayants droit, des industriels assujettis et des consommateurs. Pour ces raisons, le Gouvernement \u00e9met un avis d\u00e9favorable sur cet amendement.M. Serge Lagauche. Cet amendement a pour objet d\u2019adapter le code de la propri\u00e9t\u00e9 intellectuelle afin de permettre aux nouveaux modes d\u2019enregistrements d\u00e9mat\u00e9rialis\u00e9s de contribuer \u00e0 la r\u00e9mun\u00e9ration des ayants droit dans le cadre de la copie priv\u00e9e. Je rappellerai rapidement le contexte qui nous incite \u00e0 vouloir l\u00e9gif\u00e9rer dans ce sens. Depuis pr\u00e8s de six\u00a0mois, sont apparus en France, comme d\u2019ailleurs dans quelques autres pays europ\u00e9ens, des services de magn\u00e9toscopes d\u00e9mat\u00e9rialis\u00e9s qui permettent, via internet, d\u2019enregistrer les programmes de t\u00e9l\u00e9vision, et ce en reproduisant exactement le m\u00eame sch\u00e9ma de fonctionnement que les magn\u00e9toscopes traditionnels, avec, notamment, la n\u00e9cessit\u00e9 d\u2019anticiper le d\u00e9but de la diffusion du programme pour transmettre l\u2019ordre d\u2019enregistrement. L\u2019enregistrement n\u2019est r\u00e9cup\u00e9rable, bien s\u00fbr, qu\u2019une fois r\u00e9alis\u00e9, c\u2019est-\u00e0-dire apr\u00e8s la diffusion du programme, via un acc\u00e8s personnalis\u00e9 et non public. Nous nous situons donc ici, non pas dans le cadre de la vid\u00e9o \u00e0 la demande, la VOD, ni m\u00eame dans celui de la \u00ab\u00a0t\u00e9l\u00e9vision de rattrapage\u00a0\u00bb, mais bien dans celui du magn\u00e9toscope tel qu\u2019il existe depuis le d\u00e9but des ann\u00e9es\u00a0soixante-dix. Or ce dernier, lui aussi, \u00e9volue. De m\u00eame que la VOD constitue l\u2019\u00e9volution d\u00e9mat\u00e9rialis\u00e9e naturelle des vid\u00e9os clubs, l\u2019enregistrement \u00e0 la demande constitue l\u2019\u00e9volution naturelle du magn\u00e9toscope dans l\u2019environnement num\u00e9rique d\u2019aujourd\u2019hui, environnement marqu\u00e9 par la d\u00e9mat\u00e9rialisation via le Net, avec, par exemple, de plus en plus d\u2019applications distantes, mais aussi du stockage de donn\u00e9es distant. \u00c0 notre sens, ces services doivent aussi contribuer \u00e0 la r\u00e9mun\u00e9ration de la copie priv\u00e9e. Il ne s\u2019agit aucunement de modifier le champ de l\u2019exception au droit d\u2019auteur qu\u2019est la copie priv\u00e9e, d\u00e9finie par le 2\u00b0 de l\u2019article\u00a0L.\u00a0122-5 du code de la propri\u00e9t\u00e9 intellectuelle, qui, d\u2019ailleurs, n\u2019exclut pas les copies num\u00e9riques provenant d\u2019actes d\u00e9mat\u00e9rialis\u00e9s. Il s\u2019agit simplement d\u2019adapter les modalit\u00e9s de r\u00e9mun\u00e9ration, qui ne sont jusqu\u2019\u00e0 pr\u00e9sent que forfaitaires puisqu\u2019elles ne s\u2019appliquent qu\u2019\u00e0 des supports physiques d\u2019enregistrement. Nous vous proposons donc de permettre la prise en compte de la d\u00e9mat\u00e9rialisation de l\u2019acte physique de copie, qui, parce qu\u2019elle permet de savoir tr\u00e8s pr\u00e9cis\u00e9ment ce qui est copi\u00e9, offre en outre la possibilit\u00e9 d\u2019\u00e9tablir une r\u00e9mun\u00e9ration proportionnelle, principe de base du droit d\u2019auteur. Enfin, soucieux de respecter l\u2019esprit de la loi, nous estimons n\u00e9cessaire, comme dans le cadre de la r\u00e9mun\u00e9ration forfaitaire, de laisser \u00e0 la Commission de la copie priv\u00e9e la responsabilit\u00e9 de fixer, sur la base d\u2019\u00e9l\u00e9ments objectifs et contr\u00f4l\u00e9s fournis par les \u00e9diteurs de services de magn\u00e9toscopes en ligne, le montant de cette r\u00e9mun\u00e9ration proportionnelle. Le projet de loi a pour ambition de lutter contre le piratage et de cr\u00e9er le cadre juridique indispensable au d\u00e9veloppement des offres l\u00e9gales. Les nouveaux services de magn\u00e9toscopes num\u00e9riques y contribuent tr\u00e8s concr\u00e8tement et permettent de conforter la copie priv\u00e9e, \u00e0 laquelle nous tenons tous, dans un nouvel environnement num\u00e9rique susceptible de lui apporter de nouveaux revenus, importants et p\u00e9rennes. Mes chers coll\u00e8gues, les propositions concr\u00e8tes, permettant de satisfaire les nouveaux usages des internautes tout en apportant, dans un cadre juridique pr\u00e9existant, des revenus compl\u00e9mentaires aux ayants droit, ne sont pas si nombreuses, raison de plus pour adopter notre amendement\u00a0!'

def pos_tagger(nltk_tag): 
    if nltk_tag.startswith('J'): 
        return wordnet.ADJ 
    elif nltk_tag.startswith('V'): 
        return wordnet.VERB 
    elif nltk_tag.startswith('N'): 
        return wordnet.NOUN 
    elif nltk_tag.startswith('R'): 
        return wordnet.ADV 
    else:           
        return None

def frequence_nlp(sentence):
    char_spec = ["!", '"', "#", "%", "&", "'", "(", ")", "*", "+",
                 ",", "-", ".", "/", ":", ";", "<", ">", "=", "?",
                 "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}",
                 "~", "-"]
    sentence = sentence.lower()
    lemmatizer = WordNetLemmatizer() 

#    for char in char_spec:
#        sentence = sentence.replace(char, ' ')

    tokeni = nltk.word_tokenize(sentence)
    stopWords = set(stopwords.words('french'))
    clean_text = []

    for token in tokeni:
        if token not in stopWords:
            clean_text.append(token)
    print(clean_text)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    pos_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))     
    print(pos_tagged) 
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    wordnet_tagged = list(map(lambda x: (x[0], pos_tagger(x[1])), pos_tagged)) 
    print(wordnet_tagged) 
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    lemmatized_sentence = [] 
    for word, tag in wordnet_tagged: 
        if tag == "n": 
            print(word)
            lemmatized_sentence.append(word)
#    lemmatized_sentence = " ".join(lemmatized_sentence) 
    print(lemmatized_sentence)
#    for token in tokeni:
#        if token not in stopWords:
#            clean_text.append(token)

#    print(clean_text)
    return clean_text

frequence_nlp(sentence)

#vectorizer = TfidfVectorizer(
#  max_features=5000, 
#  stop_words="english", 
#  max_df=0.95, 
#  min_df=2)
#text = ["The sky is blue with clouds. but the water is blue too."]
#vectorizer.fit(text)
#vocab_itos = vectorizer.get_feature_names_out()
#vocab_stoi = vectorizer.vocabulary_
#vectors = vectorizer.transform(text)
#print(vectors.shape)
#print(type(vectors))
#print(vectors.toarray())