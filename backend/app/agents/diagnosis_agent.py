from app.groq_client import GroqService
from app.csv_store import log_assessment

class DiagnosisAgent:
    """
    DiagnosisAgent — Clinivanta AI Core Diagnostic Engine

    Combines wound measurements + vision caption + research context
    to generate a structured clinical wound assessment report using
    Groq's Llama 3.3 70B model.
    """

    def generate_report(self, measurements: dict, combined_context: str) -> str:
        """
        Generate a structured surgical wound assessment.

        Args:
            measurements: dict with keys: length, width, depth, area, volume
            combined_context: combined text from vision caption + research

        Returns:
            str: Full structured clinical diagnostic report
        """
        length  = measurements.get("length", 0)
        width   = measurements.get("width",  0)
        depth   = measurements.get("depth",  0)
        area    = measurements.get("area",   0)
        volume  = measurements.get("volume", 0)

        prompt = f"""You are Clinivanta AI — a clinical-grade AI diagnostic engine specializing in wound assessment.

WOUND MEASUREMENTS (AI-calculated via YOLO segmentation + depth estimation):
  - Length  : {length} cm
  - Width   : {width} cm
  - Depth   : {depth} cm
  - Area    : {area} cm²
  - Volume  : {volume} cm³

VISION & RESEARCH INTELLIGENCE:
{combined_context[:1500]}

Generate a STRUCTURED SURGICAL WOUND REPORT using EXACTLY these section headers (with ### prefix and colon):

### CLINICAL FINDINGS & CLASSIFICATION:
State the wound type, Wagner grade or NPUAP stage, clinical presentation. Be specific.

### TISSUE COMPOSITION:
- Granulation tissue: X%
- Slough: X%
- Necrosis: X%
- Epithelization: X%

### EXUDATE & INFECTION RISK:
Exudate level (None/Low/Moderate/Heavy), character (serous/purulent/haemoserous), infection indicators, odour, surrounding skin status.

### MD RECOMMENDED CARE PLAN:
Step-by-step priority plan:
1. Debridement approach
2. Dressing type and frequency
3. Offloading / pressure relief
4. Antibiotic / antimicrobial therapy
5. Vascular referral if indicated
6. Next review: X days

Keep language precise, concise, and surgical-grade. Do NOT change the section headers."""
        try:
            report = GroqService.get_mixtral_recommendation(prompt)
            return report
        except Exception as e:
            print(f"DiagnosisAgent error: {e}")
            return (
                f"### CLINICAL FINDINGS & CLASSIFICATION:\n"
                f"Diagnosis generation failed. Manual review required.\n\n"
                f"### TISSUE COMPOSITION:\n"
                f"Data unavailable.\n\n"
                f"### EXUDATE & INFECTION RISK:\n"
                f"Data unavailable.\n\n"
                f"### MD RECOMMENDED CARE PLAN:\n"
                f"Measurements recovered: Area={area}cm², Volume={volume}cm³, Length={length}cm.\n"
                f"Please review manually with clinical staff."
            )
