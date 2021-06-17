import nltk
from tkinter import *
import bs4 as bs
import urllib.request
import re
from collections import OrderedDict
nltk.download('punkt')

with open('culture2.txt',encoding="utf8") as f:
    lines = f.readlines()

article_text = ' '.join([str(item) for item in lines ]) #bt7ut kul items ely fl list(lines) fe string wa7ed w ma ben kul item in lines ' ' (space)
article_text = article_text.lower()
article_text = re.sub(r'[^\w\s]', ' ', article_text) #btshel kul lcharacters ly mesh digits aw _ aw letters arabic aw english aw white spaces
article_text = re.sub(r'[_ A-Za-z]', ' ', article_text) #btshel l _ w letters l english ...fa fel a5er betba2a arabic litters and digits only
#print(article_text)

words_tokens = []
words_tokens = nltk.word_tokenize(article_text)   # by7awel string to tokens kul kelma token


ngrams = {}
words = 2
prob_bigram = {}
# bnshof l 2 words geh ba3dohm eh mn lkalemat w bn7uthom f list
#ngrams hya dictionary l key = word1+word2 w l value list of w3 ly gom ba3d w1+w2
#  ngrams={تلعب فى" :['مدارس', 'أرض', 'أي'] }
for i in range(len(words_tokens) - words):
    seq = ' '.join(words_tokens[i:i + words])
    if seq not in ngrams.keys():
        ngrams[seq] = []
    ngrams[seq].append(words_tokens[i + words])


#prob_bigram dictionary feha key w1+w2 m value 3adad tekrarhom fel corpus han7tagha ba3den
# prob_bigram["تلعب في"] =3  for example
for i in range(len(words_tokens) - words):
    seq = ' '.join(words_tokens[i:i + words])
    #print(seq)
    if seq not in prob_bigram.keys():
        prob_bigram[seq] = 1
    else:
        prob_bigram[seq] = prob_bigram[seq] + 1


def num_repitation(str, arr):
    count = 0
    for i in range(len(arr)):
        if arr[i] == str:
            count += 1
    return count


probabilities = {}
repetations = {}
sorted_probabilities = {}

#repetations  dictionary key w1+w2+w3 , value 3adad tekrar w3 ba3d w1+w2
# probabilities dictionary  feha key w3 , value probability of w3 ba3d w1+w2
# parameter str de w1+w2
def Word_prediction(str):
    s = ""
    if str not in ngrams.keys():
        return []
    else:
        s = ngrams[str]
        for i in range(len(ngrams[str])):
            repetations[str + ' ' + s[i]] = num_repitation(ngrams[str][i], ngrams[str])
            pw1_w2_w3 = repetations[str + ' ' + s[i]]
            pw1_w2 = prob_bigram[str]
            probabilities[s[i]] = pw1_w2_w3 / pw1_w2   # probability of w3 ba3d w1+w2
        print(probabilities)
        sorted_probabilities = OrderedDict(sorted(probabilities.items(), key=lambda x: x[1], reverse=True)) # byrateb l dectionary according to values (descendingly)

        print(list(sorted_probabilities.keys()))
        return list(sorted_probabilities.keys()) #return  list of keis mtrateb mn high probability to low




#Word_prediction("السابقة مئات")


############################################  GUI part

root = Tk()
root.title("Sport")

def update(data):
    list_box_1.delete(0,END)  # delete ly fl list box
    if len(data)!=0:
        for item in data:
            list_box_1.insert(END, item)   # bezher kul l items ly f list data (ly rag3a mn function Word_prediction)
    else:
        list_box_1.insert(END, '')



def fillOut(event):
    #entry1.delete(0,END)

    entry1.insert(END,''+list_box_1.get(ACTIVE))

def check(e):
    typed = entry1.get() # l string ly user byda5alhom w1+w2
    print("typed" , typed)
    if typed == '':
        data = ''
    else:
        data =[]
        third_word = Word_prediction(typed) # third_word list of predected words
        print(third_word)
        for i in third_word:
            data.append(i)
    update(data)

label1 = Label(root,text= "Start Typing here " , font = ("Helvetica",14) ,fg="green")
label1.pack(pady = 20)
entry1 = Entry(root , font =  ("Helvetica",20))
entry1.pack()
list_box_1 = Listbox(root , width = 50)
list_box_1.pack(pady = 40)

entry1.bind("<KeyRelease>",check)
list_box_1.bind("<<ListboxSelect>>",fillOut)




root.mainloop()
