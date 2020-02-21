# Moneytree Parser

This script will log you in to your moneytree account and put all your account amounts into a CSV file.

## Setup

```
cp config.example.py config.py
```

Fill in `config.py` with your details.

Run the following script to create the `balance.csv` file.
```
bin/setup
```

## Forcing moneytree to refresh amounts

```
bin/refresh
```

### Parse moneytree to record amounts

```
bin/parse
```
