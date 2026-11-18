"""Vigía de bots: avisa al móvil si un bot NO ha dado señales de vida en su ventana.

Cada bot, al terminar bien, publica un 'latido' en ntfy (tema LATIDO_TOPIC) con su nombre.
Este script (GitHub Actions, en la nube) comprueba que cada bot latió en las últimas N horas
y, si no, envía una alerta al tema de avisos (ALERTA_TOPIC). Solo librería estándar.
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request

SERVIDOR = "https://ntfy.sh"
LATIDO = os.environ["LATIDO_TOPIC"]
ALERTA = os.environ["ALERTA_TOPIC"]
# bot -> horas máximas sin latido (ntfy.sh guarda los mensajes ~12 h)
BOTS: dict[str, int] = json.loads(os.environ.get("BOTS_JSON", '{"pinterest": 6}'))


def latidos(horas: int) -> list[dict]:
    url = f"{SERVIDOR}/{LATIDO}/json?poll=1&since={horas}h"
    with urllib.request.urlopen(url, timeout=30) as r:
        return [json.loads(l) for l in r.read().decode().splitlines() if l.strip()]


def avisar(titulo: str, texto: str) -> None:
    req = urllib.request.Request(f"{SERVIDOR}/{ALERTA}", data=texto.encode(), method="POST",
                                 headers={"Title": titulo, "Priority": "high", "Tags": "rotating_light"})
    urllib.request.urlopen(req, timeout=30).read()


def main() -> int:
    faltan = []
    for bot, horas in BOTS.items():
        msgs = [m for m in latidos(horas) if m.get("event") == "message" and m.get("message", "").startswith(bot)]
        ultimo = max((m["time"] for m in msgs), default=None)
        estado = "OK" if ultimo else "SIN LATIDO"
        print(f"{bot}: {estado}" + (f" (hace {int((time.time() - ultimo) / 60)} min)" if ultimo else ""))
        if not ultimo:
            faltan.append(f"{bot} (sin señales en {horas} h)")
    if faltan:
        avisar("Vigia: un bot no se ha ejecutado",
               "No hay latido de: " + ", ".join(faltan) + ". Portatil apagado o tarea caida? Revisa el Panel de automatizaciones.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
