import pandas as pd
import streamlit as st
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

st.title('Template Matching Application')

template_file = st.file_uploader("Upload your Template Table", type=['csv'])
user_file = st.file_uploader("Upload your table to transform", type=['csv'])

def load_csv(file):
    """Load csv file with pandas."""
    return pd.read_csv(file)

def run_llm_chain(llm, prompt, variables):
    """Run LLMChain with the specified language model, prompt, and variables."""
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(variables)

def generate_transformation_instructions(user_file, template_file):
    """Generate transformation instructions from user file to template file."""
    user_table = load_csv(user_file)
    template_table = load_csv(template_file)

    user_table_str_col = str(list(user_table.columns))
    template_table_str_col = str(list(template_table.columns))
    user_table_str_frst = str(list(user_table.iloc[0]))
    template_table_str_frst = str(list(template_table.iloc[0]))

    output_example="""
    {
        "column_renames": {

        },
        "columns_to_remove": [],
        "columns_to_keep": [],
        "data_transformations": {

        }
    }
    """
    
    prompt = PromptTemplate(
        input_variables=["user_table_str_col", "user_table_str_frst", "template_table_str_col", "template_table_str_frst", "output_example"],
        template="""
        - I have the user_data with the following columns: {user_table_str_col}. \
        - The user_data is formatted as follows: {user_table_str_frst} \
        - This is the template_data columns: {template_table_str_col} \
        - These are the values in template_data: {template_table_str_frst} \
        - Map the user_data columns with the most relevant columns of transformed_data \
        - Understand what transformation needed for user_data to match the format of template_data \
        - Consider, column_renames are the mapping done on user_data to match columns of template_data \
        - column_to_remove are the columns that are not there in template_data \
        - columns_to_keep are the columns that are in the template_data \
        - data_transformations are the transformation performed on user_data columns to make the format of user_data columns as template_data columns \
        - data_transformations should also show which column in user_data the transformation is happening \
        - The output should be in the JSON of this format: {output_example} \
        STRICTLY JSON FORMAT
        """
    )

    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key='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',temperature=0.1)
    return run_llm_chain(llm, prompt, {
        'user_table_str_col': user_table_str_col,
        'user_table_str_frst': user_table_str_frst,
        'template_table_str_col':template_table_str_col,
        'template_table_str_frst':template_table_str_frst,
        'output_example':output_example
    })

def generate_correction_instructions(json_output, not_correct):
    """Generate corrected transformation instructions based on user feedback."""
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key='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',temperature=0.2)
    
    prompt = PromptTemplate(
        input_variables=["json_output","not_correct"],
        template="""
    - Change this json_output:
                {json_output}
    - To the correct format mentioned by following these changes:
                {not_correct}
    """
    )
    return run_llm_chain(llm, prompt, {'json_output': json_output, 'not_correct': not_correct})

def generate_transformation_code(json_output):
    """Generate transformation code based on json instructions."""
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key='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',temperature=0.2)
    
    prompt = PromptTemplate(
        input_variables=["json_output"],
        template="""
    - This is the instruction in json on how to transform user_table.csv to transformed_table.csv:
    {json_output}
    - Write a python code to:
        1. Rename the columns with column_renames
        2. Drop the colums with columns_to_remove
        3. Keep the columns with columns_to_keep
        4. Transform the column with data_transformations

        Here, data_transformations shows how the particular column should be transformed with an example.

        .str.replace() should replace the general condition instead of conidering one example like:
        df['column_name'] = df['column_name'].replace(' Plan', '', regex=True)

    """
    )
    code_output = run_llm_chain(llm, prompt, {'json_output': json_output})
    st.code(code_output)
    st.write("Please copy the code and run it in your local machine.")

if user_file and template_file:
    json_output = generate_transformation_instructions(user_file, template_file)
    st.json(json_output)

    is_correct = st.selectbox('Is the generated json correct?', ['Yes', 'No'])
    if is_correct == 'No':
        not_correct = st.text_input('Please indicate what is not correct:')
        if not_correct:
            json_output = generate_correction_instructions(json_output, not_correct)
            st.json(json_output)
            if st.button('Generate Corrected Transformation Code'):
                generate_transformation_code(json_output)
    elif is_correct == 'Yes':
        if st.button('Generate Transformation Code'):
            generate_transformation_code(json_output)
else:
    st.write("Please upload both files.")
