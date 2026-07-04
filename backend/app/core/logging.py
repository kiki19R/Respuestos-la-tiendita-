"""Sistema de logging de la aplicación"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Crear directorio de logs si no existe
Log_DIR = Path("logs")
Log_DIR.mkdir(exist_ok=True)

# Configurar formato de logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Logger para aplicación
app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)

# Handler para consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(console_formatter)

# Handler para archivo
file_handler = logging.FileHandler(
    Log_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(file_formatter)

# Agregar handlers
app_logger.addHandler(console_handler)
app_logger.addHandler(file_handler)

# Logger para auditoría
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
audit_file_handler = logging.FileHandler(
    Log_DIR / f"audit_{datetime.now().strftime('%Y%m%d')}.log"
)
audit_file_handler.setLevel(logging.INFO)
audit_file_handler.setFormatter(file_formatter)
audit_logger.addHandler(audit_file_handler)


def log_user_action(user_id: int, action: str, details: str = ""):
    """Registra una acción de usuario para auditoría"""
    audit_logger.info(f"Usuario {user_id} - {action} - {details}")
