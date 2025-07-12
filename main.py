from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import re

# Load environment variables
load_dotenv()

app = FastAPI(title="Nibero Comment Filter API")

# Set up CORS to only allow requests from nibero.ir
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://nibero.ir"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Define request model
class CommentRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    post_id: Optional[str] = None

# Define response model
class CommentResponse(BaseModel):
    is_approved: bool
    reason: Optional[str] = None

# Load Persian toxic comment classifier
# Using ParsBERT model fine-tuned for toxicity detection
model_name = "HooshvareLab/bert-fa-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# In production, you would use a fine-tuned model for toxicity detection
# For this example, we'll use a simple keyword-based approach as a fallback
# and then show how to integrate with a proper model

# List of Persian inappropriate words (this is just a placeholder)
inappropriate_words = [
    "فحش", "توهین", "کلمه_نامناسب",  # Add your list of inappropriate words
]

def verify_origin(request: Request):
    """Verify that the request is coming from nibero.ir"""
    origin = request.headers.get("Origin", "")
    if not origin.endswith("nibero.ir"):
        raise HTTPException(status_code=403, detail="Access forbidden: Invalid origin")
    return True

def contains_inappropriate_content(text: str) -> (bool, str):
    """
    Check if the text contains inappropriate content
    Returns: (is_inappropriate, reason)
    """
    # Convert to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    # Check for inappropriate words
    for word in inappropriate_words:
        if word in text_lower:
            return True, f"Contains inappropriate language"
    
    # Here you would integrate with a proper model like:
    # classifier = pipeline("text-classification", model=model_name, tokenizer=tokenizer)
    # result = classifier(text)
    # if result[0]["label"] == "TOXIC" and result[0]["score"] > 0.7:
    #     return True, "Detected toxic content"
    
    # For now, we'll use a simple length check as a placeholder
    if len(text) < 2:
        return True, "Comment is too short"
        
    return False, None

@app.post("/filter-comment", response_model=CommentResponse)
async def filter_comment(comment: CommentRequest, authorized: bool = Depends(verify_origin)):
    """
    Filter a comment and determine if it should be approved
    """
    # Check if the comment contains inappropriate content
    is_inappropriate, reason = contains_inappropriate_content(comment.text)
    
    # Return the result
    return CommentResponse(
        is_approved=not is_inappropriate,
        reason=reason
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
