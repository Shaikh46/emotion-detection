import requests
import json

def emotion_detector(text_to_analyze):
    """
    Detect emotions in the given text using Watson NLP API.
    
    Args:
        text_to_analyze (str): The text to analyze for emotions
    
    Returns:
        dict: Dictionary containing emotion scores and dominant emotion,
              or None/error dict if request fails
    """
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = {"raw_document": {"text": text_to_analyze}}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            emotion = result.get('emotionPredictions', [{}])[0].get('emotion', {})
            
            anger = emotion.get('anger', None)
            disgust = emotion.get('disgust', None)
            fear = emotion.get('fear', None)
            joy = emotion.get('joy', None)
            sadness = emotion.get('sadness', None)
            
            dominant_emotion = max([anger, disgust, fear, joy, sadness], 
                                  key=lambda x: x if x is not None else 0) \
                             if any([anger, disgust, fear, joy, sadness]) else None
            
            if dominant_emotion == anger:
                dominant_emotion = 'anger'
            elif dominant_emotion == disgust:
                dominant_emotion = 'disgust'
            elif dominant_emotion == fear:
                dominant_emotion = 'fear'
            elif dominant_emotion == joy:
                dominant_emotion = 'joy'
            elif dominant_emotion == sadness:
                dominant_emotion = 'sadness'
            
            return {
                'anger': anger,
                'disgust': disgust,
                'fear': fear,
                'joy': joy,
                'sadness': sadness,
                'dominant_emotion': dominant_emotion
            }
        
        elif response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        
        else:
            return None
    
    except Exception as e:
        return None
