"""
Google Gemini AI service for tax query processing
"""

import json
import logging
import os
from typing import Dict, Any, Optional

from google import genai
from google.genai import types
from pydantic import BaseModel

from utils.tax_context import TaxContext

logger = logging.getLogger(__name__)

class TaxResponse(BaseModel):
    """Structured response model for tax queries"""
    answer: str
    confidence: float
    relevant_sections: list[str] = []
    official_links: list[str] = []
    disclaimer: str = ""

class GeminiService:
    """Service for interacting with Google Gemini AI API"""
    
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.tax_context = TaxContext()
    
    async def process_tax_query(self, query: str) -> Dict[str, Any]:
        """Process a tax-related query using Gemini AI"""
        try:
            # Build the prompt with Indian tax context
            system_prompt = self._build_tax_system_prompt()
            user_prompt = self._build_user_prompt(query)
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=user_prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    response_mime_type="application/json",
                    response_schema=TaxResponse,
                    temperature=0.3,  # Lower temperature for more factual responses
                    max_output_tokens=2048
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                logger.info(f"Processed tax query successfully: {query[:50]}...")
                return result
            else:
                raise ValueError("Empty response from Gemini API")
                
        except Exception as e:
            logger.error(f"Error processing tax query: {e}")
            return self._get_fallback_response(query)
    
    async def analyze_tax_document(self, document_text: str, filename: str) -> Dict[str, Any]:
        """Analyze a tax document using Gemini AI"""
        try:
            system_prompt = self._build_document_analysis_prompt()
            user_prompt = f"""
            Analyze this tax document: {filename}
            
            Document content:
            {document_text[:8000]}  # Limit content to avoid token limits
            
            Please provide:
            1. Document type identification
            2. Key tax information extracted
            3. Important dates and deadlines
            4. Potential issues or recommendations
            5. Relevant tax sections or forms
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    types.Content(role="user", parts=[types.Part(text=user_prompt)])
                ],
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                    max_output_tokens=2048
                )
            )
            
            if response.text:
                logger.info(f"Analyzed document successfully: {filename}")
                return {
                    "analysis": response.text,
                    "document_name": filename,
                    "status": "success"
                }
            else:
                raise ValueError("Empty response from Gemini API")
                
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            return {
                "analysis": "Unable to analyze the document at this time. Please try again later.",
                "document_name": filename,
                "status": "error"
            }
    
    def _build_tax_system_prompt(self) -> str:
        """Build system prompt for tax queries"""
        return f"""
        You are an expert Indian tax advisor with comprehensive knowledge of:
        
        1. Income Tax Act, 1961 and all amendments
        2. Current tax slabs and rates for FY 2024-25
        3. Deductions under Chapter VI-A (80C, 80D, 80E, etc.)
        4. TDS provisions and rates
        5. ITR forms and filing requirements
        6. GST basics and compliance
        7. Capital gains taxation
        8. Tax planning strategies
        
        IMPORTANT GUIDELINES:
        - Provide accurate information based on current Indian tax laws
        - Always include relevant section numbers from the Income Tax Act
        - Provide practical examples when helpful
        - Include official government links when applicable
        - Add appropriate disclaimers about consulting tax professionals
        - Use clear, simple language accessible to common taxpayers
        - Structure responses with bullet points and clear sections
        
        CONTEXT:
        {self.tax_context.get_current_tax_context()}
        
        Always respond in JSON format with the following structure:
        - answer: Detailed response to the query
        - confidence: Confidence level (0.0 to 1.0)
        - relevant_sections: List of relevant IT Act sections
        - official_links: List of official government resource links
        - disclaimer: Appropriate disclaimer text
        """
    
    def _build_user_prompt(self, query: str) -> str:
        """Build user prompt for tax queries"""
        return f"""
        Tax Query: {query}
        
        Please provide a comprehensive answer addressing:
        1. Direct answer to the question
        2. Relevant tax provisions and section numbers
        3. Practical implications or examples
        4. Current rates/limits if applicable
        5. Filing requirements if relevant
        6. Official resources for more information
        
        Focus on accuracy and practical applicability for Indian taxpayers.
        """
    
    def _build_document_analysis_prompt(self) -> str:
        """Build system prompt for document analysis"""
        return """
        You are an expert Indian tax document analyzer. Your task is to:
        
        1. Identify the type of tax document (Form 16, ITR, TDS certificate, etc.)
        2. Extract key financial information (income, tax paid, deductions, etc.)
        3. Identify important dates (due dates, assessment year, etc.)
        4. Highlight potential issues or discrepancies
        5. Provide actionable recommendations
        6. Reference relevant tax sections or forms
        
        Provide clear, structured analysis that helps taxpayers understand their documents.
        Focus on accuracy and practical insights.
        """
    
    def _get_fallback_response(self, query: str) -> Dict[str, Any]:
        """Provide fallback response when API fails"""
        return {
            "answer": "I'm currently unable to process your tax query due to technical issues. Please try again in a few moments or contact a tax professional for immediate assistance.",
            "confidence": 0.0,
            "relevant_sections": [],
            "official_links": ["https://www.incometax.gov.in/"],
            "disclaimer": "This is a fallback response due to technical difficulties. Please consult a qualified tax advisor for accurate information."
        }
