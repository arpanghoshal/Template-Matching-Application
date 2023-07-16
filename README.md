# Template Matching Application

## Overview

The Template Matching Application is a tool that utilizes Langchain and OpenAI to transform a user's data to match a specific template. Users upload their data and a template file in CSV format, and the application generates instructions for transforming the data to match the template. These instructions are then converted into Python code, which the user can run on their local machine.

## File Structure

The project is structured as follows:

- `app.py`: This is the main application file. It contains the user interface logic and interacts with the helper functions defined in `app_utils.py`.
- `app_utils.py`: This file contains all the helper functions used in the application for loading CSV files, running the LLMChain, and generating transformation instructions, correction instructions, and transformation code.

## Method Descriptions

`app_utils.py` contains the following methods:

- `load_csv(file)`: This function takes a file path as an argument and uses pandas to load the CSV file. It returns a DataFrame containing the file data.

- `run_llm_chain(llm, prompt, variables)`: This function runs an LLMChain using the provided language model, prompt, and variables.

- `generate_transformation_instructions(user_file, template_file, openai_api_key)`: This function takes the user's file, the template file, and the OpenAI API key as arguments. It generates transformation instructions using the ChatOpenAI model and returns a JSON object detailing the instructions.

- `generate_correction_instructions(json_output, not_correct, openai_api_key)`: This function takes the original transformation instructions, user feedback, and the OpenAI API key as arguments. It generates corrected transformation instructions based on the user's feedback.

- `generate_transformation_code(json_output, openai_api_key)`: This function takes the transformation instructions and the OpenAI API key as arguments. It generates Python code for performing the data transformation based on the instructions.

## Usage

1. Clone this repository:

```bash
git clone https://github.com/arpanghoshal/Template-Matching-Application.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the Streamlit application:

```bash
streamlit run app.py
```

4. Access the application in your browser via the localhost URL that Streamlit provides (usually `http://localhost:8501`).

5. Follow the prompts in the application to upload your data and template files, verify the generated transformation instructions, and generate your transformation code.

Sure, here is the proposed approach in Markdown format.

---

**Proposed Approach to Solve Misalignment and Ambiguity of Column Mapping in Assignment**


---

**Project Demo:** [Link](#)

**Algorithm for the Approach:** [Link](#)

---

**1. Column Mapping:**

- Load user and template data.
- For each user data column, extract and encode the first few rows using a Language Model (e.g., BERT) to generate 'user_embeddings.'
- For each template data column, generate 'template_embeddings.'
- Compute cosine similarity between 'user_embeddings' and 'template_embeddings' for each pair of user and template columns.
- Map each user column to the template column with the highest cosine similarity.

---

**2. Addressing Ambiguities in Mapping:**

- Identify mappings where multiple user columns are mapped to a single template column or vice versa.
- For each ambiguous mapping, present the user with potential matches for them to confirm or select the most suitable match.

---

**3. Generating Transformation Logic:**

- For each mapped column pair, use GPT-3.5 to generate transformation logic based on examples of the transformation process.

---

**4. Retraining for Improved Accuracy:**

- **Approach 1 - Few-shot Learning:** Store the transformation logic as part of 'prompt_examples' for future transformations.
- **Approach 2 - Retraining the Model:** Continuously collect 'labeled_data' for each successful transformation. When enough 'labeled_data' is collected, retrain the GPT model. [Link to the Algorithm Approach](#)

---

**5. Post-Transformation Validation:**

- Apply the transformation logic to the user data to generate 'transformed_data.'
- Compare 'transformed_data' with the template format and alert the user of any discrepancies.

---

## Contributing

Contributions are welcome! Please fork this repository and create a Pull Request with your changes.

## License

This project is licensed under the terms of the MIT license.

## Author

[Arpan Ghoshal](https://www.linkedin.com/in/arpanghoshal/)

## Note
This project was successfully completed in a span of just 4 hours, thanks to the efficiency and power of the Langchain and OpenAI libraries. It involved a lot of iterative testing with various prompting techniques, to ensure that the generated outputs (transformation instructions and Python code) are accurate and robust. The application has been designed to be user-friendly, providing an intuitive interface and interactive options for uploading data, generating transformation instructions, making corrections, and generating transformation code. This project serves as an excellent demonstration of the capabilities of language models in practical applications.


