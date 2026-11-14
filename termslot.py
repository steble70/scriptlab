"""
Slot Machine — Textual TUI (CLI GUI)
© Stefan Blecko 2026
A text-based ("CLI") slot machine simulator, wrapped in a proper terminal
GUI built with the Textual framework (https://textual.textualize.io).
The original game logic lives in SlotMachine, refactored so a single spin
can be triggered interactively (spin()) while still supporting unattended,
multi-attempt simulation (play()) for headless/batch use.

Terminal usage:
    pip install textual
    python termslot.py

JupyterLab usage: open termslot_jupyter.ipynb in JupyterLab. It uses
ipywidgets and works independently of the Textual terminal event loop.

Keys:  s = spin   r = ny insättning (reset)   q = avsluta (quit)
"""