import click
from pyinputrecorder._main import setup_listeners, repeat_macro


@click.command()
@click.option("-r", "--record", is_flag=True, default=False)
@click.option("-u", "--run", is_flag=True, default=False)
def cli(record, run):
    assert record is not True or run is not True
    if record:
        setup_listeners()
    elif run:
        repeat_macro()
    else:
        print("Need to use --record/-r or --run/-u")
