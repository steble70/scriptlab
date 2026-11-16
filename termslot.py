"""En enkel spelautomat för JupyterLab och Jupyter Notebook.

Installera widget-beroendet vid behov::

    %pip install ipywidgets

Kör sedan i en notebook-cell::

    from termslot_sv import show_slot_machine
    game = show_slot_machine()

Spellogiken kan också användas utan notebook-gränssnittet via
``SlotMachine`` och dess metoder ``spin()`` / ``play()``.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterator

import ipywidgets as widgets
from IPython.display import display

JACKPOT_THRESHOLD = 1000

# --- Utbetalningstabell ------------------------------------------------------
# Utbetalningarna är multiplar av insatsen, så återbetalningsandelen (RTP) är
# densamma för alla insatsstorlekar. Varje snurr drar ett utfall likformigt ur
# denna pool:
#   * små vinster:   randint(1 x insats, m x insats) för varje m i SMALL_WIN_MULTIPLES
#   * ingen vinst:   ZERO_OUTCOMES poster som betalar 0
#   * breda vinster: randint(0, m x insats) för varje m i WIDE_WIN_MULTIPLES
# Med dessa värden blir RTP 58,5 / 61 = 95,9 %.
SMALL_WIN_MULTIPLES = (2, 2, 4, 6, 8, 9)
ZERO_OUTCOMES = 53
WIDE_WIN_MULTIPLES = (30, 50)


def theoretical_rtp() -> float:
    """Exakt återbetalningsandel (RTP) som bråkdel (0,959 betyder 95,9 %).

    Medelvärdet av randint(a, b) är (a + b) / 2, så den förväntade
    utbetalningen per snurr, uttryckt i insatser, är en summa av enkla
    medelvärden delad med poolens storlek.
    """
    expected = sum((1 + m) / 2 for m in SMALL_WIN_MULTIPLES)
    expected += sum(m / 2 for m in WIDE_WIN_MULTIPLES)
    pool = len(SMALL_WIN_MULTIPLES) + ZERO_OUTCOMES + len(WIDE_WIN_MULTIPLES)
    return expected / pool



@dataclass
class SpinResult:
    """Utfallet av en snurr."""

    status: str  # "insufficient", "jackpot", "game_over" eller "ok"
    win_amount: int = 0
    deposit: int = 0
    message: str = ""


class SlotMachine:
    """Spellogik, oberoende av notebook-gränssnittet."""

    def __init__(self, deposit: int = 100, bet: int = 5, attempts: int = 1):
        if deposit < 0:
            raise ValueError("Insättningen kan inte vara negativ.")
        if bet <= 0:
            raise ValueError("Insatsen måste vara större än noll.")
        if attempts < 0:
            raise ValueError("Antalet försök kan inte vara negativt.")

        self.deposit = deposit
        self.bet = bet
        self.attempts = attempts
        self.game_over = False

    @property
    def balance(self) -> str:
        """Returnera aktuellt saldo i spelets visningsformat."""
        return f"{self.deposit}:-"

    def _spin_wheel(self) -> int:
        """Välj en utbetalning ur poolen som beskrivs i utbetalningstabellen."""
        bet = self.bet
        n_small = len(SMALL_WIN_MULTIPLES)
        pick = random.randrange(n_small + ZERO_OUTCOMES + len(WIDE_WIN_MULTIPLES))

        if pick < n_small:
            return random.randint(bet, SMALL_WIN_MULTIPLES[pick] * bet)
        pick -= n_small
        if pick < ZERO_OUTCOMES:
            return 0
        return random.randint(0, WIDE_WIN_MULTIPLES[pick - ZERO_OUTCOMES] * bet)

    def spin(self) -> SpinResult:
        """Spela en runda och returnera resultatet."""
        if self.game_over:
            return SpinResult(
                status="game_over",
                deposit=self.deposit,
                message="Spelet är slut. Starta ett nytt spel för att spela igen.",
            )

        if self.deposit < self.bet:
            self.game_over = True
            return SpinResult(
                status="insufficient",
                deposit=self.deposit,
                message="Inte tillräckligt med krediter för ännu en insats.",
            )

        self.deposit -= self.bet
        win_amount = self._spin_wheel()
        self.deposit += win_amount

        if self.deposit >= JACKPOT_THRESHOLD:
            self.game_over = True
            return SpinResult(
                status="jackpot",
                win_amount=win_amount,
                deposit=self.deposit,
                message=(
                    f"JACKPOT! Utbetalning: {win_amount}:-. "
                    f"Slutsaldo: {self.deposit}:-."
                ),
            )

        # Avsluta spelet om det återstående saldot inte räcker till en ny insats.
        if self.deposit < self.bet:
            self.game_over = True
            return SpinResult(
                status="game_over",
                win_amount=win_amount,
                deposit=self.deposit,
                message=(
                    f"Utbetalning: {win_amount}:-. "
                    "Inte tillräckligt med krediter för ännu en insats."
                ),
            )

        return SpinResult(
            status="ok",
            win_amount=win_amount,
            deposit=self.deposit,
            message=f"Utbetalning: {win_amount}:-.",
        )

    def play(self) -> Iterator[str]:
        """Ge meddelanden för upp till ``attempts`` snurr (batchanvändning)."""
        for _ in range(self.attempts):
            result = self.spin()
            yield result.message
            if result.status != "ok":
                break


# Utbetalningen, som multipel av insatsen, avgör vilka symboler hjulen visar.
_TIERS = (
    (0, ("🍋", "🍇", "🔔")),
    (2, ("🍒", "🍒", "🍒")),
    (10, ("🔔", "🔔", "🔔")),
    (30, ("⭐", "⭐", "⭐")),
    (float("inf"), ("💎", "💎", "💎")),
)


def _symbols_for(win_amount: int, bet: int = 5) -> tuple[str, str, str]:
    """Returnera en symbolkombination som passar en utbetalning.

    ``bet`` är den insats utbetalningen hör till (standard: spelets
    standardinsats), eftersom symbolnivåerna är multiplar av insatsen.
    """
    multiple = win_amount / bet
    for ceiling, symbols in _TIERS:
        if multiple <= ceiling:
            return symbols
    return _TIERS[-1][1]


class NotebookSlotMachine:
    """ipywidgets-gränssnitt för att spela spelet i en notebook."""

    def __init__(self, deposit: int = 100, bet: int = 5):
        self.machine = SlotMachine(deposit=deposit, bet=bet)

        self.deposit_input = widgets.IntText(
            value=deposit,
            description="Insättning:",
            style={"description_width": "initial"},
        )
        self.bet_input = widgets.IntText(
            value=bet,
            description="Insats:",
            style={"description_width": "initial"},
        )
        self.spin_button = widgets.Button(
            description="Snurra", button_style="success", icon="play"
        )
        self.reset_button = widgets.Button(
            description="Nytt spel", button_style="warning", icon="refresh"
        )
        self.reels = widgets.HTML()
        self.status = widgets.HTML()
        self.history = widgets.Output(
            layout=widgets.Layout(border="1px solid #ccc", padding="8px")
        )
        self.progress = widgets.IntProgress(
            value=min(deposit, JACKPOT_THRESHOLD),
            min=0,
            max=JACKPOT_THRESHOLD,
            description="Jackpot:",
            style={"description_width": "initial"},
        )

        self.spin_button.on_click(self._on_spin)
        self.reset_button.on_click(self._on_reset)

        self.widget = widgets.VBox(
            [
                widgets.HTML("<h2>🎰 Spelautomat</h2>"),
                widgets.HBox([self.deposit_input, self.bet_input]),
                widgets.HBox([self.spin_button, self.reset_button]),
                self.reels,
                self.status,
                self.progress,
                widgets.HTML("<b>Spelhistorik</b>"),
                self.history,
            ]
        )
        self._refresh()

    def _refresh(
        self,
        message: str = "Redo att spela.",
        symbols: tuple[str, str, str] = ("🍒", "🍋", "🔔"),
    ) -> None:
        self.reels.value = (
            '<div style="font-size:2em;text-align:center">'
            + "　".join(symbols)
            + "</div>"
        )
        self.status.value = (
            f"<b>Saldo:</b> {self.machine.balance} &nbsp; "
            f"<b>Insats:</b> {self.machine.bet}:-<br>{message}"
        )
        self.progress.value = min(max(self.machine.deposit, 0), JACKPOT_THRESHOLD)
        self.spin_button.disabled = self.machine.game_over

    def _on_spin(self, _button: widgets.Button) -> None:
        result = self.machine.spin()
        self._refresh(result.message, _symbols_for(result.win_amount, self.machine.bet))
        with self.history:
            print(result.message)

    def _on_reset(self, _button: widgets.Button) -> None:
        deposit = int(self.deposit_input.value)
        bet = int(self.bet_input.value)
        if deposit < 0 or bet <= 0:
            self.status.value = (
                "<span style='color:#b00020'>"
                "Insättningen måste vara noll eller mer, och insatsen måste vara "
                "större än noll."
                "</span>"
            )
            return

        self.machine = SlotMachine(deposit=deposit, bet=bet)
        self.history.clear_output()
        self._refresh("Nytt spel startat.")


def show_slot_machine(deposit: int = 100, bet: int = 5) -> NotebookSlotMachine:
    """Visa spelet i JupyterLab/Notebook och returnera dess styrobjekt."""
    game = NotebookSlotMachine(deposit=deposit, bet=bet)
    display(game.widget)
    return game


if __name__ == "__main__":
    print("Den här modulen är avsedd för JupyterLab/Notebook.")
    print("Kör i en notebook-cell: from termslot_sv import show_slot_machine; show_slot_machine()")
