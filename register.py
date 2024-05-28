import streamlit as st
import database


conn = database.db()
# Get the database connection
cursor = conn
cursor = conn.cursor()


def registeruser():
    # Display the register user form
    st.title('Register User')   

    username = st.text_input('Username')
    password = st.text_input('Password', type='password')

    role = st.selectbox('Role', ['user', 'admin'])

    if st.button('Register'):
        # Check if the username already exists in the database
        cursor.execute('SELECT * FROM users')
        data =cursor.fetchone()
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()


        if user is None:
            # Insert the new user into the database
            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, role))
            conn.commit()

            # Success message
            st.success('User registered successfully!')
        
        else:
            # Error message
            st.error('Username already exists.')

    # Close the database connection
    cursor.close()
    conn.close()
