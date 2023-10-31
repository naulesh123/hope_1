import numpy as np
import pandas
import pandas as pd
import streamlit as st




movies=pd.DataFrame(pd.read_csv("tmdb_5000_movies.csv"))
credit=pd.DataFrame(pd.read_csv("tmdb_5000_credits.csv"))


movies=movies.merge(credit,on="title")


movies=movies[['movie_id','title','overview','genres','keywords','cast','crew']]

# print(movies)
movies.dropna(inplace=True)


import json


def convert_keyword(x):
    str_to_list=json.loads(x)
    keyword_name = []
    for i in str_to_list:
        keyword_name.append(i["name"])

    return keyword_name

    pass

def convert(x):
    str_to_list=json.loads(x)
    genre_name=[]
    for i in str_to_list:
        genre_name.append(i["name"])

    return genre_name


    pass

movies['genres']=movies['genres'].apply(lambda x:convert(x))
movies['keywords']=movies['keywords'].apply(lambda x:convert_keyword(x))


director_name=""
def convert_director(x):

    x=json.loads(x)

    for i in x:
        if i["job"]=='Director':
            global director_name
            director_name=i["name"]

        pass
    return director_name
    pass




movies['crew']=movies['crew'].apply(lambda x:convert_director(x))
# print(movies['crew'])



# print(movies['keywords'])

# print(type(movies['crew']))


###################### cast ##########################

def cast(x):
    list_of_celebs=[]
    x=json.loads(x)
    count=1
    for i in x:
        if count<=3:

            list_of_celebs.append(i["name"])
            count+=1


    # for i in list_of_celebs:
    #     i=i.replace(" ","")
    #
    #     pass

    return list_of_celebs



    pass


def split_overview(x):
    # for i in x:
    x=x.split(" ")
    return x

    pass

######################################################


movies['cast']=movies['cast'].apply(lambda x:cast(x))
movies['cast']=movies['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies['crew']=movies['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies['overview']=movies['overview'].apply(lambda x:split_overview(x))
movies['tags']=movies['overview']+movies['genres']+movies['cast']+movies['keywords']+movies['crew']
# print(movies['tags'])


movies['tags']=movies['tags'].apply(lambda x:" ".join(x))
movies['tags']=movies['tags'].apply(lambda x:x.lower())
# print(movies['tags'])



new_df=movies[['movie_id','title','tags']]

# print(new_df)

from nltk.stem.porter import PorterStemmer
ps=PorterStemmer()

def stemming(x):
    y = x.split()
    return " ".join(ps.stem(i) for i in y)


    pass



movies['tags']=movies['tags'].apply(lambda x:stemming(x))



###############################################################################
###############################################################################
import streamlit as st

# Create a form
user_input = st.text_input("Enter users tag")


# print("required_list",list_of_all_movies)


option = st.selectbox("Select an option", movies['title'].values)
# Process user input

col1,col2=st.columns(2,gap="small")

movies_tobe_shown=[]

with col1:
    if st.button("recommend by tag"):

        if user_input=="":
            st.write("Enter the tag first")
        else:
            # st.write(user_input)

            temp_movie_list=movies['tags'].values
            temp_movie_list=np.append(temp_movie_list,user_input)
            # st.write(temp_movie_list,type(temp_movie_list))

            from sklearn.feature_extraction.text import CountVectorizer
            cv = CountVectorizer(max_features=5000, stop_words='english')
            vector = cv.fit_transform(temp_movie_list).toarray()


            from sklearn.metrics.pairwise import cosine_similarity
            similarity = cosine_similarity(vector)
            similarity=similarity[4806,:]
            similarity=sorted(list(enumerate(similarity)), reverse=True, key=lambda x: x[1])
            # st.write(similarity)

            counter=1
            for i in similarity:
                if i[1]!=0 and counter!=6 and i[1]!=1:
                    movies_tobe_shown.append(movies.loc[i[0],'movie_id'])
                    counter+=1


                pass

            pass

        pass


with col2:
    if st.button("recommend by options"):
        from sklearn.feature_extraction.text import CountVectorizer

        cv = CountVectorizer(max_features=5000, stop_words='english')
        vector = cv.fit_transform(new_df['tags']).toarray()

        # print("new_df type",(new_df['tags']))

        # print(vector)

        from sklearn.metrics.pairwise import cosine_similarity

        similarity = cosine_similarity(vector)

        list_enum=list(enumerate(movies['title'].values))

        for i in list_enum:
            if i[1]==option:

                # st.write(i[0],i[1])

                similarity_list=similarity[i[0]]

                similarity_list = sorted(list(enumerate(similarity_list)), reverse=True, key=lambda x: x[1])
                # st.write(similarity_list)
                counter=1
                for i in similarity_list:
                    if counter!=6:
                        movies_tobe_shown.append(movies.loc[i[0],'movie_id'])
                        counter+=1
                    pass
                # st.write(movies_tobe_shown)
                pass

        pass

# st.write(movies_tobe_shown)
import requests
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

list_of_poster=[]
for i in movies_tobe_shown:
    list_of_poster.append(fetch_poster(i))


    pass




##############################################################################
##############################################################################


col21,col22,col23,col24,col25=st.columns(5,gap="small")

with col21:
    if list_of_poster:
        st.image(list_of_poster[0])
    else:
        pass

    pass

with col22:
    if list_of_poster:
        st.image(list_of_poster[1])
    else:
       pass
    pass

with col23:
    if list_of_poster:
        st.image(list_of_poster[2])
    else:
        pass

    pass


with col24:
    if list_of_poster:
        st.image(list_of_poster[3])
    else:
        pass
    pass


with col25:
    if list_of_poster:
        st.image(list_of_poster[4])
    else:
        pass
    pass








##############################################################################
##############################################################################

# from sklearn.feature_extraction.text import CountVectorizer
#
# cv=CountVectorizer(max_features=5000,stop_words='english')
# vector=cv.fit_transform(new_df['tags']).toarray()
#
# # print("new_df type",(new_df['tags']))
#
# # print(vector)
#
# from sklearn.metrics.pairwise import cosine_similarity
#
# similarity=cosine_similarity(vector)



# print(similarity)



# # distances=similarity[0]
#
# # print(list(enumerate(distances)))
# def recom(str):
#     list_of_movie_index = []
#     for i in range(len(movies['title'])):
#
#         if (new_df.loc[i, 'title'] == str):
#             distances = similarity[i]
#             movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
#             # print("huge",movies_list)
#             counter = 0
#             for i in movies_list:
#                 if counter != 5:
#                     list_of_movie_index.append(i[0])
#                     counter += 1
#             break
#     list_of_movie_recom = []
#     for i in list_of_movie_index:
#         list_of_movie_recom.append(new_df.loc[i, 'title'])
#
#     return list_of_movie_recom
#
#     pass
#
#
# recom_list=recom('Batman Begins')
#
#
#
#
# print(recom_list)



# list_enum=list(enumerate(movies['title'].values))
# print("list_enum",list_enum)










