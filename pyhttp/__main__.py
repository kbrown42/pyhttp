import click

from pyhttp import BaseServer


@click.group()
def pyhttp():
    pass


@pyhttp.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=8888)
def serve(host, port):
    """Start serving from BaseServer"""
    server = BaseServer(host=host, port=port)
    server.serve_forever()

@pyhttp.command()
def cmd2():
    """Command on pyhttp"""
    click.echo('pyhttp cmd2')


if __name__ == '__main__':
    pyhttp()
