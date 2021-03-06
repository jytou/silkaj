#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from commandlines import Command
from commands import *


def usage():
    print("Silkaj: command line Duniter client \
    \n\nhelp: -h, --help, --usage \
    \nversion: -v, --version \
    \n \
    \nCustom endpoint with option `-p` and <domain>:<port>\
    \n \
    \nCommands: \
    \n - info: Display information about currency \
    \n \
    \n - amount: Get amount of one account \
    \n      --pubkey=<pubkey[:checksum]> | --auth-scrypt\
    \n      --auth-seed | --auth-file\
    \n \
    \n - transaction: Send transaction\
    \n     --auth-scrypt | --auth-seed | --auth-file [--file=<path file>]\
    \n     --amountDU=<relative value> | --amount=<quantitative value>\
    \n     --output=<public key>[:checksum] \
    \n     [--comment=<comment>] \
    \n     [--allSources] \
    \n     [--outputBackChange=<public key[:checksum]>] \
    \n     -y | --yes, don't ask for prompt confirmation \
    \n \
    \n - network: Display current network with many information \
    \n      [--discover]     Discover all network (could take a while), optional \
    \n      [-s, --sort]     Sort column names comma-separated (for example \"-s block,diffi\"), optional \
    \n                       Default sort is block,member,diffi,uid \
    \n \
    \n - diffi: list proof-of-work difficulty to generate next block \
    \n \
    \n - issuers n: display last n issuers (`0` for all blockchain) \
    \n      last issuers are displayed under n <= 30.\
    \n      To force display last ones, use `--last` option\
    \n \
    \n - argos: display currency information formated for Argos or BitBar\
    \n \
    \n - generate_auth_file: Generate file to store the seed of the account\
    \n      --auth-scrypt | --auth-seed \
    \n      [--file=<path file>] \
    \n \
    \n - id <pubkey> or <identity>: get corresponding identity or pubkey from pubkey or identity.\
    \n      it could autocomplete the pubkey corresponding to an identity with three or four following characters.")
    exit()


def cli():
    # ep: endpoint, node's network interface
    ep, c = dict(), Command()
    subcmd = ["info", "diffi", "network", "issuers", "argos", "amount", "transaction", "generate_auth_file", "id"]
    if c.is_help_request() or c.is_usage_request() or c.subcmd not in subcmd:
        usage()
    if c.is_version_request():
        print("silkaj 0.2.0")
        exit()
    ep["domain"], ep["port"] = "duniter.org", "10901"
    try:
        ep["domain"], ep["port"] = c.get_definition('p').rsplit(':', 1)
    except:
        print("Requested default node: <{}:{}>".format(ep["domain"], ep["port"]), file=sys.stderr)
    if ep["domain"].startswith('[') and ep["domain"].endswith(']'):
        ep["domain"] = ep["domain"][1:-1]
    return ep, c


def manage_cmd(ep, c):
    if c.subcmd == "info":
        currency_info(ep)

    elif c.subcmd == "diffi":
        difficulties(ep)

    elif c.subcmd == "network":
        from commands import set_network_sort_keys
        if c.contains_switches("sort"):
            set_network_sort_keys(c.get_definition("sort"))
        if c.contains_switches("s"):
            set_network_sort_keys(c.get_definition("s"))
        network_info(ep, c.contains_switches("discover"))

    elif c.subcmd == "issuers" and c.subsubcmd and int(c.subsubcmd) >= 0:
        list_issuers(ep, int(c.subsubcmd), c.contains_switches('last'))

    elif c.subcmd == "argos":
        argos_info(ep)

    elif c.subcmd == "amount" and c.subsubcmd:
        cmd_amount(ep, c)

    elif c.subcmd == "transaction":
        cmd_transaction(ep, c)

    elif c.subcmd == "generate_auth_file":
        generate_auth_file(c)

    elif c.subcmd == "id":
        id_pubkey_correspondence(ep, c.subsubcmd)


if __name__ == '__main__':
    ep, c = cli()
    check_port(ep["port"])
    best_node(ep, 1)
    manage_cmd(ep, c)
