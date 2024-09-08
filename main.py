import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
text = open('input.txt' , encoding='utf-8').read()
print("input file:  " + text)
## print(string.punctuation)
lt = text.lower()
print("lower case text file:  " + lt)
clean_text = lt.translate(str.maketrans(' ', ' ',string.punctuation))
print("clean text file:  " + clean_text)
#tokenize_text = clean_text.split()
tokenize_text = word_tokenize(clean_text , "english" , )
print("Tokenize text:")
print(tokenize_text)
#stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
  #            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
   #           "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
  #            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
   #           "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
   #           "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
   ##          "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
   #           "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

final_words = [ ]
for word in tokenize_text:
    #if word not in stop_words:
    if word not in stopwords.words('english'):
        final_words.append(word)
print("Final words:")
print(final_words)
# NLP Emotion Algorithm
# 1) Check if the word in the final word list is also present in emotion.txt
#  - open the emotion file
#  - Loop through each line and clear it
#  - Extract the word and emotion using split

# 2) If word is present -> Add the emotion to emotion_list
# 3) Finally count each emotion in the emotion list
emotion_list = [ ]
with open('emotions.txt' , 'r') as file:
    for line in file:
        clear_line = line.replace("\n","").replace(",","").replace("'","").strip()
        ## replace new line comma or single comma ko or strip aage ke space ko htane ke kam aata h
        ##print(clear_line)
        word , emotion = clear_line.split(":")
        ##emotions list me : esse phle ke naam word me store honge or aage ke emotion me
        #print("Word:" + word ,"  " ,"Emotion:" + emotion)
        if word in final_words:
            emotion_list.append(emotion)
print("Emotions List")
print(emotion_list)
w = Counter(emotion_list)
print(w)
def sentimental_analyse(sentiment_text):
    score= SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    print(score)
    neg = score['neg']
    pos = score['pos']
    if neg > pos:
        print("Negative Sentiment")
    elif pos > neg:
        print("Positive Sentiment")
    else:
        print("Neutral Vibe")
sentimental_analyse(clean_text)

fig , ax1 = plt.subplots()
fig.autofmt_xdate()
ax1.bar(w.keys(),w.values())
plt.savefig('graph.png')
plt.show()