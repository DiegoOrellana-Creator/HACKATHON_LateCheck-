import json
import re
from PIL import Image
from google import genai

API_KEY = "AQ.Ab8RN6IZY42_LlOoS_ZgwhDqecfBV7zOdgbs1k239dbIflRj5A"

class GeminiModel:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.model_id = "gemini-1.5-flash"
        
        # PROMPT SIMPLE Y DIRECTO
        self.prompt = """
        Eres un agrónomo experto en Santa Cruz, Bolivia.
        
        Analiza esta imagen de una hoja de cultivo y responde SOLO con este formato JSON:
        
        {
            "crop": "nombre del cultivo (Soja, Maiz, Caña de azúcar, Girasol, Arroz, Algodon, o Desconocido)",
            "disease": "nombre de la enfermedad o plaga (Roya asiática, Mancha marrón, Tizón, Carbón, Defoliadores, Sano, etc.)",
            "confidence": 0-100,
            "symptoms": ["sintoma1", "sintoma2"],
            "treatment": "tratamiento recomendado",
            "severity": "leve/moderado/grave"
        }
        
        IMPORTANTE - Características de hojas:
        - CAÑA DE AZÚCAR: hoja MUY LARGA, ESTRECHA, como una cinta de 1 metro
        - SOJA: hoja con 3 folíolos (trifoliada)
        - MAÍZ: hoja larga, ancha, con nervadura central marcada
        
        Responde SOLO el JSON, sin texto adicional.
        """
    
    def predict(self, image_path: str) -> dict:
        try:
            img = Image.open(image_path)
            
            # Redimensionar para mejorar velocidad
            if img.size[0] > 1024 or img.size[1] > 1024:
                img.thumbnail((1024, 1024))
            
            print(f"🔍 Analizando: {image_path}")
            
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[self.prompt, img]
            )
            
            print(f"📝 Respuesta Gemini: {response.text[:300]}")
            
            # Extraer JSON
            result = self._extract_json(response.text)
            
            # Corrección manual si no detectó bien
            result = self._manual_correction(result, response.text)
            
            return result
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return self._error_response(str(e))
    
    def _extract_json(self, text: str) -> dict:
        """Extrae JSON de la respuesta"""
        try:
            # Buscar patrón JSON
            match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
        except:
            pass
        
        # Si no hay JSON, analizar texto plano
        return self._parse_plain_text(text)
    
    def _parse_plain_text(self, text: str) -> dict:
        """Extrae información de texto plano"""
        text_lower = text.lower()
        
        # Identificar cultivo por palabras clave
        crop = "Desconocido"
        if "caña" in text_lower or "cana" in text_lower:
            crop = "Caña de azúcar"
        elif "soja" in text_lower or "soya" in text_lower or "trifoliada" in text_lower:
            crop = "Soja"
        elif "maíz" in text_lower or "maiz" in text_lower:
            crop = "Maíz"
        
        # Identificar enfermedad
        disease = "No identificado"
        if "sano" in text_lower or "saludable" in text_lower:
            disease = "Sano"
        elif "roya" in text_lower:
            disease = "Roya asiática"
        elif "mancha" in text_lower:
            disease = "Mancha foliar"
        elif "defoliador" in text_lower or "perforación" in text_lower or "insecto" in text_lower:
            disease = "Daño por insectos defoliadores"
        elif "carbón" in text_lower:
            disease = "Carbón"
        
        return {
            "crop": crop,
            "disease": disease,
            "confidence": 70,
            "symptoms": ["Observar en campo para confirmar"],
            "treatment": "Consultar con técnico especialista",
            "severity": "leve"
        }
    
    def _manual_correction(self, result: dict, raw_response: str) -> dict:
        """Corrige manualmente basado en palabras clave"""
        raw_lower = raw_response.lower()
        
        # Si detectó caña en la respuesta pero no en crop
        if result.get("crop") == "Desconocido" and ("caña" in raw_lower or "cana" in raw_lower):
            result["crop"] = "Caña de azúcar"
            result["confidence"] = max(result.get("confidence", 0), 75)
        
        # Si detectó soya
        if result.get("crop") == "Desconocido" and ("soja" in raw_lower or "soya" in raw_lower):
            result["crop"] = "Soja"
        
        # Si detectó enfermedad pero crop desconocido
        if result.get("crop") == "Desconocido" and result.get("disease") != "No identificado":
            # Intentar inferir cultivo por enfermedad
            disease = result.get("disease", "").lower()
            if "roya" in disease:
                result["crop"] = "Soja (probable)"
        
        return result
    
    def _error_response(self, message: str) -> dict:
        return {
            "crop": "Error de conexión",
            "disease": "No se pudo analizar",
            "confidence": 0,
            "symptoms": [],
            "treatment": f"Error técnico: {message[:150]}",
            "severity": "desconocido"
        }