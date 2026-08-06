import streamlit as st
import asyncio

import sys
import os


sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)


from agent.user_agent import get_user_agent
from agent.admin_agent import ask_admin



# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="HR Assistant",
    page_icon="🤖",
    layout="centered"
)



# -------------------------
# Session State
# -------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


if "role" not in st.session_state:
    st.session_state.role = None


if "messages" not in st.session_state:
    st.session_state.messages = []



# -------------------------
# Login
# -------------------------

st.sidebar.title("🔐 Login")


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


    if username and password:


        st.session_state.logged_in = True

        st.session_state.role = role

        st.session_state.messages = []


        st.sidebar.success(
            f"Logged in as {role}"
        )


    else:

        st.sidebar.error(
            "Enter username and password"
        )



# -------------------------
# Login Check
# -------------------------

if not st.session_state.logged_in:

    st.warning(
        "Please login first"
    )

    st.stop()



# -------------------------
# Load User Agent
# -------------------------

@st.cache_resource
def load_user_agent():

    return get_user_agent()



if st.session_state.role == "user":

    user_agent = load_user_agent()



# -------------------------
# Header
# -------------------------

st.title(
    "🤖 HR Assistant"
)



if st.session_state.role == "user":

    st.info(
        "User Mode: HR documents only"
    )

else:

    st.info(
        "Admin Mode: HR documents + employee data"
    )



# -------------------------
# Display Chat History
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )



# -------------------------
# User Question
# -------------------------

question = st.chat_input(
    "Ask HR Assistant..."
)



if question:


    st.session_state.messages.append(

        {
            "role": "user",
            "content": question
        }

    )


    with st.chat_message("user"):

        st.markdown(question)



    with st.chat_message("assistant"):


        with st.spinner(
            "Thinking..."
        ):



            # =========================
            # USER MODE
            # =========================

            if st.session_state.role == "user":


                result = user_agent(
                    question
                )


                answer = result["answer"]


                sources = result.get(
                    "sources",
                    []
                )


                if sources:


                    answer += "\n\n### Sources\n"


                    for source in sources:


                        answer += (
                            f"- {source['file']} "
                            f"(Page {source['page']})\n"
                        )



            # =========================
            # ADMIN MODE
            # =========================

            else:


                answer = asyncio.run(

                    ask_admin(
                        question
                    )

                )



            st.markdown(
                answer
            )



    st.session_state.messages.append(

        {
            "role": "assistant",
            "content": answer
        }

    )