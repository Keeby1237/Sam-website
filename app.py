from flask import Flask, request, render_template_string
from transformers import pipeline

app = Flask(__name__)
generator = pipeline("text-generation", model="Smilyai-labs/Sam-reason-A1")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Text Generator</title>
    <style>
        body { font-family: sans-serif; margin: 2rem; }
        textarea { width: 100%; height: 150px; }
        .output { margin-top: 1rem; background: #f4f4f4; padding: 1rem; border-radius: 6px; }
    </style>
</head>
<body>
    <h2>Text Generator UI</h2>
    <form method="POST">
        <textarea name="prompt" placeholder="Enter your prompt here...">{{ prompt or '' }}</textarea><br><br>
        <input type="submit" value="Generate">
    </form>
    {% if result %}
    <div class="output">
        <strong>Generated Text:</strong>
        <p>{{ result }}</p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    prompt = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        output = generator(prompt, max_length=100, do_sample=True)
        result = output[0]["generated_text"]
    return render_template_string(HTML, result=result, prompt=prompt)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
