import click

from pyhttp import BaseServer, ThreadedServer


@click.group()
def pyhttp():
    pass


@pyhttp.command()
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default=8888)
@click.option('--threaded', is_flag=True)
def serve(host, port, threaded):
    """Start serving from BaseServer"""
    if not threaded:
        server = BaseServer(host=host, port=port)
    else:
        server = ThreadedServer(host=host, port=port)

    server.serve_forever()


@pyhttp.command()
def cmd2():
    """Command on pyhttp"""
    click.echo('pyhttp cmd2')


if __name__ == '__main__':
    pyhttp()
