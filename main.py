from cli.commands import init, add, list_entries, get, delete
import os
import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="commands")
subparsers.add_parser("init")
subparsers.add_parser("add")
subparsers.add_parser("list_entries")
get_parser = subparsers.add_parser("get")
get_parser.add_argument("name")
getdel_parser = subparsers.add_parser("delete")
getdel_parser.add_argument("name")

args = parser.parse_args()

if args.commands == "init":
    init()

elif args.commands == "add":
    add()

elif args.commands == "list_entries":
    list_entries()
    
elif args.commands == "get":
    get(args.name)

elif args.commands == "delete":
    delete(args.name)