import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class EmotionDetector:
    def __init__(self):
        self.model_name = "SamLowe/roberta-base-go_emotions"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        
        # Define emotion labels
        self.emotion_labels = [
            "admiration", "amusement", "anger", "annoyance", "approval", "caring",
            "confusion", "curiosity", "desire", "disappointment", "disapproval",
            "disgust", "embarrassment", "excitement", "fear", "gratitude", "grief",
            "joy", "love", "nervousness", "optimism", "pride", "realization",
            "relief", "remorse", "sadness", "surprise"
        ]
        
        # Group emotions
        self.emotion_groups = {
            "positive": ["admiration", "amusement", "approval", "caring", "excitement", 
                        "gratitude", "joy", "love", "optimism", "pride", "relief"],
            "negative": ["anger", "annoyance", "disappointment", "disapproval", "disgust",
                        "embarrassment", "fear", "grief", "remorse", "sadness"],
            "neutral": ["confusion", "curiosity", "desire", "realization", "surprise", "nervousness"]
        }

    def detect_emotions_for_text(self, text):
        """Analyze emotions for a single piece of text"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        outputs = self.model(**inputs)
        probs = torch.sigmoid(outputs.logits).squeeze().detach().numpy()
        
        emotions = [
            {"emotion": emotion, "score": float(score)} 
            for emotion, score in zip(self.emotion_labels, probs)
        ]
        emotions.sort(key=lambda x: x['score'], reverse=True)
        
        top_emotions = emotions[:5]
        
        group_scores = {group: 0.0 for group in self.emotion_groups.keys()}
        for emotion in top_emotions:
            for group, group_emotions in self.emotion_groups.items():
                if emotion["emotion"] in group_emotions:
                    group_scores[group] += emotion["score"]
        
        dominant_group = max(group_scores.items(), key=lambda x: x[1])
        intensity = sum(e["score"] for e in emotions[:3]) / 3
        
        return {
            "emotions": [
                {
                    "emotion": e["emotion"],
                    "score": round(float(e["score"]), 3),
                    "group": next(
                        group for group, emotions in self.emotion_groups.items() 
                        if e["emotion"] in emotions
                    )
                } 
                for e in top_emotions
            ],
            "dominant_group": {
                "name": dominant_group[0],
                "score": round(float(dominant_group[1]), 3)
            },
            "emotional_intensity": round(float(intensity), 3),
            "emotion_vector": [float(score) for score in probs]
        }

    def calculate_emotional_similarity(self, vector1, vector2):
        """Calculate cosine similarity between two emotion vectors"""
        return float(cosine_similarity(
            np.array(vector1).reshape(1, -1),
            np.array(vector2).reshape(1, -1)
        )[0][0])

    def analyze_emotional_alignment(self, event_emotions, thought_emotions):
        """Analyze how well the thought emotions align with the event emotions"""
        similarity_score = self.calculate_emotional_similarity(
            event_emotions["emotion_vector"],
            thought_emotions["emotion_vector"]
        )
        
        event_top_emotions = set(e["emotion"] for e in event_emotions["emotions"][:3])
        thought_top_emotions = set(e["emotion"] for e in thought_emotions["emotions"][:3])
        shared_emotions = event_top_emotions.intersection(thought_top_emotions)
        
        same_dominant_group = (
            event_emotions["dominant_group"]["name"] == 
            thought_emotions["dominant_group"]["name"]
        )
        
        return {
            "similarity_score": round(similarity_score, 3),
            "shared_top_emotions": list(shared_emotions),
            "same_dominant_group": same_dominant_group,
            "alignment_level": "high" if similarity_score > 0.8 else
                              "moderate" if similarity_score > 0.5 else "low"
        }

    def analyze(self, event, thoughts):
        """Main method to analyze emotions in both event and thoughts"""
        try:
            event_emotions = self.detect_emotions_for_text(event)
            thought_emotions = self.detect_emotions_for_text(thoughts)
            alignment = self.analyze_emotional_alignment(event_emotions, thought_emotions)
            
            return {
                "event_analysis": {
                    "text": event,
                    "emotions": event_emotions["emotions"],
                    "dominant_group": event_emotions["dominant_group"],
                    "emotional_intensity": event_emotions["emotional_intensity"]
                },
                "thought_analysis": {
                    "text": thoughts,
                    "emotions": thought_emotions["emotions"],
                    "dominant_group": thought_emotions["dominant_group"],
                    "emotional_intensity": thought_emotions["emotional_intensity"]
                },
                "emotional_alignment": alignment
            }
            
        except Exception as e:
            raise Exception(f"Error in emotion analysis: {str(e)}")

