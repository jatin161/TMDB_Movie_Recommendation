import pandas as pd
import ast
import pickle
import bz2
#getting Movie Details
movie=pd.read_csv(r"tmdb_5000_movies.csv")
credits=pd.read_csv(r"tmdb_5000_credits.csv")
df=movie.merge(credits,how='left',right_on='movie_id',left_on='id')
#Selecting Useful Data
df=df[['genres','movie_id','keywords','overview',"title_x",'cast','crew']]


#Data Cleaning
def call(text):
    lis = []
    text = ast.literal_eval(text)
    for i in text:
        lis.append(i['name'])

    return lis
df['genres'] = [call(i) for i in df['genres']]

df['keywords']=[call(i) for i in df['keywords']]

def call3(text):
    a=0
    lis=[]
    text=ast.literal_eval(text)
    for i in text:
        if(a!=3):
            lis.append(i['name'])
            a=a+1
        else:
            break
    return lis

df['cast']=[call3(i) for i in df['cast']]

def call2(text):
    a=0
    lis=[]
    text=ast.literal_eval(text)
    for i in text:
        if((i['job']=='Director' or i['job']=='Writer')):
            lis.append(i['name'])
    return lis

df['crew']=[call2(i) for i in df['crew']]

df['cast']=df['cast'].apply(lambda x:[i.replace(" ","") for i in x])
df['movie_name']=df['title_x']
df['keywords']=df['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
df['genres']=df['genres'].apply(lambda x:[i.replace(" ","") for i in x])
df['crew']=df['crew'].apply(lambda x:[i.replace(" ","") for i in x])
data_df=df

def call(text):
    lis=[]
    lis.append(text)
    return lis
df['movie_name']=df['movie_name'].apply(call)

df['Tags']=df['cast']+df['keywords']+df['genres']+df['crew']+df['movie_name']
df=df[['movie_id','title_x','Tags']]

df['Tags']=df['Tags'].apply(lambda x:" ".join(x))
#Recomendation Algo
from nltk.stem import PorterStemmer

ps = PorterStemmer()


def stemming(text):
    lis = []
    for w in text.split(" "):
        rootWord = ps.stem(w)
        lis.append(rootWord)

    return " ".join(lis)


df['Tags'] = df['Tags'].apply(stemming)

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
cv = CountVectorizer(max_features = 5000, stop_words = 'english')
cv.fit_transform(df['Tags'])
skl_output = cv.transform(df['Tags']).toarray()

similarity=cosine_similarity(skl_output)

def recommended(movie):
    index=df[df['title_x']==movie].index[0]
    distance=sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x:x[1])
    for i in distance[1:6]:
        print(df.loc[i[0]]['title_x'])
#check Output
recommended("Captain America: Civil War")


#System is working fine now export simmilarty using pickle
pickle.dump(df.to_dict(),open("df_final.pkl",'wb'))
# pickle.dump(similarity,open("similarity.pkl",'wb'))

ofile = bz2.BZ2File("similarity",'wb')
pickle.dump(similarity,ofile)
ofile.close()