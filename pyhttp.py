import click

@click.group()
def pyhttp():
    pass

@pyhttp.command()
def cmd1():
    '''Command on pyhttp'''
    click.echo('pyhttp cmd1')

@pyhttp.command()
def cmd2():
    '''Command on pyhttp'''
    click.echo('pyhttp cmd2')

if __name__ == '__main__':
    pyhttp()
