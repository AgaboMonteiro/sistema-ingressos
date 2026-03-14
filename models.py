from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Usuario:
    id: Optional[int] = None
    nome: str = ""
    email: str = ""
    senha: str = ""
    tipo: str = "cliente" # 'admin' ou 'cliente'

@dataclass
class Ingresso:
    id: Optional[int] = None
    evento: str = ""
    preco: float = 0.0
    quantidade_disponivel: int = 0
    data_evento: str = ""

@dataclass
class CompraIngresso:
    id: Optional[int] = None
    usuario_id: int = 0
    ingresso_id: int = 0
    quantidade: int = 0
    data_compra: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    valor_total: float = 0.0
