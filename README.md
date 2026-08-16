# ScriptLab

En samling tutorial-exempel för Python och PowerShell med fokus på praktiska arbetsflöden och grundläggande AI-användning.

### Kort om projektet
ScriptLab innehåller Jupyter-notebooks, scripts och PowerShell-exempel som hjälper nybörjare och mellanliggande användare att lära sig hur man använder Python och PowerShell i praktiska scenarier — inklusive enklare AI-exempel, datahantering och automation.

### Varför (beskrivning / syfte)
Målet är att erbjuda lättillgängliga, hands-on-exempel som:
- Förklarar grundläggande Python- och PowerShell-mönster
- Visar hur man kombinerar skript och notebooks i arbetsflöden
- Introducerar enkla AI-exempel (t.ex. API-anrop eller transformer-exempel)
- Fungerar som en steg-för-steg-tutorial för egna experiment

### Projektstruktur / filöversikt
- notebooks/                — Jupyter-notebooks (.ipynb) organiserade efter ämne
- scripts/                  — Körbara Python-skript (.py) för demos och utilities
- powershell/               — PowerShell-skript (.ps1) och moduler
- data/                     — Exempeldataset eller testfiler (om delade)
- requirements.txt          — Pythonberoenden
- LICENSE                   — Licensfil (t.ex. MIT)
- .gitignore                — Ignorera filer som inte bör committas
- README.md                 — Denna fil

Obs: Jag planerar att konsolidera separata .ipynb-filer till en huvudnotebook (t.ex. notebooks/ScriptLab.ipynb) för enklare navigering.

### Installation / krav
Rekommenderade minimikrav:
- Python 3.10+ (justera efter behov)
- PowerShell 7+ (för PowerShell-skript på macOS/Linux/Windows)
- Git

### Steg för att komma igång:
1. Klona repot

   git clone https://github.com/steble70/scriptlab.git
   cd scriptlab

2. Skapa och aktivera en virtuell miljö (valfritt men rekommenderas)
   python -m venv .venv
   - macOS / Linux
   source .venv/bin/activate
   - Windows PowerShell
   .\.venv\Scripts\Activate.ps1

3. Installera Pythonberoenden
   pip install -r requirements.txt

4. Starta Jupyter Lab (om du vill köra notebooks)

   pip install jupyterlab
   jupyter lab

Kom igång / användningsexempel

- Kör en notebook
  - Öppna jupyter lab och navigera till notebooks/ och välj en notebook, t.ex. notebooks/01-intro-python.ipynb

- Kör ett Python-skript
  - python scripts/example_data_processing.py --input data/sample.csv --output data/out.csv

- Kör ett PowerShell-skript
  - pwsh ./powershell/example-script.ps1 -Param1 Value

### Tips för AI-exempel
- Om notebooks eller skript använder API-nycklar (t.ex. OpenAI) — exportera nyckeln som en miljövariabel eller använd en lokal .env-fil som ignoreras av Git (.gitignore).
  - macOS / Linux: export OPENAI_API_KEY="din_nyckel"
  - PowerShell: $env:OPENAI_API_KEY = "din_nyckel"

### Status / Roadmap
Nuvarande status
- Grundläggande Python- och PowerShell-exempel: KLART (basversioner)
- Flera fristående notebooks: KLART

### Planerat / På gång
- Konsolidera alla .ipynb till en huvudnotebook: PLANERAT
- Fler AI-exempel med transformers och prompts: PLANERAT
- Enkel CI för att köra skript / tests: PLANERAT
- Publicera interaktiv version (Binder / Voila): ÖNSKAS

Bidra
- Öppna en issue för buggar eller förslag
- Skicka en pull request mot standardbranchen
- Kör flertest lokalt och skriv kortfattad beskrivning av ändringar
- Lägg inte upp hemliga nycklar i repo

### Licens
Detta projekt föreslås släppas under MIT-licensen. Se LICENSE-filen för detaljer.

### Kontakt / om skaparen
Skapat av: Stefan Blecko (https://github.com/steble70)