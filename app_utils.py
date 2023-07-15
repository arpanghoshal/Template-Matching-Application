import pandas as pd
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def load_csv(file):
    """Load csv file with pandas."""
    try:
        return pd.read_csv(file, nrows=5)
    except Exception as e:
        return None, str(e)

def run_llm_chain(llm, prompt, variables):
    """Run LLMChain with the specified language model, prompt, and variables."""
    try:
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(variables), None
    except Exception as e:
        return None, str(e)

def generate_transformation_instructions(user_file, template_file, openai_api_key):
    """Generate transformation instructions from user file to template file."""
    user_table, error = load_csv(user_file)
    template_table, error = load_csv(template_file)

    if error is not None:
        return None, error

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

    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=openai_api_key,temperature=0.1)
    return run_llm_chain(llm, prompt, {
        'user_table_str_col': user_table_str_col,
        'user_table_str_frst': user_table_str_frst,
        'template_table_str_col':template_table_str_col,
        'template_table_str_frst':template_table_str_frst,
        'output_example':output_example
    })

def generate_correction_instructions(json_output, not_correct, openai_api_key):
    """Generate corrected transformation instructions based on user feedback."""
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=openai_api_key,temperature=0.2)
    
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

def generate_transformation_code(json_output, openai_api_key):
    """Generate transformation code based on json instructions."""
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=openai_api_key,temperature=0.2)
    
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
    return run_llm_chain(llm, prompt, {'json_output': json_output})
