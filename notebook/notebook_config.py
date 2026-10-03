import sys
from pathlib import Path

# definindo a rota para acessar a pasta /src
PASTA_RAIZ = Path(__file__).resolve().parent.parent
PASTA_SRC = PASTA_RAIZ / "src"

# dar acesso a pasta
if str(PASTA_SRC) not in sys.path:
    sys.path.append(str(PASTA_SRC))