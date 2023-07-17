Begin Few-shot Learning Process

1. Initialize an empty list 'prompt_examples' to store successful transformation logic

2. Whenever a successful transformation logic is generated:
    - Add the 'transformation_logic' to a temporary list 'new_examples'

3. Sort 'new_examples' based on distinctiveness or complexity of transformation logic (MMR Algorithm)

4. If the length of 'prompt_examples' is less than 5:
    - Add the most distinctive examples from 'new_examples' to 'prompt_examples' until it contains 5 examples 
Else:
    - Compare the new examples with the existing examples in 'prompt_examples'
    - If a new example is more distinctive or complex than an existing example, replace the least distinctive example in 'prompt_examples' with the new one

5. When generating transformation logic for a new transformation:
    - Use 'prompt_examples' as the prompt for GPT-3.5
    - Generate the 'transformation_logic' based on the 'prompt_examples'

End Few-shot Learning Process
