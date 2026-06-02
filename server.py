from flask import Flask, render_template_string, request, jsonify
from emotion_detection import emotion_detector

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotion Detection Web App</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 40px;
            max-width: 600px;
            width: 100%;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 32px;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 10px;
            color: #333;
            font-weight: 600;
            font-size: 14px;
        }
        
        textarea {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            resize: vertical;
            min-height: 120px;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .button-group {
            display: flex;
            gap: 10px;
        }
        
        button {
            flex: 1;
            padding: 12px 24px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-analyze {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-analyze:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .btn-clear {
            background: #f0f0f0;
            color: #333;
        }
        
        .btn-clear:hover {
            background: #e0e0e0;
        }
        
        .results {
            margin-top: 30px;
            padding: 20px;
            background: #f9f9f9;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            display: none;
        }
        
        .results.show {
            display: block;
        }
        
        .results h3 {
            color: #333;
            margin-bottom: 15px;
            font-size: 18px;
        }
        
        .emotion-scores {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 15px;
        }
        
        .emotion-item {
            background: white;
            padding: 12px;
            border-radius: 6px;
            border: 1px solid #e0e0e0;
        }
        
        .emotion-label {
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            font-weight: 600;
            margin-bottom: 5px;
        }
        
        .emotion-value {
            font-size: 18px;
            font-weight: 700;
            color: #667eea;
        }
        
        .dominant {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            grid-column: 1 / -1;
            text-align: center;
            padding: 15px;
        }
        
        .dominant .emotion-label {
            color: rgba(255, 255, 255, 0.8);
        }
        
        .dominant .emotion-value {
            color: white;
            font-size: 24px;
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #c33;
            margin-top: 20px;
            display: none;
        }
        
        .error.show {
            display: block;
        }
        
        .loading {
            text-align: center;
            color: #667eea;
            display: none;
        }
        
        .loading.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>😊 Emotion Detector</h1>
        <p class="subtitle">Analyze emotions in your text</p>
        
        <form id="emotionForm">
            <div class="form-group">
                <label for="textInput">Enter Text to Analyze:</label>
                <textarea id="textInput" name="textToAnalyze" placeholder="Type or paste your text here..."></textarea>
            </div>
            
            <div class="button-group">
                <button type="submit" class="btn-analyze">Run Emotion Detection</button>
                <button type="reset" class="btn-clear">Clear</button>
            </div>
        </form>
        
        <div class="loading" id="loading">Analyzing emotions...</div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <h3>Emotion Analysis Results</h3>
            <div class="emotion-scores" id="emotionScores"></div>
        </div>
    </div>
    
    <script>
        document.getElementById('emotionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const textToAnalyze = document.getElementById('textInput').value.trim();
            const resultsDiv = document.getElementById('results');
            const errorDiv = document.getElementById('error');
            const loadingDiv = document.getElementById('loading');
            
            resultsDiv.classList.remove('show');
            errorDiv.classList.remove('show');
            loadingDiv.classList.add('show');
            
            if (!textToAnalyze) {
                errorDiv.textContent = '⚠️ Please enter text to analyze';
                errorDiv.classList.add('show');
                loadingDiv.classList.remove('show');
                return;
            }
            
            try {
                const response = await fetch('/emotionDetector', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ textToAnalyze: textToAnalyze })
                });
                
                const data = await response.json();
                loadingDiv.classList.remove('show');
                
                if (data.error) {
                    errorDiv.textContent = '❌ ' + data.error;
                    errorDiv.classList.add('show');
                } else if (data.dominant_emotion === null) {
                    errorDiv.textContent = '❌ Unable to analyze emotions. Please try again.';
                    errorDiv.classList.add('show');
                } else {
                    const emotionScores = document.getElementById('emotionScores');
                    emotionScores.innerHTML = `
                        <div class="emotion-item">
                            <div class="emotion-label">😠 Anger</div>
                            <div class="emotion-value">${(data.anger * 100).toFixed(1)}%</div>
                        </div>
                        <div class="emotion-item">
                            <div class="emotion-label">🤢 Disgust</div>
                            <div class="emotion-value">${(data.disgust * 100).toFixed(1)}%</div>
                        </div>
                        <div class="emotion-item">
                            <div class="emotion-label">😨 Fear</div>
                            <div class="emotion-value">${(data.fear * 100).toFixed(1)}%</div>
                        </div>
                        <div class="emotion-item">
                            <div class="emotion-label">😊 Joy</div>
                            <div class="emotion-value">${(data.joy * 100).toFixed(1)}%</div>
                        </div>
                        <div class="emotion-item">
                            <div class="emotion-label">😢 Sadness</div>
                            <div class="emotion-value">${(data.sadness * 100).toFixed(1)}%</div>
                        </div>
                        <div class="emotion-item dominant">
                            <div class="emotion-label">Dominant Emotion</div>
                            <div class="emotion-value">${data.dominant_emotion.toUpperCase()}</div>
                        </div>
                    `;
                    resultsDiv.classList.add('show');
                }
            } catch (error) {
                loadingDiv.classList.remove('show');
                errorDiv.textContent = '❌ An error occurred. Please try again.';
                errorDiv.classList.add('show');
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the main emotion detection form."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/emotionDetector', methods=['POST'])
def emotion_detector_route():
    """API endpoint for emotion detection."""
    try:
        data = request.get_json()
        text_to_analyze = data.get('textToAnalyze', '').strip()
        
        if not text_to_analyze:
            return jsonify({
                'error': 'Please enter text to analyze',
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }), 400
        
        result = emotion_detector(text_to_analyze)
        
        if result is None:
            return jsonify({
                'error': 'Unable to process the request',
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }), 500
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
