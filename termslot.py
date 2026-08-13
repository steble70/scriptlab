"""
Slot Machine — Textual TUI (CLI GUI)
© Stefan Blecko 2026
A text-based ("CLI") slot machine simulator, wrapped in a proper terminal
GUI built with the Textual framework (https://textual.textualize.io).
The original game logic lives in SlotMachine, refactored so a single spin
can be triggered interactively (spin()) while still supporting unattended,
multi-attempt simulation (play()) for headless/batch use.
Run it with:
    pip install textual
    python slot_machine_tui.py
Keys:  s = spin   r = ny insättning (reset)   q = avsluta (quit)
"""
 
from __future__ import annotations
 
import random
from dataclasses import dataclass
from typing import Iterator
 
from textual import work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ProgressBar,
    RichLog,
    Static,
)
 
 
# --------------------------------------------------------------------------
# Model — pure game logic, no UI concerns
# --------------------------------------------------------------------------
 
JACKPOT_THRESHOLD = 1000
 
 
@dataclass
class SpinResult:
    """The outcome of a single spin, used by the UI to render itself."""
 
    status: str          # "insufficient" | "jackpot" | "game_over" | "ok"
    win_amount: int = 0
    deposit: int = 0
    message: str = ""
 
 
class SlotMachine:
    """A text-based slot machine simulator."""
 
    def __init__(self, deposit: int = 100, bet: int = 5, attempts: int = 1):
        self.deposit = deposit
        self.bet = bet
        self.attempts = attempts
        self.game_over = False
 
    @property
    def balance(self) -> str:
        """Returns the current balance as a formatted string."""
        # max(0, deposit) ensures we never display a negative balance
        return f"{max(0, self.deposit)}:-"
 
    def _spin_wheel(self) -> int:
        """Generates a random win amount based on predefined probabilities."""
        small_wins = [
            random.randint(self.bet, 10),
            random.randint(self.bet, 10),
            random.randint(self.bet, 20),
            random.randint(self.bet, 30),
            random.randint(self.bet, 40),
            random.randint(self.bet, 50),
        ]
        big_wins = [random.randint(0, 150), random.randint(0, 250)]
        no_wins = [0] * 50
 
        all_possible_outcomes = small_wins + no_wins + big_wins
        return random.choice(all_possible_outcomes)
 
    def spin(self) -> SpinResult:
        """Plays exactly one round and returns a structured result.
        This is the method the interactive UI calls each time the player
        presses "Spin" — one user action, one spin, one result.
        """
        if self.game_over:
            return SpinResult(status="game_over", deposit=self.deposit,
                               message="Game Over. Mata in mera pengar i maskinen")
 
        if self.deposit < self.bet:
            self.game_over = True
            return SpinResult(status="insufficient", deposit=self.deposit,
                               message="Inte tillräckligt med krediter")
 
        self.deposit -= self.bet
        win_amount = self._spin_wheel()
        self.deposit += win_amount
 
        if self.deposit >= JACKPOT_THRESHOLD:
            result = SpinResult(
                status="jackpot", win_amount=win_amount, deposit=self.deposit,
                message=f"MAXVINST! Du vann {win_amount}:-, sammanlagt {self.deposit}:-",
            )
            self.deposit = 0
            self.game_over = True
            return result
 
        if self.deposit == 0:
            self.game_over = True
            return SpinResult(
                status="game_over", win_amount=win_amount, deposit=self.deposit,
                message=f"Vinst: {win_amount}:-  →  Game Over. Mata in mera pengar i maskinen",
            )
 
        return SpinResult(
            status="ok", win_amount=win_amount, deposit=self.deposit,
            message=f"Vinst: {win_amount}:-",
        )
 
    def play(self) -> Iterator[str]:
        """Original generator-based API, preserved for headless/batch play."""
        for _ in range(self.attempts):
            result = self.spin()
            yield f"\n{result.message}"
            if result.status in ("insufficient", "jackpot", "game_over"):
                break
 
 
# --------------------------------------------------------------------------
# Widgets
# --------------------------------------------------------------------------
 
# win_amount tiers -> reel symbols shown on the three "wheels"
_TIERS = (
    (0, ("🍋", "🍇", "🔔")),     # no win: mismatched fruit
    (10, ("🍒", "🍒", "🍒")),
    (50, ("🔔", "🔔", "🔔")),
    (150, ("⭐", "⭐", "⭐")),
    (10**9, ("💎", "💎", "💎")),
)
_SPIN_FRAME_SYMBOLS = ["🍒", "🍋", "🍇", "🔔", "⭐", "💎", "7️⃣"]
 
 
def _symbols_for(win_amount: int) -> tuple[str, str, str]:
    for ceiling, symbols in _TIERS:
        if win_amount <= ceiling:
            return symbols
    return _TIERS[-1][1]
 
 
class ReelDisplay(Static):
    """The three slot-machine reels."""
 
    DEFAULT_CSS = """
    ReelDisplay {
        content-align: center middle;
        height: 5;
        border: heavy $warning;
        background: $panel;
        text-style: bold;
    }
    """
 
    def on_mount(self) -> None:
        self.settle(("🍒", "🍋", "🔔"))
 
    def randomize_frame(self) -> None:
        """A single animation frame: self-message to randomize symbols."""
        symbols = [random.choice(_SPIN_FRAME_SYMBOLS) for _ in range(3)]
        self.update(self._format_symbols(symbols))
 
    def settle(self, symbols: tuple[str, str, str]) -> None:
        self.update(self._format_symbols(symbols))
 
    @staticmethod
    def _format_symbols(symbols) -> str:
        return "   ".join(f"[ {s} ]" for s in symbols)
 
 
