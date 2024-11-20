import cohere


# Initialize Cohere with your API key
co = cohere.Client('v3MveYurFYCrCrS4UnazRQ7yqkHreNXXuluBk4cm')  # Replace with your Cohere API key

def generate_story(input_text):
    # Define the prompt to create a more detailed and structured story
    prompt = f"Write a detailed and engaging large story based on the following text: {input_text}"

    # Call the Cohere API to generate the story with more tokens
    response = co.generate(
        model='command-xlarge-nightly',  # Use the 'command-xlarge' model for better results
        prompt=prompt,
        max_tokens=500,  # Increase the token limit for a more detailed story
        temperature=0.7,  # Control the creativity; you can adjust this value for different styles
        stop_sequences=["\n"]  # Ensure the story ends properly
    )

    # Extract the generated story from the response
    story = response.generations[0].text.strip()
    return story

# Example usage
input_text = "A young girl discovers a hidden door in her attic that leads to a magical world."
story = generate_story(input_text)
print("Generated Story:")
print(story)
