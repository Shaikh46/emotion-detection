# Emotion Detection Application

A Python-based web application that detects emotions in text using IBM Watson's Natural Language Processing API.

## Features

- **Emotion Detection**: Analyzes text to detect emotions (anger, disgust, fear, joy, sadness)
- **Flask Web Interface**: User-friendly web form for text input
- **REST API Endpoint**: `/emotionDetector` for programmatic access
- **Error Handling**: Graceful handling of blank inputs and API errors
- **Unit Tests**: Comprehensive test coverage for emotion detection
- **Code Quality**: Linting with pylint for code standards

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shaikh46/emotion-detection.git
cd emotion-detection
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Web Server

Start the Flask development server:
```bash
python server.py
```

The application will be available at `http://localhost:5000`

### Using the Web Interface

1. Open your browser and navigate to `http://localhost:5000`
2. Enter text in the form field
3. Click "Run Emotion Detection"
4. View the emotion analysis results

### API Endpoint

**Endpoint**: `POST /emotionDetector`

**Request Body**:
```json
{
  "textToAnalyze": "Your text here"
}
```

**Response** (Success - 200):
```json
{
  "anger": 0.05,
  "disgust": 0.02,
  "fear": 0.03,
  "joy": 0.85,
  "sadness": 0.05,
  "dominant_emotion": "joy"
}
```

**Response** (Error - 400):
```json
{
  "anger": null,
  "disgust": null,
  "fear": null,
  "joy": null,
  "sadness": null,
  "dominant_emotion": null,
  "error": "Invalid input or API error"
}
```

## Testing

### Running Unit Tests

Execute all unit tests:
```bash
python -m unittest test_emotion_detection.py
```

Run specific test:
```bash
python -m unittest test_emotion_detection.EmotionDetectionTests.test_emotion_joy
```

### Static Code Analysis

Run pylint for code quality checks:
```bash
pylint emotion_detection.py server.py
```

## File Structure

```
emotion-detection/
├── README.md                           # Project documentation
├── requirements.txt                    # Python dependencies
├── emotion_detection.py                # Emotion detection logic
├── server.py                           # Flask web server
├── test_emotion_detection.py           # Unit tests
└── EmotionDetection/
    ├── __init__.py                     # Package initialization
    └── emotion_detection.py            # Module version of detector
```

## Example Output

### Input
```
I love this! It's wonderful and I'm so happy!
```

### Output
```
Emotion Analysis Results:
- Anger: 0.02
- Disgust: 0.01
- Fear: 0.01
- Joy: 0.92
- Sadness: 0.04

Dominant Emotion: joy
```

## Technologies Used

- **Python 3**: Programming language
- **Flask**: Web framework
- **Requests**: HTTP library
- **IBM Watson NLP**: Emotion detection API
- **Pylint**: Code linting tool

## API Reference

### Emotion Detector Function

```python
from EmotionDetection import emotion_detector

result = emotion_detector("I am very happy!")
print(result['dominant_emotion'])
```

## Error Handling

- **Blank Input**: Returns error message "Please enter text to analyze"
- **Invalid Response (400)**: Returns all emotion scores as `None`
- **Network Error**: Returns `None` for the entire response
- **API Unavailable**: Gracefully handles connection errors

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m unittest test_emotion_detection.py`
5. Run linter: `pylint emotion_detection.py server.py`
6. Submit a pull request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions, please open an issue on the GitHub repository.
