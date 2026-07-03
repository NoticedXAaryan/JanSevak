"""Locust load testing script for JanSeva webhook."""
import random
from locust import HttpUser, task, between

class JanSevaSimulator(HttpUser):
    wait_time = between(2, 5)
    
    # Common repeated queries to test cache hits
    QUERIES = [
        "What is the procedure for an income certificate?",
        "How can I report a corrupt official?",
        "I need a caste certificate",
        "PM Kisan Samman Nidhi info",
    ]

    @task
    def send_whatsapp_message(self):
        """Simulate an incoming WhatsApp message via Twilio webhook."""
        # Generate a random phone number for the simulated user
        phone_number = f"whatsapp:+1415555{random.randint(1000, 9999)}"
        query = random.choice(self.QUERIES)
        
        # Twilio sends form data
        data = {
            "From": phone_number,
            "Body": query
        }
        
        # Post to the webhook endpoint
        self.client.post("/api/webhook/twilio", data=data)
