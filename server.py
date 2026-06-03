from flask import Flask, request, jsonify
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector", methods=['GET'])
def emotion_detector_function():
    text_to_analyze = request.args.get('textToAnalyze')
    anger_score, disgust_score, fear_score, joy_score, sadness_score, dominant_emotion = emotion_detector(text_to_analyze)
    if dominant_emotion is None:
        return "Invalid input! Try again."
    output_string = f"For the given statement, the system response is 'anger': {anger_score}, 'disgust': {disgust_score}, 'fear': {fear_score}, 'joy': {joy_score}, 'sadness': {sadness_score}. The dominant emotion is {dominant_emotion}."
    return output_string

@app.route("/")
def render_index_page():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Emotion Analyzer</title>
    </head>
    <body>
        <h1>Emotion Analyzer</h1>
        <form action="/emotionDetector" method="get">
            <input type="text" name="textToAnalyze" placeholder="Enter your statement here..." required>
            <button type="submit">Analyze Emotion</button>
        </form>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
