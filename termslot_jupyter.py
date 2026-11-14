"""JupyterLab-friendly widget interface for the slot machine.

Place this file beside ``termslot.py`` (or install the repository package),
then in a Jupyter notebook run::

    %pip install ipywidgets
    from IPython.display import display
    from termslot_jupyter import create_jupyter_ui
    display(create_jupyter_ui())

The original Textual terminal application remains available in ``termslot.py``.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

import ipywidgets as widgets
from IPython.display import display

JACKPOT_THRESHOLD = 1000


@dataclass
class SpinResult:
    """The outcome of one spin."""

    status: str
    win_amount: int = 0
    deposit: int = 0
    message: str = ""


class SlotMachine:
    """Game model, independent of the Textual terminal UI."""

    def __init__(self, deposit: int = 100, bet: int = 5, attempts: int = 1):
        if deposit < 1:
            raise ValueError("deposit must be at least 1")
        if bet < 1:
            raise ValueError("bet must be at least 1")
        self.deposit = deposit
        self.bet = bet
        self.attempts = attempts
        self.game_over = False

    @property
    def balance(self) -> str:
        return f"{max(0, self.deposit)}:-"

    def _spin_wheel(self) -> int:
        small_wins = [
            random.randint(self.bet, 10),
            random.randint(self.bet, 10),
            random.randint(self.bet, 20),
            random.randint(self.bet, 30),
            random.randint(self.bet, 40),
            random.randint(self.bet, 50),
        ]
        outcomes = small_wins + [0] * 50 + [
            random.randint(0, 150),
            random.randint(0, 250),
        ]
        return random.choice(outcomes)

    def spin(self) -> SpinResult:
        if self.game_over:
            return SpinResult(
                "game_over", deposit=self.deposit,
                message="Game Over. Mata in mera pengar i maskinen",
            )
        if self.deposit < self.bet:
            self.game_over = True
            return SpinResult(
                "insufficient", deposit=self.deposit,
                message="Inte tillräckligt med krediter",
            )

        self.deposit -= self.bet
        win_amount = self._spin_wheel()
        self.deposit += win_amount

        if self.deposit >= JACKPOT_THRESHOLD:
            result = SpinResult(
                "jackpot", win_amount, self.deposit,
                f"MAXVINST! Du vann {win_amount}:-, sammanlagt {self.deposit}:-",
            )
            self.deposit = 0
            self.game_over = True
            return result
        if self.deposit == 0:
            self.game_over = True
            return SpinResult(
                "game_over", win_amount, self.deposit,
                f"Vinst: {win_amount}:- → Game Over. Mata in mera pengar i maskinen",
            )
        return SpinResult("ok", win_amount, self.deposit, f"Vinst: {win_amount}:-")


class JupyterSlotMachine:
    """ipywidgets controls for playing directly inside a notebook output cell."""

    def __init__(self, deposit: int = 100, bet: int = 5):
        self.machine = SlotMachine(deposit=deposit, bet=bet)
        self.deposit_input = widgets.BoundedIntText(
            value=deposit, min=1, max=10**9, description="Insättning:",
            style={"description_width": "initial"},
        )
        self.bet_input = widgets.BoundedIntText(
            value=bet, min=1, max=10**9, description="Insats:",
            style={"description_width": "initial"},
        )
        self.spin_button = widgets.Button(
            description="🎰 SNURRA", button_style="success", tooltip="Spela en omgång"
        )
        self.reset_button = widgets.Button(
            description="↺ Ny insättning", button_style="warning"
        )
        self.balance_label = widgets.HTML()
        self.reels_label = widgets.HTML(value="<h2 style='text-align:center'>🍒　🍋　🔔</h2>")
        self.progress = widgets.FloatProgress(
            value=deposit, min=0, max=JACKPOT_THRESHOLD,
            description="Jackpot:", bar_style="info",
            style={"description_width": "initial"},
        )
        self.message = widgets.HTML(value="<b>Välkommen! Tryck SNURRA för att spela.</b>")
        self.log = widgets.Output(layout={"border": "1px solid #888", "padding": "6px"})

        self.spin_button.on_click(self._spin)
        self.reset_button.on_click(self._reset)
        self.widget = widgets.VBox([
            widgets.HTML("<h2>🎰 SLOT MACHINE</h2>"),
            self.balance_label,
            self.progress,
            self.reels_label,
            widgets.HBox([self.deposit_input, self.bet_input]),
            widgets.HBox([self.spin_button, self.reset_button]),
            self.message,
            self.log,
        ], layout={"width": "min(100%, 700px)"})
        self._sync_status()

    def _sync_status(self) -> None:
        self.balance_label.value = (
            f"<b>💰 Saldo:</b> {self.machine.balance}"
            f"　 <b>🎯 Insats per snurr:</b> {self.machine.bet}:-"
        )
        self.progress.value = min(max(self.machine.deposit, 0), JACKPOT_THRESHOLD)

    def _spin(self, _button) -> None:
        result = self.machine.spin()
        symbol = "🍋　🍇　🔔" if result.win_amount == 0 else (
            "🍒　🍒　🍒" if result.win_amount <= 10 else
            "🔔　🔔　🔔" if result.win_amount <= 50 else
            "⭐　⭐　⭐" if result.win_amount <= 150 else "💎　💎　💎"
        )
        self.reels_label.value = f"<h2 style='text-align:center'>{symbol}</h2>"
        color = "#b8860b" if result.status == "jackpot" else (
            "#b00020" if result.status in ("game_over", "insufficient") else "inherit"
        )
        self.message.value = f"<span style='color:{color}'>{result.message}</span>"
        self._sync_status()
        self.spin_button.disabled = result.status != "ok"
        with self.log:
            print(result.message)

    def _reset(self, _button) -> None:
        deposit = self.deposit_input.value
        bet = self.bet_input.value
        self.machine = SlotMachine(deposit=deposit, bet=bet)
        self.spin_button.disabled = False
        self.reels_label.value = "<h2 style='text-align:center'>🍒　🍋　🔔</h2>"
        self.message.value = f"Ny insättning: {deposit}:- · insats {bet}:-"
        self._sync_status()

    def display(self):
        """Display the widget in a notebook cell and return it for reuse."""
        display(self.widget)
        return self.widget


def create_jupyter_ui(deposit: int = 100, bet: int = 5) -> JupyterSlotMachine:
    """Create the interactive notebook game; call ``.display()`` to show it."""
    return JupyterSlotMachine(deposit=deposit, bet=bet)
