"""A main script to run streamlit application.

"""
import streamlit as st
from src.utility.loggers import logger
from src.inference.core import generate_output
from src.utility.graph_visualization import get_graph_plot

st.title("Knowledge Graph")
form = st.form(key="my-form")
input_data = form.text_area("Enter text for Knowledge Graph creation")
#only_custom_entities = form.checkbox(
#    "Extract Relationships for only Custom Entities"
#)
submit = form.form_submit_button("Submit")

if submit:
    try:
        output_df = generate_output(input_data)
        st.dataframe(output_df)
        output_plot = get_graph_plot(output_df)
        st.pyplot(output_plot)
    except Exception as error:
        message = "Error while creating output"
        logger.error(message, str(error))
