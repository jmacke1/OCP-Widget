import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

row0_spacer1, row0_1, row0_spacer2 = st.beta_columns(
    (.1, 2, .1))

row0_1.title('Examining how OCP utility changes with various preference and situational parameters.')

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.beta_columns((2,3))

with row1_1:
    st.title("OCP Utility")
    eta_selected = st.slider("Select eta", 0, 10, value = 1)
    lambda_selected = st.slider("Select lambda", 1, 10, value = 3)
    a_selected = st.slider("Select a", -10, 10, value = 0)
    c_selected = st.slider("Select c", 0, 10, value = 1)

# Start with utility from lottery [a,1-q;a+c,q], c>0.

q_seq = np.linspace(0,1,50)
eta_seq = np.linspace(0, 10, 11)
lambda_seq = np.linspace(1, 10, 10)
a_seq = np.linspace(-10, 10, 21)
c_seq = np.linspace(0, 10, 11)

q_list, eta_list, lambda_list, a_list, c_list = pd.core.reshape.util.cartesian_product([q_seq, eta_seq, lambda_seq, a_seq, c_seq])

all_utils = pd.DataFrame(dict(q = q_list, eta = eta_list, lambda_ = lambda_list, a = a_list, c = c_list))

all_utils['simp_util'] = all_utils.a + all_utils.q * all_utils.c - all_utils.q * (1 - all_utils.q) * all_utils.eta * (all_utils.lambda_-1) * all_utils.c


filtered = all_utils[
    (all_utils.eta == eta_selected) & 
    (all_utils.lambda_ == lambda_selected) &
    (all_utils.a == a_selected) &
    (all_utils.c == c_selected) 
    ]

source = pd.DataFrame({
  'q': filtered.q,
  'Utility': filtered.simp_util
})

with row1_2: 
    st.altair_chart(alt.Chart(source)
        .mark_line().encode(
        x='q',
        y='Utility'
    ).properties(
        width=500,
        height=500   
    ))