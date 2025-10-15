from boltiotai import openai
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_tutorial(components):
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"system", "content":"Helping AI assistant"},
            {"role":"user", "content":f"Suggest a recipe using the items listed as available. Make sure you have a nice name for this recipe. Then share the recipe in a step-by-step manner. Here are the items available: {components}, Haldi, Chilly Powder, Tomato Ketchup, Water, Garam Masala, Oil. Try to answer in less than 6 lines"}
        ]
    )
    return response["choices"][0]["message"]["content"]

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def hello():
    output = ""
    if request.method == 'POST':
        components = request.form['components']
        output = generate_tutorial(components)
    return render_template('index.html', output=output)

@app.route('/generate', methods=['POST'])
def generate():
    components = request.form['components']
    return generate_tutorial(components)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=8080)