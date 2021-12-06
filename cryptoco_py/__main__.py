import requests
import json
import typer
import datetime
from datetime import datetime

app = typer.Typer()

def bol(st:bool):
		if st:
			return 'true'
		else:
			return 'false'

@app.command()
def ping():
	""" ping the server """
	response = requests.get('https://api.coingecko.com/api/v3/ping')
	p = json.dumps(response.json(), indent=2)
	return typer.echo(p)


def validate(date_text):
	try:
		datetime.datetime.strptime(date_text, '%d-%m-%Y')
	except ValueError:
		return False
	return True


@app.command()
def sprice(
	ids: str = typer.Argument(...,help="pass the coin id (can be obtained from list coins) eg. bitcoin"),
 	vs_currency: str = typer.Argument("usd",help="the currency you want to compare with."),
	cap: bool = typer.Option(False,'--cap'),
	vol: bool = typer.Option(False,'--vol'),
	change: bool = typer.Option(False,'--change'),
	include_last_updated: bool = typer.Option(False)
):
	""" price(s) of cryptocurrency """
	response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies={vs_currency}&include_market_cap={bol(cap)}&include_24hr_vol={bol(vol)}&include_24hr_change={bol(change)}&include_last_updated_at={include_last_updated}")
	if response.json() == {}:
		typer.echo("unknown coin name")
		raise typer.Exit(code=1)
	else:
		p = json.dumps(response.json(), indent=2)
		return typer.echo(p)




@app.command()
def list(option: str = typer.Argument(...)):
	""" list all supported [ vs_currency | coins | platforms | categories ] """
	if option == "vs_currency":
		response = requests.get('https://api.coingecko.com/api/v3/simple/supported_vs_currencies')
		p = json.dumps(response.json(), indent=2)
		return typer.echo(p)
	elif option == 'coins':
		response = requests.get('https://api.coingecko.com/api/v3/coins/list')
		p = json.dumps(response.json(), indent=2)
		return typer.echo(p)
	elif option == 'platforms' :
		response = requests.get('https://api.coingecko.com/api/v3/asset_platforms')
		p = json.dumps(response.json(), indent=2)
		return typer.echo(p)
	elif option == 'categories':
		m = typer.prompt(' with market_data ? [y|n] ')
		if m.lower() == 'y':
			response = requests.get('https://api.coingecko.com/api/v3/coins/categories')
			p = json.dumps(response.json(), indent=2)
			return typer.echo(p)
		elif m.lower() == 'n':
			response = requests.get('https://api.coingecko.com/api/v3/coins/categories/list')
			p = json.dumps(response.json(), indent=2)
			return typer.echo(p)
		else:
			typer.echo(f'"{m}" is not an available option')
			return typer.Exit(code=1)
	else:
		typer.echo(f'"{option}" is not an available option')
		typer.Exit(code=1)
@app.command()
def coin(
	ids: str = typer.Argument(...,help="pass the coin id (can be obtained from list coins) eg. bitcoin"),
 	localization: bool = typer.Option(False),
	tickers: bool = typer.Option(False),
	market_data: bool = typer.Option(False),
	community_data: bool = typer.Option(False),
	developer_data: bool = typer.Option(False),
	sparkline: bool = typer.Option(False),

):
	""" view detailed information about the coin """
	response = requests.get(f"https://api.coingecko.com/api/v3/coins/{ids}?localization={bol(localization)}&tickers={bol(tickers)}&community_data={bol(community_data)}&developer_data={bol(developer_data)}&sparkline={bol(sparkline)}&market_data={market_data}")
	p = json.dumps(response.json(), indent=2)
	if response.json() == {}:
		typer.echo("unknown coin name")
		raise typer.Exit(code=1)
	else:
		return typer.echo(p)


@app.command()
def history(ids: str,date: str,localization: bool = typer.Option("False") ):

	""" Get historical data (name, price, market, stats) at a given date for a coin """

	if validate(date) == False:
		typer.echo("incorrect date format, should be DD-MM-YYYY")
		raise typer.Exit(code=1)
	response = requests.get(f'https://api.coingecko.com/api/v3/coins/{ids}/history?date={date}&localization={localization}')
	p = json.dumps(response.json(), indent=2)
	return typer.echo(p)

@app.command()
def market_chart(
	ids: str = typer.Argument(...,help="pass the coin id (can be obtained from list coins) eg. bitcoin"),
	vs_currency: str = typer.Argument("usd",help="the currency you want to compare with."),
	f: int = typer.Argument("0"),
	t: int = typer.Argument("0")
	):

	""" Get historical market data include price, market cap, and 24h volume within a range of timestamp """

	From_date = datetime.fromtimestamp(f)
	To_date = datetime.fromtimestamp(t)
	typer.echo(f"From date = {From_date}")
	typer.echo(f"To date = {To_date}")
	response = requests.get(f"https://api.coingecko.com/api/v3/coins/{ids}/market_chart/range?vs_currency={vs_currency}&from={f}&to={t}")
	p = json.dumps(response.json(), indent=2)
	return typer.echo(p)


@app.command()
def ohlc(
	ids: str = typer.Argument(...,help="pass the coin id (can be obtained from list coins) eg. bitcoin"),
	vs_currency: str = typer.Argument("usd",help="the currency you want to compare with."),
	days: int = typer.Argument(1,help="Data up to number of days ago (1/7/14/30/90/180/365[max])")
):
	""" get coin's ohlc """
	if days > 365:
		typer.echo('days must be less than 365')
		raise typer.Exit(code=1)
	response = requests.get(f"https://api.coingecko.com/api/v3/coins/{ids}/ohlc?vs_currency={vs_currency}&days={days}")
	p = json.dumps(response.json(), indent=2)
	return typer.echo(p)


@app.command()
def contract_address(
	ids: str = typer.Argument(...,help="asset platform (see asset_platforms endpoint for list of options)"),
	contract_address: str = typer.Argument(...,help="token's contract address"),

):
	""" get coin info from contract address """
	response = requests.get(f"https://api.coingecko.com/api/v3/coins/{ids}/contract/{contract_address}")
	p = json.dumps(response.json(), indent=2)
	return typer.echo(p)


@app.command()
def contract_address_m(
	ids: str = typer.Argument(...,help="asset platform (see asset_platforms endpoint for list of options)"),
	contract_address: str = typer.Argument(...,help="token's contract address"),
	vs_currency: str = typer.Argument("usd",help="the currency you want to compare with."),
	f: int = typer.Argument("0",help="From"),
	t: int = typer.Argument("0",help="To"),
	show_date: bool = typer.Option(False, '-s', help="show date from timestamp")
):
	""" get historical market data include price, market cap... within a range of timestamp """
	if show_date:
		From_date = datetime.fromtimestamp(f)
		To_date = datetime.fromtimestamp(t)
		typer.echo(f"From date = {From_date}")
		typer.echo(f"To date = {To_date}")
	response = requests.get(f"https://api.coingecko.com/api/v3/coins/{ids}/contract/{contract_address}/market_chart/range?vs_currency={vs_currency}&from={f}&to={t}")
	p = json.dumps(response.json(), indent=2)
	return typer.echo(p)


if __name__ == "__main__":
	app()
