import os
import random
from data_validator import validate_email, validate_phone

class ChatManager:
    def __init__(self):
        self.interview_flow = {
            "greeting": "collect_basic_info",
            "collect_basic_info": "experience",
            "experience": "technical_skills",
            "technical_skills": "scenario_questions",
            "scenario_questions": "candidate_questions",
            "candidate_questions": "complete"
        }
        
    def process_message(self, message, current_step, candidate_info):
        """Process user message based on the current interview step"""
        response = {
            "message": "",
            "new_step": current_step,
            "candidate_info": {}
        }
        
        # Handle different steps of the interview process
        if current_step == "greeting":
            response["message"] = "Great to meet you! Before we dive into your technical experience, could you please share your name, email address, and phone number?"
            response["new_step"] = self.interview_flow[current_step]
            
        elif current_step == "collect_basic_info":
            # Extract basic information
            name = self._extract_name(message)
            email = self._extract_email(message)
            phone = self._extract_phone(message)
            
            if name and email and phone and validate_email(email) and validate_phone(phone):
                response["candidate_info"] = {
                    "name": name,
                    "email": email,
                    "phone": phone
                }
                response["message"] = f"Thanks {name}! Now I'd like to learn about your professional experience. Could you briefly describe your current role and relevant work experience?"
                response["new_step"] = self.interview_flow[current_step]
            else:
                # Ask for missing or invalid information
                missing_info = []
                if not name:
                    missing_info.append("name")
                if not email or not validate_email(email):
                    missing_info.append("valid email address")
                if not phone or not validate_phone(phone):
                    missing_info.append("valid phone number")
                
                response["message"] = f"I need a bit more information. Could you please provide your {', '.join(missing_info)}?"
        
        elif current_step == "experience":
            # Extract experience information
            response["candidate_info"] = {
                "experience": message
            }
            response["message"] = "Thanks for sharing your experience. Let's talk about your technical skills. What programming languages and frameworks are you most comfortable with? Please rate your proficiency in each (beginner, intermediate, advanced)."
            response["new_step"] = self.interview_flow[current_step]
            
        elif current_step == "technical_skills":
            response["candidate_info"] = {
                "technical_skills": message
            }
            response["message"] = "Great! Now let's discuss a scenario. How would you approach debugging a complex application that's experiencing performance issues in production? What steps would you take to identify and resolve the problem?"
            response["new_step"] = self.interview_flow[current_step]
            
        elif current_step == "scenario_questions":
            response["candidate_info"] = {
                "scenario_response": message
            }
            response["message"] = "Thanks for your insights. Do you have any questions about the role, team, or company culture that I might be able to help with?"
            response["new_step"] = self.interview_flow[current_step]
            
        elif current_step == "candidate_questions":
            response["candidate_info"] = {
                "candidate_questions": message
            }
            response["message"] = "Thank you for your time today! I've collected all the information needed for our initial screening. Our hiring team will review your responses and reach out to you soon with next steps. Have a great day!"
            response["new_step"] = self.interview_flow[current_step]
            
        return response
    
    def _extract_name(self, message):
        """Extract name from message - simple implementation"""
        # This is a simplified version. In a real app, you might use NLP or more sophisticated parsing
        words = message.split()
        if len(words) >= 2:
            # Assume first two words could be a name
            return " ".join(words[:2])
        elif len(words) >= 1:
            return words[0]
        return None
    
    def _extract_email(self, message):
        """Extract email from message"""
        import re
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, message)
        return emails[0] if emails else None
    
    def _extract_phone(self, message):
        """Extract phone number from message"""
        import re
        # Match various phone number formats
        phone_pattern = r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b'
        phones = re.findall(phone_pattern, message)
        return phones[0] if phones else None
