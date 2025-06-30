import string
import os
import time
from collections import Counter
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from flask import Flask, render_template, request, jsonify

# --- Your Analysis Logic Wrapped in a Function ---
def analyze_text(text):
    # 1. Text Preprocessing
    lower_case_text = text.lower()
    cleaned_text = lower_case_text.translate(str.maketrans('', '', string.punctuation))
    tokenized_words = word_tokenize(cleaned_text, "english")
    
    # 2. Stopword Removal
    final_words = []
    for word in tokenized_words:
        if word not in stopwords.words('english'):
            final_words.append(word)

    # 3. Custom Emotion Analysis
    emotion_list = []
    try:
        with open('emotions.txt', 'r') as file:
            for line in file:
                clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                if word in final_words:
                    emotion_list.append(emotion)
    except FileNotFoundError:
        return {'error': 'emotions.txt not found.'}

    emotion_counts = Counter(emotion_list)

    # 4. NLTK Vader Sentiment Analysis
    score = SentimentIntensityAnalyzer().polarity_scores(cleaned_text)
    neg_score = score['neg']
    pos_score = score['pos']
    
    if neg_score > pos_score:
        sentiment_result = "Negative Sentiment"
    elif pos_score > neg_score:
        sentiment_result = "Positive Sentiment"
    else:
        sentiment_result = "Neutral Vibe"

    # 5. Generate and Save Graph
    # Ensure the static directory exists
    if not os.path.exists('static'):
        os.makedirs('static')

    fig, ax1 = plt.subplots()
    ax1.bar(emotion_counts.keys(), emotion_counts.values())
    fig.autofmt_xdate()
    plt.title('Emotion Analysis')
    plt.ylabel('Count')
    plt.xlabel('Emotions')
    
    # Save the plot with a unique filename to avoid browser caching
    graph_filename = f"graph_{int(time.time())}.png"
    graph_path = os.path.join('static', graph_filename)
    plt.savefig(graph_path)
    plt.close(fig) # Close the figure to free up memory

    # 6. Return all results in a dictionary
    return {
        'sentiment': sentiment_result,
        'vader_scores': score,
        'emotions': dict(emotion_counts),
        'graph_url': graph_path
    }

# --- Flask Application ---
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text_to_analyze = data.get('text', '')
    
    if not text_to_analyze:
        return jsonify({'error': 'No text provided.'}), 400

    # Run your complete analysis
    results = analyze_text(text_to_analyze)
    
    # Return the results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)