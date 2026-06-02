import unittest
from EmotionDetection.emotion_detection import emotion_detector

class EmotionDetectionTests(unittest.TestCase):
    """
    Unit tests for the emotion_detector function.
    Tests various emotions to ensure proper detection.
    """
    
    def test_emotion_joy(self):
        """
        Test emotion detection for joy.
        """
        result = emotion_detector('I love this so much!')
        self.assertEqual(result['dominant_emotion'], 'joy')
    
    def test_emotion_anger(self):
        """
        Test emotion detection for anger.
        """
        result = emotion_detector('I am so angry and furious!')
        self.assertEqual(result['dominant_emotion'], 'anger')
    
    def test_emotion_disgust(self):
        """
        Test emotion detection for disgust.
        """
        result = emotion_detector('This is absolutely disgusting and repulsive!')
        self.assertEqual(result['dominant_emotion'], 'disgust')
    
    def test_emotion_sadness(self):
        """
        Test emotion detection for sadness.
        """
        result = emotion_detector('I am very sad and unhappy.')
        self.assertEqual(result['dominant_emotion'], 'sadness')
    
    def test_emotion_fear(self):
        """
        Test emotion detection for fear.
        """
        result = emotion_detector('I am scared and terrified!')
        self.assertEqual(result['dominant_emotion'], 'fear')

if __name__ == '__main__':
    unittest.main()
