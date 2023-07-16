import pandas as pd
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

def load_csv(file):
    """Load csv file with pandas."""
    try:
        # Try to read CSV file
        return pd.read_csv(file, nrows=5), None
    except Exception as e:
        # Return None and the error if an exception occurs
        return None, str(e)

def run_llm_chain(llm, prompt, variables):
    """Run LLMChain with the specified language model, prompt, and variables."""
    try:
        # Try to run the LLMChain
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(variables), None
    except Exception as e:
        # Return None and the error if an exception occurs
        return None, str(e)

def generate_transformation_instructions(user_file, template_file, openai_api_key):
    """Generate transformation instructions from user file to template file."""
    # Load the user and template files
    user_table, error = load_csv(user_file)
    template_table, error = load_csv(template_file)

    if error is not None:
        # Return None and the error if an exception occurs
        return None, error
    
    global user_table_str_col
    global user_table_str_frst
    global template_table_str_col
    global template_table_str_frst

    # Extract information about the tables for the prompt
    user_table_str_col = str(list(user_table.columns))
    template_table_str_col = str(list(template_table.columns))
    user_table_str_frst = str(list(user_table.iloc[0]))
    template_table_str_frst = str(list(template_table.iloc[0]))

    template_table_lst_col = list(template_table.columns)

    result = {}
    for item in template_table_lst_col:
        result[f"old_{item}_format"] = ""
        result[f"new_{item}_format"] = ""
        result[f"old_{item}_datatype"] = ""
        result[f"new_{item}_datatype"] = ""
        result[f"old_{item}_firstdata"] = ""
        result[f"new_{item}_firstdata"] = ""


    result = str(result)

    # Example of the expected output
    output_example="""
    {
        "ç": {},
        "columns_to_remove": [],
        "columns_to_keep": [],
        "data_transformations":  %s
        }
  
    }
    """  % result

    describe_output_example="""

        Here column_renames is a mapping of user data columns to template data columns, for example:
        {
            "user_data_column_1": "template_data_column_1",
            "user_data_column_2": "template_data_column_2",
        }

        Here in data_transformations, while computing observe these very carefully:
        {
            "old_item_format": format of the item in the user data
            "new_item_format": format of the item in the template data,
            "old_item_datatype": data type of the item in the user data
            "new_item_datatype": data type of the item in the template data
            "old_item_firstdata": first row of the item in the user data
            "new_item_firstdata": first row of the item in the template data
        }

        item are the column name in the template data


        """
    
    # Prepare the prompt template
    prompt = PromptTemplate(
        input_variables=["user_table_str_col", "user_table_str_frst", "template_table_str_col", "template_table_str_frst", "output_example", "describe_output_example"],
        template="""
    Given the following information:
    - User data columns: {user_table_str_col}
    - User data example row: {user_table_str_frst}
    - Template data columns: {template_table_str_col}
    - Template data example row: {template_table_str_frst}

    For each column in the template data, generate a JSON object detailing:
    1. The corresponding user data column (column_renames)
    2. The necessary transformations, including:
        - Original format and datatype
        - Desired format and datatype
        - Example data before and after transformation
    3. Specify which columns should be removed or kept (columns_to_remove, columns_to_keep)

    IMPORTANT: If no transformation is necessary for a certain field, please specify the same values for the old and new formats, datatypes, and example data.

    The output should follow JSON format, this is one of the example: {output_example}

    {describe_output_example}

        """
    )

    # Initialize the language model
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=openai_api_key,temperature=0.3)
    # Run the LLMChain
    return run_llm_chain(llm, prompt, {
        'user_table_str_col': user_table_str_col,
        'user_table_str_frst': user_table_str_frst,
        'template_table_str_col':template_table_str_col,
        'template_table_str_frst':template_table_str_frst,
        'output_example':output_example,
        'describe_output_example':describe_output_example
    })

def generate_correction_instructions(json_output, not_correct, openai_api_key):
    """Generate corrected transformation instructions based on user feedback."""
    # Initialize the language model
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=openai_api_key,temperature=0)
    
    # Prepare the prompt template
    prompt = PromptTemplate(
        input_variables=["json_output","not_correct"],
        template="""
        - Update the following JSON output:
            {json_output}
        - Based on these corrections:
            {not_correct}
        """
    )
    # Run the LLMChain
    return run_llm_chain(llm, prompt, {'json_output': json_output, 'not_correct': not_correct})

def generate_transformation_code(json_output, openai_api_key):
    """Generate transformation code based on json instructions."""
    # Initialize the language model
    llm = ChatOpenAI(model='gpt-3.5-turbo',openai_api_key=openai_api_key,temperature=0.4)
    
    # Prepare the prompt template
    prompt = PromptTemplate(
        input_variables=["user_table_str_col", "user_table_str_frst", "template_table_str_col", "template_table_str_frst","json_output"],
        template="""
        - The user data columns are: {user_table_str_col}
        - The user data example row is: {user_table_str_frst}
        - The template data columns are: {template_table_str_col}
        - The template data example row is: {template_table_str_frst}

        - Given these instructions in JSON format:
          {json_output}

        - Write a Python script transforming 'user_data.csv' to 'transformed_data.csv' using pandas to:
          1. Rename the columns according to 'column_renames'
          2. Drop the columns listed in 'columns_to_remove'
          3. Keep the columns listed in 'columns_to_keep'
          4. Apply the transformations specified in 'data_transformations'
        """
    )
    # Run the LLMChain
    return run_llm_chain(llm, prompt, {
        'user_table_str_col': user_table_str_col,
        'user_table_str_frst': user_table_str_frst,
        'template_table_str_col':template_table_str_col,
        'template_table_str_frst':template_table_str_frst,
        'json_output': json_output})
