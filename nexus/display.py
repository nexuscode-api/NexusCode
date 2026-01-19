from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.markdown import Markdown

class Interface:
    """
    Handles all Terminal User Interface (TUI) rendering using 'rich'.
    """
    def __init__(self):
        self.console = Console()

    def show_splash(self, version: str):
        self.console.clear()
        self.console.print(Panel.fit(
            f"[bold white]⚡ NEXUS CODE AI[/bold white]\n[dim]v{version} | The Unshackled Agent[/dim]",
            border_style="cyan",
            padding=(1, 4)
        ))

    def show_dashboard(self, pool_data: list):
        """Renders the KeyPool status table."""
        table = Table(title="📡 NEXUS KEYPOOL™ STATUS", border_style="blue", expand=True)
        table.add_column("Provider", style="cyan", ratio=1)
        table.add_column("Model", style="magenta", ratio=1)
        table.add_column("Latency", style="green", ratio=1)
        table.add_column("Status", justify="right", ratio=1)

        for node in pool_data:
            status_style = "green" if node['status'] == "ACTIVE" else "red"
            table.add_row(
                node['provider'], 
                node['model'], 
                f"{node['latency_ms']}ms", 
                f"[{status_style}]{node['status']}[/{status_style}]"
            )
        self.console.print(table)
        self.console.print("\n")

    def get_input(self) -> str:
        return self.console.input("[bold green]User > [/bold green]")

    def print_stream(self, text, is_system=False, is_error=False):
        """Prints text to console. Handles partial updates for streaming effect."""
        if is_error:
            self.console.print(f"\n[bold red]{text}[/bold red]")
        elif is_system:
            self.console.print(f"\n[dim italic]{text}[/dim italic]\n")
        else:
            # Direct write to buffer for 'typing' effect
            self.console.print(text, end="")
