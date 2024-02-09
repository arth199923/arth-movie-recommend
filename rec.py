# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 17:55:38 2024

@author: Arth
"""

import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    #response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f0876dce92dd28505b9ec945cb32c688').format(movie_id)
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f0876dce92dd28505b9ec945cb32c688'.format(movie_id))

    data=response.json()    
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']
                




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    
    recommend_movies=[]
    recommened_movies_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        
        recommend_movies.append(movies.iloc[i[0]].title)
        recommened_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommened_movies_posters

        
        
movies_dict=pickle.load(open('D:/Alabs/TERM2.2_ML/ML case studies/movie_small/movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity=pickle.load(open('D:/Alabs/TERM2.2_ML/ML case studies/movie_small/similarity.pkl','rb'))



st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    movies['title'].values)


if st.button('Recommend'):
    names,posters=recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
            st.text(names[0])
            st.image(posters[0])
    with col2:
            st.text(names[1])
            st.image(posters[1])
    with col3:
            st.text(names[2])
            st.image(posters[2])
    with col4:
            st.text(names[3])
            st.image(posters[3])
    with col5:
            st.text(names[4])
            st.image(posters[4])
        
         
