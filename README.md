# Orquestador de *swarms* de agentes LLM agnóstico al modelo y al dominio

**Julián Andrés Mendoza Castro · Esteban Gaviria Zambrano**
Inteligencia Artificial (G1), Universidad Icesi, Cali, Colombia · octubre de 2026

Un orquestador reina–obreros en Python que corre el mismo código sobre la API de DeepSeek o sobre modelos locales en Ollama, y en cualquier dominio descrito como datos. Con él medimos cuánto cuesta y cuánto aporta coordinar agentes.

Comparamos el agente único, una topología jerárquica y una malla con 2 y 4 obreros, sobre `deepseek-flash` sin razonamiento extendido, en tres dominios: GSM8K-Platinum, MATH-500 nivel 5 y un plan de viaje a Cartagena.

**Resultado principal** (195 corridas, 921 llamadas, USD 0.22):

| | GSM8K-Platinum | MATH-500 nivel 5 | Cartagena |
|---|---|---|---|
| Calidad del agente único | 1.00 | 1.00 | 1.00 |
| Mejor calidad de un *swarm* | 1.00 | 1.00 | 1.00 |
| Costo por corrida frente al agente único | 5.1× – 16.6× | 2.7× – 9.4× | 3.5× – 14.5× |

Ninguna configuración superó al agente único en calidad, y el costo de la malla crece con n² por su ronda de revisión. El paper (`paper/main.pdf`) presenta los detalles y las limitaciones, entre ellas el efecto techo y que la rúbrica de Cartagena la aplicó a ciegas un evaluador LLM, no humanos.

## Contenido

```
notebook/
  2026.10.07_Demo_Swarm_Notebook_EN_V3.4.ipynb   cuaderno final, ejecutado (con salidas)
  results_deepseek/      experimento principal
    runs.jsonl           una fila por corrida (respuesta final, tokens, costo, latencia, fallos)
    calls.jsonl          una fila por llamada al LLM
    spend_ledger.jsonl   cada llamada facturada (verificaciones, pilotos, matriz, juez)
    judge.jsonl          juez LLM secundario (Cartagena)
    human_eval/          respuestas ciegas, rúbrica, calificaciones y clave
    figures/             figuras del cuaderno
  results_ollama/        piloto local con llama3.2:3b y qwen2.5:3b (portabilidad)
  archive/               pilotos descartados que documentan dos decisiones del paper
    results_ollama_pilot0_original_gsm8k/   etiqueta errónea del GSM8K original
    results_deepseek_pilot0_max1024/        respuestas truncadas con 1 024 tokens de salida
paper/
  main.tex, main.pdf     artículo (IEEE, español)
  make_assets.py         genera las figuras y numbers.json a partir de notebook/results_*
  figs/                  figuras del artículo
  IEEEtran.cls           clase IEEE (plantilla de conferencia 2024)
  build_local.sh, make_fonts.sh   compilación local sin las fuentes Times de TeX
docs/
  factcheck.md           verificación de fuentes primarias usada para las referencias
```

## Requisitos

- Python 3.11 o superior: `pip install -r requirements.txt`.
- Para el experimento principal, una API key de DeepSeek.
- Para el backend local, [Ollama](https://ollama.com) con `llama3.2:3b` y `qwen2.5:3b`.

## Reproducir el cuaderno

Abra Jupyter desde la carpeta `notebook/`; las rutas de datos y resultados son relativas a ella.

- **Sin costo, solo el pipeline.** Ponga `BACKEND = "mock"` en la sección 1 y ejecute todo. Los resultados van a `results_mock/`, que git ignora.
- **Con los resultados publicados.** Con `BACKEND = "deepseek"`, cada corrida tiene un identificador determinista, así que el cuaderno reutiliza las 195 corridas de `results_deepseek/` y no las repite. Solo hace una llamada de verificación y el demo didáctico (unos centavos).
- **La API key.** Expórtela antes de abrir Jupyter (`export DEEPSEEK_API_KEY=...`) o copie `.env.example` a `.env`. Si no la encuentra, el cuaderno la pide con una entrada oculta. Nunca se escribe en el cuaderno ni en los resultados, y `.env` está en `.gitignore`.
- **Tope de gasto.** `MAX_SPEND_USD` (0.50) detiene cualquier ejecución que pueda superarlo.
- **Datos.** GSM8K-Platinum y MATH-500 se descargan solos de Hugging Face en `notebook/data/` (ignorada por git).

## Reconstruir el paper

```bash
python paper/make_assets.py     # figuras y numbers.json desde notebook/results_*
```

- **En Overleaf o con un TeX Live completo:** suba `main.tex`, `IEEEtran.cls` y `figs/`, y compile con pdfLaTeX dos veces.
- **Si su TeX no trae las fuentes Times (`ptm`):** ejecute `paper/build_local.sh`. Genera un clon de Times con las fuentes URW del sistema (necesita `t1utils` y las fuentes `urw-base35`).

## Datos y licencias

- **Código:** licencia MIT (ver `LICENSE`).
- **GSM8K-Platinum:** Vendrow et al., 2025; MIT.
- **MATH-500:** Lightman et al., 2023, subconjunto de MATH (Hendrycks et al., 2021); MIT. No se redistribuye; el cuaderno lo descarga.
- **Respuestas de Cartagena:** las generó `deepseek-flash` y se incluyen como resultados del experimento.
