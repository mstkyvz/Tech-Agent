import json
import os
from typing import Dict, Any


def load_config() -> Dict[str, Any]:
    """JSON dosyasını okuyarak konfigürasyon verilerini döndürür."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path) as f:
            return json.load(f)


