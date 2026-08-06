import streamlit as st


def login():

    st.sidebar.title("Login")


    username = st.sidebar.text_input(
        "Username"
    )


    password = st.sidebar.text_input(
        "Password",
        type="password"
    )


    role = st.sidebar.selectbox(
        "Role",
        [
            "user",
            "admin"
        ]
    )


    if st.sidebar.button("Login"):


        # temporary authentication
        # replace later with database


        if username and password:


            st.session_state.logged_in = True

            st.session_state.role = role


            st.sidebar.success(
                f"Logged in as {role}"
            )

        else:

            st.sidebar.error(
                "Invalid login"
            )