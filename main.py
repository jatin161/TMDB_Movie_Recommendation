import pandas as pd
import streamlit as st
import pickle
import requests
import json
import bz2

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return 1

def recommended(movie):
    index = movies[movies['title_x'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    liss = []
    list1 = []
    count=0
    for i in distance[1:]:
        if(count>7):
            break
        elif(fetch_poster(movies.loc[i[0]]['movie_id'])==1):
            pass
        else:
            liss.append(movies.loc[i[0]]['title_x'])
            list1.append(fetch_poster(movies.loc[i[0]]['movie_id']))
            count=count+1
    return liss, list1




movies_list = pickle.load(open('df_final.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
movies_list = movies['title_x'].values

ifile = bz2.BZ2File("similarity",'rb')
similarity = pickle.load(ifile)

# similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")
st.write(
    """
    <div style="margin-align:center;">
    <H3>Steps To use</H3>
    1) Select Any sample Movie from the Drop Down Menu <br>
    2) Click on the Show Recommendation Button at the bottom.<br>
    <br>
    </div>
    """,
    unsafe_allow_html=True,
)

option = st.selectbox('TMDB Movie List', movies_list)

if st.button('Show Recommendation'):
    st.write(
        """
        <div style="margin-align:center;">
        <H3>Mentioned Below are Recommended Movies :</H3>
        """,
        unsafe_allow_html=True,
    )
    recommended_movie_names, recommended_movie_posters = recommended(option)
    col1, col2 = st.columns([5, 5])
    with col1:
        st.markdown(
        """
        <style>
        img {
            float: left;
            height: 200px;
        }        
        </style>
        """,
        unsafe_allow_html=True,
             )
        st.image(recommended_movie_posters[0], width=200,caption=recommended_movie_names[0])
    with col2:

        st.markdown(
        """
        <style>
        img {
            float: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        st.image(recommended_movie_posters[1], width=200,caption=recommended_movie_names[1])

    col1, col2 = st.columns([5, 5])
    with col1:
        st.markdown(
        """
        <style>
        img {
            float: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        st.image(recommended_movie_posters[2], width=200,caption=recommended_movie_names[2])
    with col2:
        st.markdown(
        """
        <style>
        img {
            float: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        st.image(recommended_movie_posters[3], width=200,caption=recommended_movie_names[3])
    col1, col2 = st.columns([5, 5])
    with col1:
        st.markdown(
        """
        <style>
        img {
            float: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        st.image(recommended_movie_posters[4], width=200,caption=recommended_movie_names[4])
    with col2:
        st.markdown(
        """
        <style>
        img {
            float: left;
        }
        </style>
        """,
        unsafe_allow_html=True,
        )
        st.image(recommended_movie_posters[5], width=200,caption=recommended_movie_names[5])

















    #
    # col1, col2, col3, col4, col5 = st.columns(5)
    # with col1:
    #     st.text()
    #     st.image()
    # with col2:
    #     st.text(recommended_movie_names[1])
    #     st.image(recommended_movie_posters[1])
    #
    # with col3:
    #     st.text(recommended_movie_names[2])
    #     st.image(recommended_movie_posters[2])
    # with col4:
    #     st.text(recommended_movie_names[3])
    #     st.image(recommended_movie_posters[3])
    # with col5:
    #     st.text(recommended_movie_names[4])
    #     st.image(recommended_movie_posters[4])