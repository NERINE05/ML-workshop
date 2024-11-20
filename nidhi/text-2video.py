import openai
import cohere
from moviepy import ImageClip, concatenate_videoclips
import requests
from io import BytesIO

# Initialize APIs
cohere_api_key = "v3MveYurFYCrCrS4UnazRQ7yqkHreNXXuluBk4cm"  # Replace with your Cohere API key
openai.api_key = "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"  # Replace with your OpenAI API key

co = cohere.Client(cohere_api_key)

# Function to generate text using Cohere
def generate_text(prompt: str):
    try:
        response = co.generate(
            model='command-xlarge-nightly',  # Use a valid Cohere model
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"Error generating text with Cohere: {e}")
        return None

# Function to generate image using OpenAI DALL·E
def generate_image_from_text(prompt: str):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        img_data = requests.get(image_url).content
        image = BytesIO(img_data)  # Convert image data to BytesIO object
        return image
    except Exception as e:
        print(f"Error generating image with DALL·E: {e}")
        return None

# Function to create video from generated images
def create_video_from_images(prompts: list, output_path: str):
    clips = []

    for prompt in prompts:
        try:
            # Generate text using Cohere
            generated_text = generate_text(prompt)
            if generated_text:
                print(f"Generated Text: {generated_text}")
                
                # Generate image from text using DALL·E
                image_data = generate_image_from_text(generated_text)
                if image_data:
                    # Create an ImageClip from the image
                    img_clip = ImageClip(image_data)
                    img_clip = img_clip.set_duration(5)  # Set the duration of the image in the video (5 seconds)
                    clips.append(img_clip)
        except Exception as e:
            print(f"Error processing prompt: {prompt}\n{e}")

    # Concatenate the images into a video
    if clips:
        final_video = concatenate_videoclips(clips, method="compose")
        final_video.write_videofile(output_path, fps=24, codec="libx264")
        print(f"Video created successfully: {output_path}")
    else:
        print("No images to combine into a video.")

# Main execution
if __name__ == "__main__":
    # Define prompts for text generation
    prompts = [
        "A futuristic city with flying cars",
        "A beautiful sunset over a calm beach",
        "An alien landscape with strange plants"
    ]
    
    # Path to save the output video
    video_output_path = "output_video.mp4"
    
    # Create video from generated images
    create_video_from_images(prompts, video_output_path)
