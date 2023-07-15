import os
import pandas as pd
import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

st.title('Template Matching Application')
st.markdown('Made by [Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/): 3 hour project')

template_file = st.file_uploader("Upload your Template Table", type=['csv'])
user_file = st.file_uploader("Upload your table to transform", type=['csv'])

@st.cache_data
def load_csv(file):
    """Load csv file with pandas."""
    try:
        return pd.read_csv(file, nrows=5)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

def run_llm_chain(llm, prompt, variables):
    """Run LLMChain with the specified language model, prompt, and variables."""
    try:
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(variables)
    except Exception as e:
        st.error(f"Error running LLMChain: {e}")
        return None

def generate_transformation_instructions(user_file, template_file):
    """Generate transformation instructions from user file to template file."""
    user_table = load_csv(user_file)
    template_table = load_csv(template_file)

    if user_table is None or template_table is None:
        return None

    user_table_str_col = str(list(user_table.columns))
    template_table_str_col = str(list(template_table.columns))
    user_table_str_frst = str(list(user_table.iloc[0]))
    template_table_str_frst = str(list(template_table.iloc[0]))

    output_example="""
    {
        "column_renames": {},
        "columns_to_remove": [],
        "columns_to_keep": [],
        "data_transformations": {}
    }
    """
    
    prompt = PromptTemplate(
        input_variables=["user_table_str_col", "user_table_str_frst", "template_table_str_col", "template_table_str_frst", "output_example"],
        template="""
        Given the following information:
        - User data columns: {user_table_str_col}
        - User data example row: {user_table_str_frst}
        - Template data columns: {template_table_str_col}
        - Template data example row: {template_table_str_frst}

        Generate a JSON object detailing:
        1. Mapping of user data columns to template data columns (column_renames)
        2. Any necessary data transformations (data_transformations)
        3. Columns to remove or keep (columns_to_remove, columns_to_keep)

        The output should follow this format: {output_example}
        """
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=st.secrets['openai']['OPENAI_API_KEY'],temperature=0.1)
    return run_llm_chain(llm, prompt, {
        'user_table_str_col': user_table_str_col,
        'user_table_str_frst': user_table_str_frst,
        'template_table_str_col':template_table_str_col,
        'template_table_str_frst':template_table_str_frst,
        'output_example':output_example
    })

def generate_correction_instructions(json_output, not_correct):
    """Generate corrected transformation instructions based on user feedback."""
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=st.secrets['openai']['OPENAI_API_KEY'],temperature=0.2)
    
    prompt = PromptTemplate(
        input_variables=["json_output","not_correct"],
        template="""
        - Update the following JSON output:
            {json_output}
        - Based on these corrections:
            {not_correct}
        """
    )
    return run_llm_chain(llm, prompt, {'json_output': json_output, 'not_correct': not_correct})

def generate_transformation_code(json_output):
    """Generate transformation code based on json instructions."""
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=st.secrets['openai']['OPENAI_API_KEY'],temperature=0.2)
    
    prompt = PromptTemplate(
        input_variables=["json_output"],
        template="""
        - Given these instructions in JSON format:
          {json_output}
        - Write a Python script using pandas to:
          1. Rename the columns according to 'column_renames'
          2. Drop the columns listed in 'columns_to_remove'
          3. Keep the columns listed in 'columns_to_keep'
          4. Apply the transformations specified in 'data_transformations'
        """
    )
    code_output = run_llm_chain(llm, prompt, {'json_output': json_output})
    st.code(code_output)
    st.write("Please copy the code and run it in your local machine.")

if user_file and template_file:
    json_output = generate_transformation_instructions(user_file, template_file)
    if json_output is None:
        st.write("An error occurred. Please try again.")
    else:
        st.json(json_output)
        is_correct = st.selectbox('Is the generated json correct?', ['Yes', 'No'])
        if is_correct == 'No':
            not_correct = st.text_input('Please indicate what is not correct:')
            if not_correct:
                json_output = generate_correction_instructions(json_output, not_correct)
                if json_output is None:
                    st.write("An error occurred. Please try again.")
                else:
                    st.json(json_output)
                    if st.button('Generate Corrected Transformation Code'):
                        generate_transformation_code(json_output)
        elif is_correct == 'Yes':
            if st.button('Generate Transformation Code'):
                generate_transformation_code(json_output)
else:
    st.write("Please upload both files.")
