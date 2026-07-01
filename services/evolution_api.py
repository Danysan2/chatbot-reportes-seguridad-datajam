"""Cliente para Evolution API."""
import requests
from typing import Optional, Dict, Any
from loguru import logger

from config.settings import (
    EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
)


class EvolutionAPI:
    """Cliente para interactuar con Evolution API."""
    
    def __init__(self):
        """Inicializa el cliente de Evolution API."""
        self.base_url = EVOLUTION_API_URL.rstrip('/')
        self.api_key = EVOLUTION_API_KEY
        self.instance_name = EVOLUTION_INSTANCE_NAME
        self.headers = {
            'apikey': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def send_message(self, telefono: str, mensaje: str) -> bool:
        """Envía un mensaje de texto por WhatsApp."""
        url = f"{self.base_url}/message/sendText/{self.instance_name}"

        payloads = [
            {"number": telefono, "textMessage": {"text": mensaje}},
            {"number": telefono, "text": mensaje},
        ]

        for i, payload in enumerate(payloads):
            try:
                logger.debug("Intento {} POST {} payload={}", i + 1, url, payload)
                response = requests.post(url, json=payload, headers=self.headers, timeout=10)
                response.raise_for_status()
                logger.info("Mensaje de WhatsApp enviado (formato {})", i + 1)
                return True
            except requests.exceptions.HTTPError as e:
                logger.warning(
                    "Intento {} falló: status={} body={}",
                    i + 1, e.response.status_code, e.response.text[:500]
                )
            except requests.exceptions.RequestException as e:
                logger.warning("Intento {} falló: {}", i + 1, type(e).__name__)

        logger.error("No se pudo enviar mensaje de WhatsApp con ningún formato")
        return False
    
    def get_instance_status(self) -> Optional[Dict[str, Any]]:
        """Obtiene el estado de la instancia."""
        url = f"{self.base_url}/instance/connectionState/{self.instance_name}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo estado de instancia: {e}")
            return None
    
    def get_qr_code(self) -> Optional[Dict[str, Any]]:
        """Obtiene el código QR para conectar WhatsApp."""
        url = f"{self.base_url}/instance/connect/{self.instance_name}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo QR: {e}")
            return None
