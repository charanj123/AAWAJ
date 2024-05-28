import streamlit as st
import pandas as pd
#import database
#import register
from streamlit_extras.switch_page_button import switch_page
#from register import registeruser
from streamlit_option_menu import option_menu
from video import videos, uploadvideos
import home as dashboard
import psycopg2
import home

# establishing the connection
#import mysql.connector
import mysql.connector

conn = psycopg2.connect(database="awaj", user="postgres", password="admin", host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute("SELECT * FROM Users")
dataset = cur.fetchall()

for data in dataset:
    print(data)



def login():
        # Check if the user is logged in
        if st.session_state.get('logged_in') is None:
            # Display the login form
            st.title('Login')
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')

            if st.button('Login'):
                # Check if the user exists in the database
                cur.execute('SELECT * FROM Users WHERE username = %s AND passwords = %s', (username, password))
                user = cur.fetchone()
                st.write(user)
                
                if user is not None:
                    # Login the user
                    st.session_state['logged_in'] = True
                    st.session_state['role'] = user[3]

                    # Redirect the user to the appropriate interface
                    if st.session_state['role'] == 'admin':
                        st.experimental_rerun()
                        
                    else:
                        if st.session_state['role'] == 'user':
                            st.experimental_rerun()
                        
                        
                else:
                    st.error('Invalid username or password.')

        else:
            # The user is logged in, so display the appropriate interface
            if st.session_state['role'] == 'admin':
                admin_actions()
            #else:
                #user_actions() 

def admin_actions():
            if st.session_state['role'] == 'admin':
                # Display the admin interface
                
                with st.sidebar:
                    selected = option_menu("Main Menu", ["Home", 'Uploaded videos','Dubbed videos','Sign Out'], 
                        icons=['house', 'gear'], menu_icon="cast", default_index=1)
                    selected

                if selected == "Home":
                    dashboard()  
                if selected == "Uploaded videos":
                    uploadvideos() 
                if selected == "Dubbed videos":
                    videos() 

                if selected == "Sign Out":
                    #logout()
                    st.session_state.clear()
                    st.rerun()

def user_actions():
            
    if st.session_state['role'] == 'user':
        # Display the user interface           
        with st.sidebar:
            selected2 = option_menu("User Menu", ["Home", 'Account Details','intergation operation','Integration Videos','Sign Out'], 
                icons=['house', 'gear'], menu_icon="cast", default_index=1)
            selected2


        if selected2 == "Integration Videos":
            videos()

        if selected2 == "Sign Out":
            #logout()
            st.session_state.clear()
            st.rerun() 
login()

# Close the database connection


cur.close()
conn.close()

