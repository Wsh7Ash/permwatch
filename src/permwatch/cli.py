#!/usr/bin/env python3
import click
from rich.console import Console
from .audit import audit_tree
console = Console()
@click.group()
@click.version_option()
def main(): pass
@main.command()
@click.argument('path')
def scan(path):
    results = audit_tree(path)
    flagged = [r for r in results if r['issues']]
    for r in flagged:
        console.print(f"[yellow]{r['path']}[/yellow] {r['mode']}: {', '.join(r['issues'])}")
    console.print(f"[green]{len(flagged)}/{len(results)} files flagged[/green]")
if __name__ == '__main__': main()
