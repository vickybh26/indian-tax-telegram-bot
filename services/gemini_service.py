"""
Google Gemini API service for processing tax queries and document analysis
"""

import os
import logging
from typing import Dict, Any
from google import genai

logger = logging.getLogger(__name__)

class GeminiService:
    """Service for processing tax queries using Google Gemini AI"""
    
    def __init__(self):
        """Initialize Gemini service with API key from environment"""
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-2.5-flash"

    async def process_tax_query(self, query: str, context: str = "") -> Dict[str, Any]:
        """Process a tax-related query using Gemini AI"""
        try:
            # Create comprehensive tax prompt with current context
            full_prompt = f"""You are an expert Indian tax advisor with comprehensive knowledge of Indian Income Tax Act, GST, and related tax laws.

Current Tax Information (FY 2024-25):
- New Regime Tax Slabs: 0% (up to ₹3L), 5% (₹3L-₹6L), 10% (₹6L-₹9L), 15% (₹9L-₹12L), 20% (₹12L-₹15L), 30% (above ₹15L)
- Old Regime Tax Slabs: 0% (up to ₹2.5L), 5% (₹2.5L-₹5L), 20% (₹5L-₹10L), 30% (above ₹10L)
- Standard Deduction: ₹50,000 (old regime), ₹75,000 (new regime)
- 80C Limit: ₹1.5L (old regime only)
- ITR Filing Deadline: July 31, 2025

User Query: {query}

Provide a comprehensive, accurate answer with practical examples where relevant. Include relevant section numbers and official links where applicable."""
            
            if context:
                full_prompt += f"\nAdditional Context: {context}"
            
            # Simple direct API call
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
            
            if not response.text:
                logger.warning("Empty response from Gemini API")
                return self._get_fallback_response(query)
            
            # Return structured response
            return {
                "answer": response.text.strip(),
                "confidence": 0.90,  # High confidence for successful responses
                "relevant_sections": [],
                "official_links": [
                    "https://www.incometax.gov.in/",
                    "https://cleartax.in/s/income-tax-guide"
                ],
                "status": "success"
            }
                
        except Exception as e:
            logger.error(f"Error processing tax query: {e}")
            return self._get_fallback_response(query, error=str(e))
    
    async def analyze_document(self, text_content: str, filename: str) -> Dict[str, Any]:
        """Analyze tax-related document content"""
        try:
            prompt = f"""Analyze this Indian tax document and provide key insights:

Document: {filename}
Content excerpt: {text_content[:2000]}

Provide analysis focusing on:
- Key tax information and figures
- Important dates and deadlines
- Deductions and exemptions
- Action items or recommendations"""

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            if not response.text:
                return {"analysis": "Unable to analyze document", "status": "error"}
            
            return {
                "analysis": response.text.strip(),
                "status": "success"
            }
                
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return {"analysis": f"Error analyzing document: {e}", "status": "error"}
    
    def _get_fallback_response(self, query: str, error: str = None) -> Dict[str, Any]:
        """Generate fallback response when AI processing fails"""
        
        # Provide basic tax information based on common queries
        fallback_answers = {
            "tax slab": "For FY 2024-25, New Regime: 0% (up to ₹3L), 5% (₹3L-₹6L), 10% (₹6L-₹9L), 15% (₹9L-₹12L), 20% (₹12L-₹15L), 30% (above ₹15L). Old Regime: 0% (up to ₹2.5L), 5% (₹2.5L-₹5L), 20% (₹5L-₹10L), 30% (above ₹10L).",
            "80c": "Section 80C allows deduction up to ₹1.5 lakh in the old tax regime for investments in PPF, ELSS, NSC, life insurance premiums, etc. Not available in new regime.",
            "deadline": "ITR filing deadline for FY 2024-25 is July 31, 2025 for individuals. Late filing attracts penalty of ₹5,000 (₹1,000 if income < ₹5 lakh).",
            "hra": "HRA exemption (old regime only): Minimum of (Actual HRA received, 50%/40% of salary, Rent paid - 10% of salary)."
        }
        
        # Try to match query with fallback answers
        query_lower = query.lower()
        fallback_answer = "I'm experiencing technical issues processing your query. Please try again in a few moments."
        
        for key, answer in fallback_answers.items():
            if key in query_lower:
                fallback_answer = answer
                break
        
        base_response = {
            "answer": fallback_answer,
            "confidence": 0.3 if fallback_answer != "I'm experiencing technical issues processing your query. Please try again in a few moments." else 0.0,
            "relevant_sections": [],
            "official_links": [
                "https://www.incometax.gov.in/",
                "https://cleartax.in/s/income-tax-guide"
            ],
            "status": "fallback"
        }
        
        if error:
            base_response["answer"] += f" (Technical error: {error})"
        
        return base_response
