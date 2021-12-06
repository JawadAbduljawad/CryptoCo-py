

# CryptoCo-py

[CryptoCo-py](https://github.com/Edmain1/CryptoCo-py) is a Python CLI application that uses [CoinGecko](https://www.coingecko.com/en/api) API to allow the user to query cryptocurrency information
by typing simple commands.

#### Table of contents
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [License](#license)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install cryptoco-py.

```bash
pip install cryptoco-py
```
## Requirements
| Name      | Version |
| :-----------: | :-----------: |
| [Python](https://www.python.org/)      | 3.6 +       |
| [Typer](https://typer.tiangolo.com/)   | 0.4.0 +        |
| [Requests](https://docs.python-requests.org/en/latest/) | 2.26.0 +        |


## Usage

```bash
# pings the server
cryptoco-py [OPTIONS] COMMAND [ARGS]...
```

>NOTE: you might not be able to run the command instantly after installing it
>to solve this problem simply add the directory of the installed package to ```$PATH```

```bash
# returns a help message
cryptoco-py --help
```
you can also write the output to an output file for example:
```bash
cryptoco-py sprice bitcoin > output.txt

cat output.txt
# output:
{
  "bitcoin": {
    "usd": 48338
  }
}

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
