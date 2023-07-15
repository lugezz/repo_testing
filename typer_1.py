from datetime import date, datetime
import typer

app = typer.Typer()

@app.command()
def hello(name:str):
    typer.echo(f'Hello {name}!')


@app.command()
def day_of_week(date_param:datetime):
    typer.echo(f'The day of the week is {date_param.strftime("%A")}!')


if __name__ == '__main__':
    app()