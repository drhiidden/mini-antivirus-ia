# AGENTS.md — mini-antivirus-ia

---

## Identidad

| Campo | Valor |
|---|---|
| Nombre | **mini-antivirus-ia** |
| Repo GitHub | `drhiidden/mini-antivirus-ia` |
| Tagline | *Catch what signatures miss.* |
| Licencia | MIT |
| Estado | Alpha — funcional en Windows |
| Plataforma | Windows (event APIs nativas) |

---

## Problema que resuelve

Los antivirus basados en firmas no detectan malware polimórfico ni ataques Zero-Day. mini-antivirus-ia adopta vigilancia basada en comportamiento: monitoriza el árbol de procesos, accesos a ficheros, registro y red, y clasifica patrones mediante ML (RandomForest baseline).

---

## Arquitectura

```
Windows Event APIs (procesos, archivos, registro, red)
         ↓
    Agente ligero (Python, bajo consumo)
         ↓
    Event Bus desacoplado (async)
         ↓    ↘
    SQLite      ML Model (RandomForest)
    (48h hist)  (clasificación comportamiento)
         ↓
    Decisión: ALLOW / ALERT / BLOCK
         ↓
    structlog → SIEM compatible
```

---

## Stack

| Capa | Tecnología |
|---|---|
| Lenguaje | Python 3.x |
| Events | Windows APIs (psutil, winreg, watchdog) |
| ML | scikit-learn (RandomForest) |
| Storage | SQLite |
| Logs | structlog (JSON estructurado) |
| Bus | threading / asyncio queue |

---

## Lógica crítica

1. **Score > 0.7 → ALERT, Score > 0.85 → BLOCK** — umbrales configurables
2. **Event Bus es desacoplado** — el agente de colección y el clasificador son independientes. No bloquear el bus nunca
3. **SQLite es lookback histórico** — no base de datos operacional. TTL 48h por defecto
4. **structlog** — todos los logs en JSON para integración con SIEMs (Splunk, ELK)
5. **No reiniciar el modelo en caliente** — cargar modelo al inicio, no en cada clasificación

---

## Roadmap

- [x] Agente básico de monitorización de procesos
- [x] Event Bus desacoplado
- [x] RandomForest baseline
- [x] SQLite history + structlog
- [ ] Detección de lateral movement (árboles de proceso)
- [ ] Integración con Windows Defender API
- [ ] Modelo de deep learning (LSTM para secuencias de eventos)
- [ ] Dashboard web (Flask/FastAPI) para visualización en tiempo real
- [ ] Export a formato SIEM

---

## Reglas críticas para agentes

1. **Solo Windows** — no intentar portar a Linux/macOS sin refactorizar las APIs de eventos
2. **No bloquear el Event Bus** — todas las operaciones de clasificación deben ser async
3. **Bajo consumo de recursos** — el agente no puede consumir >5% CPU en idle
4. **Falsos positivos > falsos negativos** — es preferible alertar de más que de menos
5. **No hardcodear umbrales** — siempre configurables

---

## Metodología

Desarrollado con [HCP (Human-Code-AI Protocol)](https://github.com/haletheia/human-code-ai-protocol).
