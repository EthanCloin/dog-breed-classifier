from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# # Load the pre-trained model and processor.
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# # Save model and processor locally.
# model.save_pretrained("./models")
# processor.save_pretrained("./models")



# Load the saved model and processor from the local directory.
processor = BlipProcessor.from_pretrained("./models")
model = BlipForConditionalGeneration.from_pretrained("./models")


# Open your image
image = Image.open("./images/000000580294.jpg").convert("RGB")

# Preprocess and generate caption
inputs = processor(image, return_tensors="pt")
output_ids = model.generate(**inputs)
caption = processor.decode(output_ids[0], skip_special_tokens=True)
print(output_ids[0])
print("Generated Caption:", caption)


User1 = {"user_id": "User1",
  "captions": [
    "Enjoying the sunny day!",
    "Had a great brunch at the new cafe",
    "Enjoying the lazy Sunday vibes with a warm cup of coffee",
    "Just vibing at the beach life is good!",
    "Catching sunsets and living for the moment.",
    "Coffee, friends, and endless talks."
  ]
}



