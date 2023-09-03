import streamlit as st
import pickle
import pandas as pd
import requests

movies_list=pickle.load(open("movie_dict.pkl","rb"))
movies=pd.DataFrame(movies_list)
similarity=pickle.load(open("similarity.pkl","rb"))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response=requests.get(url)
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/"+data["poster_path"]


def recommend(movie):
    L=[]
    movie_index=movies[movies["title"]==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movie_poster=[]
    
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        L.append(movies.iloc[i[0]].title)

        recommend_movie_poster.append(fetch_poster(movie_id))
    return L,recommend_movie_poster


st.title("Movie Recommendation System")

select_movie_name=st.selectbox("Movie Name",movies["title"].values)

if st.button("Recommend"):
    names,posters=recommend(select_movie_name)
    
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader(names[0])
        st.image(posters[0],width=170)
    with col2:
        st.subheader(names[1])
        st.image(posters[1],width=170)
    with col3:
        st.subheader(names[2])
        st.image(posters[2],width=170)
    col4,col5=st.columns(2)
    with col4:
        st.subheader(names[3])
        st.image(posters[3],width=170)
    with col5:
        st.subheader(names[4])
        st.image(posters[4],width=170)