class StatusPanel(Static):
    """Deposit / bet readout plus a progress bar toward the jackpot."""
 
    DEFAULT_CSS = """
    StatusPanel {
        height: auto;
        padding: 1 2;
        border: round $primary;
    }
    StatusPanel Label {
        width: 1fr;
    }
    """
 
    deposit_text: reactive[str] = reactive("100:-")
    bet_text: reactive[str] = reactive("5:-")
 
    def compose(self) -> ComposeResult:
        yield Label(id="deposit_label")
        yield Label(id="bet_label")
        yield ProgressBar(total=JACKPOT_THRESHOLD, id="jackpot_bar", show_eta=False)
 
    def watch_deposit_text(self, value: str) -> None:
        self.query_one("#deposit_label", Label).update(f"💰 Insättning: {value}")
 
    def watch_bet_text(self, value: str) -> None:
        self.query_one("#bet_label", Label).update(f"🎯 Insats per snurr: {value}")
 
    def update_progress(self, deposit: int) -> None:
        self.query_one("#jackpot_bar", ProgressBar).update(
            progress=min(max(deposit, 0), JACKPOT_THRESHOLD)
        )
 
 
# --------------------------------------------------------------------------
# App
# --------------------------------------------------------------------------
 
class SlotMachineApp(App):
    """Textual CLI-GUI wrapper around SlotMachine."""
 
    TITLE = "🎰 SLOT MACHINE"
    SUB_TITLE = "Textual CLI-GUI"
 
    CSS = """
    Screen {
        background: $surface;
        align: center middle;
    }
    #board {
        width: 60;
        height: auto;
        padding: 1 2;
        border: thick $accent;
    }
    #controls {
        height: auto;
        margin-top: 1;
    }
    #controls Input {
        width: 1fr;
        margin-right: 1;
    }
    #buttons {
        height: auto;
        margin-top: 1;
    }
    #buttons Button {
        width: 1fr;
        margin-right: 1;
    }
    RichLog {
        height: 10;
        margin-top: 1;
        border: round $secondary;
    }
    """
 
    BINDINGS = [
        Binding("s", "spin", "Snurra"),
        Binding("r", "reset", "Ny insättning"),
        Binding("q", "quit", "Avsluta"),
    ]
 
    spinning: reactive[bool] = reactive(False)
 
    def __init__(self) -> None:
        super().__init__()
        self.machine = SlotMachine(deposit=100, bet=5)
 
    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="board"):
            yield StatusPanel(id="status")
            yield ReelDisplay(id="reels")
            with Horizontal(id="controls"):
                yield Input(value="100", placeholder="Insättning", id="deposit_input")
                yield Input(value="5", placeholder="Insats", id="bet_input")
            with Horizontal(id="buttons"):
                yield Button("🎰 SNURRA (s)", id="spin_btn", variant="success")
                yield Button("↺ Ny insättning (r)", id="reset_btn", variant="warning")
            yield RichLog(id="log", markup=True)
        yield Footer()
 
    def on_mount(self) -> None:
        self._sync_status()
        self.query_one("#log", RichLog).write("[bold]Välkommen! Tryck SNURRA för att spela.[/bold]")
 
    def _sync_status(self) -> None:
        panel = self.query_one("#status", StatusPanel)
        panel.deposit_text = self.machine.balance
        panel.bet_text = f"{self.machine.bet}:-"
        panel.update_progress(self.machine.deposit)
 
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "spin_btn":
            self.action_spin()
        elif event.button.id == "reset_btn":
            self.action_reset()
 
    def action_spin(self) -> None:
        if not self.spinning:
            self.do_spin()
 
    def action_reset(self) -> None:
        deposit = self._read_int("#deposit_input", default=100)
        bet = self._read_int("#bet_input", default=5)
        self.machine = SlotMachine(deposit=deposit, bet=bet)
        self._sync_status()
        self.query_one("#spin_btn", Button).disabled = False
        self.query_one("#reels", ReelDisplay).settle(("🍒", "🍋", "🔔"))
        self.query_one("#log", RichLog).write(
            f"[bold cyan]Ny insättning: {deposit}:- · insats {bet}:-[/bold cyan]"
        )
 
    def _read_int(self, selector: str, default: int) -> int:
        try:
            return max(1, int(self.query_one(selector, Input).value))
        except (ValueError, TypeError):
            return default
 
    @work(exclusive=True)
    async def do_spin(self) -> None:
        import asyncio
 
        self.spinning = True
        spin_btn = self.query_one("#spin_btn", Button)
        reset_btn = self.query_one("#reset_btn", Button)
        reels = self.query_one("#reels", ReelDisplay)
        log = self.query_one("#log", RichLog)
        spin_btn.disabled = True
        reset_btn.disabled = True
 
        # Animation frames — reels self-message to randomize their symbols
        for _ in range(10):
            reels.randomize_frame()
            await asyncio.sleep(0.06)
 
        result = self.machine.spin()
        reels.settle(_symbols_for(result.win_amount))
        self._sync_status()
 
        color = {"ok": "white", "jackpot": "bold gold3",
                 "game_over": "bold red", "insufficient": "bold red"}[result.status]
        log.write(f"[{color}]{result.message}[/{color}]")
 
        reset_btn.disabled = False
        if result.status in ("jackpot", "game_over", "insufficient"):
            spin_btn.disabled = True
        else:
            spin_btn.disabled = False
 
        self.spinning = False
 
 
if __name__ == "__main__":
    SlotMachineApp().run()
