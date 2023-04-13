import tkinter as tk
from tkinter import filedialog
import pytesseract
from PIL import Image
import openai

api_key = "API_KEY"
openai.api_key = api_key

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def open_image():
    # Ask the user to select an image file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Open the image using PIL
        image = Image.open(file_path)

        # Preprocess the image
        image = image.convert('L')  # Convert the image to grayscale
        image = image.point(lambda x: 0 if x < 128 else 255, '1')  # Binarize the image

        # Use pytesseract to convert the image to text
        text = pytesseract.image_to_string(image, lang='eng', config='--psm 6')

        # Display the text in the GUI
        text_box.config(state='normal')
        text_box.delete('1.0', tk.END)
        text_box.insert(tk.END, text)
        text_box.config(state='disabled')

def get_openai_response():
    prompt = input_text.get()

    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.5,
            timeout=10, # Set the timeout to 10 seconds
        )
        output_text.config(state='normal')
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, response.choices[0].text.strip())
        output_text.config(state='disabled')
    except openai.error.OpenAIError as e:
        output_text.config(state='normal')
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, f"Error occurred: {e}")
        output_text.config(state='disabled')

root = tk.Tk()
root.title("AARC")

# Create a label and entry for the OpenAI prompt
input_label = tk.Label(root, text="Enter a prompt:")
input_label.pack()

input_text = tk.Entry(root)
input_text.pack()

# Create a button to get OpenAI response
openai_button = tk.Button(root, text="Get OpenAI response", command=get_openai_response)
openai_button.pack()

# Create a label and text box for the OpenAI response
output_label = tk.Label(root, text="OpenAI response:")
output_label.pack()

output_text = tk.Text(root, height=5, state='disabled')
output_text.pack()

# Create a button to open an image
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

# Create a text box to display the OCR result
text_box = tk.Text(root, height=20, state='disabled')
text_box.pack()

root.mainloop()
