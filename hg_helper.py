import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(api_key=os.environ["HF_TOKEN"])

def generate_pet_of_prompt(prompt):
    model = "black-forest-labs/FLUX.1-dev"


    image = client.text_to_image(
        prompt=prompt,
        model=model
    )

    image.save("pet_image.png")
    return image


if __name__ == "__main__":
    generate_pet_of_prompt()