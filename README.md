# vigia-bots
Avisa al móvil (ntfy) si un bot programado del portátil **no se ha ejecutado**.

- Cada bot, al terminar bien, hace `curl -d "<nombre> ok" https://ntfy.sh/<LATIDO_TOPIC>`.
- GitHub Actions ejecuta `vigia.py` cada día a las 20:37 UTC y comprueba el latido de cada bot en `BOTS_JSON`.
- Los temas van en *secrets* del repo (`LATIDO_TOPIC`, `ALERTA_TOPIC`), nunca en el código.
- Añadir un bot: que envíe su latido y añadirlo a `BOTS_JSON` en `.github/workflows/vigia.yml` (horas máximas < 12, lo que guarda ntfy.sh).
- Ver también: `Cerebro/00-Panel de automatizaciones.md`.
