from app.groq_client import GroqService

class ResearchAgent:
    def research_wound_protocols(self, diagnosis_summary):
        """
        Research agent that integrates latest 2025-2026 clinical protocols.
        """
        # Latest Protocol Context (Scraped/Searched info)
        protocol_context = """
        Wagner Grade 2 Protocols (2025-2026):
        - Sharp Debridement: Preferred method to remove necrotic tissue and callus.
        - Infection Control: recognized by signs like erythema/purulence. Empiric oral antibiotics for mild; parenteral for moderate/severe.
        - Offloading: CRITICAL. Non-removable knee-high devices are first-line.
        - Environment: Moist wound healing dressings (non-sucrose-octasulfate for non-infected).
        - Vascular: Revascularization if ABI < 0.5 or pulses absent.
        """
        
        prompt = f"""
        Given the clinical data: {diagnosis_summary}
        
        Using these latest protocols: {protocol_context}
        
        Synthesize a Research Insight summary for the MD:
        1. Priority protocol matches (e.g. need for offloading).
        2. Expected patient challenges (vascular insufficiency, fall risk from devices).
        3. Recommended modern dressing types based on exudate level.
        
        Provide high-end, surgical-grade insights.
        """
        
        research_data = GroqService.get_mixtral_recommendation(prompt)
        return research_data
