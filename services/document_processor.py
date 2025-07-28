"""
Document processing service for tax document analysis
"""

import logging
import os
from typing import Optional
import PyPDF2
import io

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Service for processing tax-related documents"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text content from PDF file"""
        try:
            text = ""
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check if PDF is encrypted
                if pdf_reader.is_encrypted:
                    logger.warning(f"PDF is encrypted: {file_path}")
                    return "Error: This PDF is password protected. Please provide an unprotected version."
                
                # Extract text from all pages
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += f"\n--- Page {page_num + 1} ---\n"
                            text += page_text
                    except Exception as e:
                        logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                        continue
                
                if not text.strip():
                    return "Error: Could not extract readable text from this PDF. It may be image-based or corrupted."
                
                # Clean up the extracted text
                text = self._clean_extracted_text(text)
                
                logger.info(f"Successfully extracted text from PDF: {file_path}")
                return text
                
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return "Error: File not found."
        
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {e}")
            return f"Error: Could not process the PDF file. {str(e)}"
    
    def extract_text_from_bytes(self, file_bytes: bytes, filename: str) -> str:
        """Extract text from PDF bytes"""
        try:
            text = ""
            
            # Create a BytesIO object from the bytes
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                logger.warning(f"PDF is encrypted: {filename}")
                return "Error: This PDF is password protected. Please provide an unprotected version."
            
            # Extract text from all pages
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num + 1}: {e}")
                    continue
            
            if not text.strip():
                return "Error: Could not extract readable text from this PDF. It may be image-based or corrupted."
            
            # Clean up the extracted text
            text = self._clean_extracted_text(text)
            
            logger.info(f"Successfully extracted text from PDF bytes: {filename}")
            return text
            
        except Exception as e:
            logger.error(f"Error processing PDF bytes for {filename}: {e}")
            return f"Error: Could not process the PDF file. {str(e)}"
    
    def validate_file(self, file_path: str, filename: str) -> tuple[bool, str]:
        """Validate if file can be processed"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False, "File not found"
            
            # Check file extension
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext not in self.supported_formats:
                return False, f"Unsupported file format. Supported formats: {', '.join(self.supported_formats)}"
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return False, f"File too large. Maximum size: {self.max_file_size // (1024*1024)}MB"
            
            if file_size == 0:
                return False, "File is empty"
            
            return True, "File is valid"
            
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {e}")
            return False, f"Error validating file: {str(e)}"
    
    def _clean_extracted_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Strip whitespace from each line
            cleaned_line = line.strip()
            
            # Skip empty lines but keep page markers
            if cleaned_line or line.startswith('--- Page'):
                cleaned_lines.append(cleaned_line)
        
        # Join lines and normalize spacing
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Remove multiple consecutive newlines
        while '\n\n\n' in cleaned_text:
            cleaned_text = cleaned_text.replace('\n\n\n', '\n\n')
        
        return cleaned_text
    
    def get_document_info(self, file_path: str) -> dict:
        """Get basic information about the document"""
        info = {
            'file_size': 0,
            'page_count': 0,
            'is_encrypted': False,
            'title': '',
            'author': '',
            'creation_date': '',
            'modification_date': ''
        }
        
        try:
            
            if not os.path.exists(file_path):
                return info
            
            info['file_size'] = os.path.getsize(file_path)
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                info['page_count'] = len(pdf_reader.pages)
                info['is_encrypted'] = pdf_reader.is_encrypted
                
                # Get metadata if available
                if pdf_reader.metadata:
                    metadata = pdf_reader.metadata
                    info['title'] = str(metadata.get('/Title', '')) if metadata.get('/Title') else ''
                    info['author'] = str(metadata.get('/Author', '')) if metadata.get('/Author') else ''
                    info['creation_date'] = str(metadata.get('/CreationDate', '')) if metadata.get('/CreationDate') else ''
                    info['modification_date'] = str(metadata.get('/ModDate', '')) if metadata.get('/ModDate') else ''
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting document info for {file_path}: {e}")
            return info
