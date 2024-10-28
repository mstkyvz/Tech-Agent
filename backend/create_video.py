import logging
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import prompt
import os
import base64
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

client = OpenAI()

def encode_image(image_path):
    """Convert an image to a base64 encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            logging.debug(f"Encoded image {image_path} to base64.")
            return encoded_string
    except Exception as e:
        logging.error(f"Failed to encode image {image_path}: {e}")
        raise

def llm(message, image_url=None):
    msg = {"role": "user", "content": [{"type": "text", "text": message}]}
    
    if image_url:
        msg['content'].append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{image_url}"}
        })
        logging.debug(f"Added image URL to message: {image_url}")
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[msg],
        )
        logging.debug("Received completion from LLM.")
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Failed to get completion from LLM: {e}")
        raise

def video(image_path):
    # Convert the image to base64
    logging.info(f"Processing video for image: {image_path}")
    
    image_base64 = encode_image(image_path)
    
    try:
        solution = llm(prompt.solution_prompt, image_base64)
        logging.debug("Generated solution from LLM.")
        
        manim_code = llm(prompt.manim_prompt, image_base64)
        logging.debug("Generated Manim code from LLM.")
        
        manim_code = manim_code.split("```python")[1]
        manim_code = manim_code.split("```")[0]
        
        # Write the generated Manim code to a file
        with open("manimCode.py", "w",encoding="utf-8") as f:
            f.write(manim_code)
            logging.info("Manim code written to mainCode.py.")
        
        # Execute the Manim command
        os.system("manim -pql manimCode.py Solution")
        logging.info("Executed Manim command.")
        
    except Exception as e:
        logging.error(f"Error in video generation: {e}")
        raise

# Call the video function
video("s2.png")
