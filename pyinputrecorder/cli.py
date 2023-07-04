import click
from pyinputrecorder._main import setup_listeners, repeat_macro


@click.group()
def cli():
    pass


@cli.command()
@click.option("-mr", "--mouse-relative", is_flag=True, default=False)
def r(mouse_relative):
    """Record kb/m. Press escape to stop."""
    mode = "r" if mouse_relative else "a"
    setup_listeners(mode)


@cli.command()
@click.option("-s", "--speed", type=int, default=100, help="How fast should the times be as a precentage. (100 is as recorded)")
def u(speed):
    """Replay recorded kb/m stream."""
    repeat_macro(speed)
