"""
Indian tax law context and knowledge base
"""

from datetime import datetime
from typing import Dict, List

class TaxContext:
    """Provides current Indian tax law context and information"""
    
    def __init__(self):
        self.current_fy = "2024-25"
        self.current_ay = "2025-26"
        self.current_date = datetime.now()
    
    def get_current_tax_context(self) -> str:
        """Get comprehensive current tax context"""
        return f"""
        CURRENT TAX YEAR INFORMATION (FY {self.current_fy}, AY {self.current_ay}):
        
        INCOME TAX SLABS (Individual - New Tax Regime):
        - Up to ₹3,00,000: Nil
        - ₹3,00,001 to ₹7,00,000: 5%
        - ₹7,00,001 to ₹10,00,000: 10%
        - ₹10,00,001 to ₹12,00,000: 15%
        - ₹12,00,001 to ₹15,00,000: 20%
        - Above ₹15,00,000: 30%
        
        OLD TAX REGIME SLABS:
        - Up to ₹2,50,000: Nil
        - ₹2,50,001 to ₹5,00,000: 5%
        - ₹5,00,001 to ₹10,00,000: 20%
        - Above ₹10,00,000: 30%
        
        KEY DEDUCTIONS (Old Regime):
        - Section 80C: Up to ₹1,50,000 (EPF, PPF, ELSS, Life Insurance, etc.)
        - Section 80D: Up to ₹25,000 (Health Insurance)
        - Section 80E: Interest on Education Loan (No limit)
        - Section 80G: Donations to specified funds
        - Section 24(b): Home Loan Interest up to ₹2,00,000
        
        IMPORTANT DATES:
        - ITR Filing Deadline: July 31, {self.current_date.year + 1}
        - Last date for tax-saving investments: March 31, {self.current_date.year + 1}
        - TDS Certificate Issue: June 15, {self.current_date.year + 1}
        
        STANDARD DEDUCTION:
        - Salaried: ₹50,000
        - Pensioners: ₹15,000
        
        HRA CALCULATION:
        - 50% of salary (metro cities) or 40% (non-metro)
        - Actual HRA received
        - Rent paid minus 10% of salary
        (Minimum of the three)
        
        TDS RATES (Common):
        - Salary: As per tax slab
        - Interest on FD: 10% (if > ₹40,000)
        - Professional fees: 10%
        - Rent: 10%
        
        GST RATES:
        - Essential goods: 0% or 5%
        - Standard rate: 12% or 18%
        - Luxury items: 28%
        
        OFFICIAL RESOURCES:
        - Income Tax Department: https://www.incometax.gov.in/
        - GST Portal: https://www.gst.gov.in/
        - CBDT: https://www.incometax.gov.in/iec/foportal/
        """
    
    def get_deduction_details(self) -> Dict[str, Dict]:
        """Get detailed deduction information"""
        return {
            "80C": {
                "limit": 150000,
                "description": "Investments in EPF, PPF, ELSS, Life Insurance, Tax-saving FD, etc.",
                "eligible_investments": [
                    "Employee Provident Fund (EPF)",
                    "Public Provident Fund (PPF)",
                    "Equity Linked Savings Scheme (ELSS)",
                    "Life Insurance Premium",
                    "Tax-saving Fixed Deposits",
                    "National Savings Certificate (NSC)",
                    "Principal repayment of Home Loan"
                ]
            },
            "80D": {
                "limit": 25000,
                "description": "Health Insurance Premium",
                "details": {
                    "self_family": 25000,
                    "parents_below_60": 25000,
                    "parents_above_60": 50000,
                    "total_max": 100000
                }
            },
            "80E": {
                "limit": "No limit",
                "description": "Interest on Education Loan",
                "conditions": "For higher education of self, spouse, children, or student for whom you are legal guardian"
            },
            "24b": {
                "limit": 200000,
                "description": "Home Loan Interest Deduction",
                "conditions": "For self-occupied property only"
            }
        }
    
    def get_itr_forms_info(self) -> Dict[str, str]:
        """Get ITR forms information"""
        return {
            "ITR-1": "For salaried individuals with income up to ₹50 lakh",
            "ITR-2": "For individuals with capital gains, foreign assets/income",
            "ITR-3": "For individuals with business/professional income",
            "ITR-4": "For presumptive business income under Section 44AD/44ADA",
            "ITR-5": "For firms, LLP, AOP, BOI",
            "ITR-6": "For companies other than claiming exemption under Section 11",
            "ITR-7": "For trusts, political parties, institutions"
        }
    
    def get_filing_deadlines(self) -> Dict[str, str]:
        """Get important filing deadlines"""
        current_year = self.current_date.year
        return {
            "ITR Filing": f"July 31, {current_year + 1}",
            "Audit Report": f"October 31, {current_year + 1}",
            "Tax Payment": f"March 31, {current_year + 1}",
            "TDS Return Filing": "Quarterly",
            "GST Return Filing": "Monthly/Quarterly"
        }
    
    def get_exemption_limits(self) -> Dict[str, int]:
        """Get various exemption limits"""
        return {
            "basic_exemption_new": 300000,
            "basic_exemption_old": 250000,
            "senior_citizen_exemption": 300000,
            "super_senior_citizen_exemption": 500000,
            "standard_deduction_salary": 50000,
            "standard_deduction_pension": 15000,
            "medical_allowance": 15000
        }
    
    def get_common_tax_scenarios(self) -> List[Dict]:
        """Get common tax calculation scenarios"""
        return [
            {
                "scenario": "Salaried Employee (New Regime)",
                "income": 800000,
                "tax_calculation": "₹3,00,000 - Nil, ₹5,00,000 @ 5% = ₹25,000",
                "total_tax": 25000
            },
            {
                "scenario": "Salaried Employee (Old Regime)",
                "income": 800000,
                "deductions": 150000,
                "taxable_income": 650000,
                "tax_calculation": "₹2,50,000 - Nil, ₹4,00,000 @ 5% = ₹20,000",
                "total_tax": 20000
            }
        ]
