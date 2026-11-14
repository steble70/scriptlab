"""A simple slot-machine game for JupyterLab and Jupyter Notebook.

Install the widget dependency if needed::

    %pip install ipywidgets

Then run in a notebook cell::

    from termslot import show_slot_machine
    game = show_slot_machine()

The game logic can also be used without the notebook interface via
``SlotMachine`` and its ``spin()`` / ``play()`` methods.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterator

import ipywidgets as widgets
from IPython.display import HTML, display

JACKPOT_THRESHOLD = 1000


@dataclass
class SpinResult:
    """The outcome of one spin."""

    status: str  # "insufficient", "jackpot", "game_over", or "ok"
    win_amount: int = 0
    deposit: int = 0
    message: str = ""


class SlotMachine:
    """Game logic, independent of the notebook interface."""

    def __init__(self, deposit: int = 100, bet: int = 5, attempts: int = 1):
        if deposit < 0:
            raise ValueError("Deposit cannot be negative.")
        if bet <= 0:
            raise ValueError("Bet must be greater than zero.")
        if attempts < 0:
            raise ValueError("Attempts cannot be negative.")

        self.deposit = deposit
        self.bet = bet
        self.attempts = attempts
        self.game_over = False

    @property
    def balance(self) -> str:
        """Return the current balance in the game's display format."""
        return f"{self.deposit}:-"

    def _spin_wheel(self) -> int:
        """Choose a payout using the original game's outcome weights."""
        def small_win(maximum: int) -> int:
            # Keep the payout range valid even when the bet exceeds its cap.
            return random.randint(min(self.bet, maximum), maximum)

        outcomes = [
            small_win(10),
            small_win(10),
            small_win(20),
            small_win(30),
            small_win(40),
            small_win(50),
            *([0] * 50),
            random.randint(0, 150),
            random.randint(0, 250),
        ]
        return random.choice(outcomes)

    def spin(self) -> SpinResult:
        """Play one round and return its result."""
        if self.game_over:
            return SpinResult(
                status="game_over",
                deposit=self.deposit,
                message="Game over. Reset the game to play again.",
            )

        if self.deposit < self.bet:
            self.game_over = True
            return SpinResult(
                status="insufficient",
                deposit=self.deposit,
                message="Not enough credits to place another bet.",
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
                    f"JACKPOT! You won {win_amount}:-. "
                    f"Final balance: {self.deposit}:-."
                ),
            )

        # End the game as soon as the remaining balance cannot cover another bet.
        if self.deposit < self.bet:
            self.game_over = True
            return SpinResult(
                status="game_over",
                win_amount=win_amount,
                deposit=self.deposit,
                message=(
                    f"Payout: {win_amount}:-. Not enough credits for another bet."
                ),
            )

        return SpinResult(
            status="ok",
            win_amount=win_amount,
            deposit=self.deposit,
            message=f"Payout: {win_amount}:-.",
        )

    def play(self) -> Iterator[str]:
        """Yield messages for up to ``attempts`` spins (batch use)."""
        for _ in range(self.attempts):
            result = self.spin()
            yield result.message
            if result.status != "ok":
                break


# Payout ranges map to the symbols displayed on the reels.
_TIERS = (
    (0, ("🍋", "🍇", "🔔")),
    (10, ("🍒", "🍒", "🍒")),
    (50, ("🔔", "🔔", "🔔")),
    (150, ("⭐", "⭐", "⭐")),
    (float("inf"), ("💎", "💎", "💎")),
)


def _symbols_for(win_amount: int) -> tuple[str, str, str]:
    """Return a reel-symbol combination appropriate for a payout."""
    for ceiling, symbols in _TIERS:
        if win_amount <= ceiling:
            return symbols
    return _TIERS[-1][1]


class NotebookSlotMachine:
    """ipywidgets interface for playing the game in a notebook."""

    def __init__(self, deposit: int = 100, bet: int = 5):
        self.machine = SlotMachine(deposit=deposit, bet=bet)

        self.deposit_input = widgets.IntText(
            value=deposit,
            description="Deposit:",
            style={"description_width": "initial"},
        )
        self.bet_input = widgets.IntText(
            value=bet,
            description="Bet:",
            style={"description_width": "initial"},
        )
        self.spin_button = widgets.Button(
            description="Spin", button_style="success", icon="play"
        )
        self.reset_button = widgets.Button(
            description="New game", button_style="warning", icon="refresh"
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
                widgets.HTML("<h2>🎰 Slot Machine</h2>"),
                widgets.HBox([self.deposit_input, self.bet_input]),
                widgets.HBox([self.spin_button, self.reset_button]),
                self.reels,
                self.status,
                self.progress,
                widgets.HTML("<b>Game history</b>"),
                self.history,
            ]
        )
        self._refresh()

    def _refresh(self, message: str = "Ready to play.") -> None:
        symbols = _symbols_for(0) if self.machine.game_over else ("🍒", "🍋", "🔔")
        self.reels.value = (
            '<div style="font-size:2em;text-align:center">'
            + "　".join(symbols)
            + "</div>"
        )
        self.status.value = (
            f"<b>Balance:</b> {self.machine.balance} &nbsp; "
            f"<b>Bet:</b> {self.machine.bet}:-<br>{message}"
        )
        self.progress.value = min(max(self.machine.deposit, 0), JACKPOT_THRESHOLD)
        self.spin_button.disabled = self.machine.game_over

    def _on_spin(self, _button: widgets.Button) -> None:
        result = self.machine.spin()
        symbols = _symbols_for(result.win_amount)
        self.reels.value = (
            '<div style="font-size:2em;text-align:center">'
            + "　".join(symbols)
            + "</div>"
        )
        self._refresh(result.message)
        with self.history:
            print(result.message)

    def _on_reset(self, _button: widgets.Button) -> None:
        deposit = int(self.deposit_input.value)
        bet = int(self.bet_input.value)
        if deposit < 0 or bet <= 0:
            self.status.value = (
                "<span style='color:#b00020'>"
                "Deposit must be zero or more, and bet must be greater than zero."
                "</span>"
            )
            return

        self.machine = SlotMachine(deposit=deposit, bet=bet)
        self.history.clear_output()
        self._refresh("New game started.")


def show_slot_machine(deposit: int = 100, bet: int = 5) -> NotebookSlotMachine:
    """Display the game in JupyterLab/Notebook and return its controller."""
    game = NotebookSlotMachine(deposit=deposit, bet=bet)
    display(game.widget)
    return game


if __name__ == "__main__":
    print("This module is designed for JupyterLab/Notebook.")
    print("In a notebook cell, run: from termslot import show_slot_machine; show_slot_machine()")
