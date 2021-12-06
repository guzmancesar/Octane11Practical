import argparse


argument_parser = argparse.ArgumentParser(description='Interpret CLI args for exchange rates')

argument_parser.add_argument('start', type=str)
argument_parser.add_argument('end', type=str)
argument_parser.add_argument('base', type=str)
argument_parser.add_argument('symbol', type=str)
argument_parser.add_argument('output', type=str)

args = argument_parser.parse_args()
print(args.sum(args.integers))