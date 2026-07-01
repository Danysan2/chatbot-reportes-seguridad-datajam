"""Cliente para Evolution API."""
from typing import Optional, Dict, Any

import requests
from loguru import logger

from config.settings import (
    EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE_NAME
)


class EvolutionAPI:
    """Cliente para interactuar con Evolution API."""

    def __init__(self):
        self.base_url = EVOLUTION_API_URL.rstrip("/")
        self.api_key = EVOLUTION_API_KEY
        self.instance_name = EVOLUTION_INSTANCE_NAME
        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json",
        }

    def send_message(self, telefono: str, mensaje: str) -> bool:
        """Envía un mensaje de texto por WhatsApp."""
        url = f"{self.base_url}/message/sendText/{self.instance_name}"

        payload = {
            "number": telefono,
            "text": mensaje,
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Mensaje enviado a {telefono}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Error enviando mensaje a {telefono}: {e}")
            return False

    def get_instance_status(self) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/instance/connectionState/{self.instance_name}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo estado de instancia: {e}")
            return None

    def get_qr_code(self) -> Optional[Dict[str, Any]]:
        url = f"{self.base_url}/instance/connect/{self.instance_name}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error obteniendo QR: {e}")
            return None
