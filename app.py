import streamlit as st
import pickle
import pandas as pd
import requests

# def fetch_poster(movie_id):
#     # response=requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=042cf89b8d8bb1eb8ba0444b374785b3&language=en-US')
#     headers = {
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNDJjZjg5YjhkOGJiMWViOGJhMDQ0NGIzNzQ3ODViMyIsIm5iZiI6MTc2MjU4ODE0Mi4zMTYsInN1YiI6IjY5MGVmNWVlYzVjNWZhZmYzYWEwYzAwOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z95rZgb9cVkZjYber-grI-Gz3wJnwWSbzySQV3Gf1Gw",
#         "accept": "application/json",
#         "User-Agent": "Mozilla/5.0"
#     }
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
#     response = requests.get(url, headers=headers)

#     data=response.json()
#     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwNDJjZjg5YjhkOGJiMWViOGJhMDQ0NGIzNzQ3ODViMyIsIm5iZiI6MTc2MjU4ODE0Mi4zMTYsInN1YiI6IjY5MGVmNWVlYzVjNWZhZmYzYWEwYzAwOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z95rZgb9cVkZjYber-grI-Gz3wJnwWSbzySQV3Gf1Gw",
        "accept": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    # url = f"https://api.themoviedb.org/3/search/movie?query={movie_title}&language=en-US"


    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500"

    except Exception as e:
        print("Error fetching poster:", e)
        return "https://via.placeholder.com/500"



movies=pickle.load(open('movies.pkl', 'rb'))
movies_list=movies['title'].values

similarity=pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    indx=movies[movies['title']==movie].index[0]
    distances=similarity[indx]
    
    movies_lst=sorted(list(enumerate(distances)),key=lambda x:x[1],reverse=True)[1:6]
    recommended_movies_posters=[]
    recommended_movies=[]
    for i in movies_lst:
        movies_id=movies.iloc[i[0]].id
        #Fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies_id))
        # recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].title))

        recommended_movies.append(movies.iloc[i[0]].title)
    
    # movies_indx=[i[0] for i in movies_lst]

    return recommended_movies, recommended_movies_posters


st.title("Movie Recommendation System")

selected_movie_name=st.selectbox(
    'Select a movie you like:',
    movies_list,
    index=None
)

if st.button('Show Recommendation'):
    st.header("Recommendations for you:")

    names,posters = recommend(selected_movie_name)
    # for r in names:
    #     st.write(r)
    col1, col2, col3, col4, col5 = st.columns(5)
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


    st.subheader(f"You selected: **{selected_movie_name}**")


