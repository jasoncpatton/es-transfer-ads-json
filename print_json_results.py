#!/usr/bin/env python3
"""Print (as JSON) all transfer ads from an AP for a given time period."""

import argparse
import time
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


def get_query(index: str, ap: str, start: int, end: int) -> dict:
    """Get the Elasticsearch query"""
    query = {
        "index": index,
        "track_scores": False,  # Reduce query overhead since we're not using scores
        "query": {
            "bool": {
                "filter": [
                    {"term": {  # Return only for the PATh facility
                        "ScheddName": ap,
                    }},
                    {"terms": {  # Return only stash, osdf, or pelican protocols
                        "TransferProtocol": ["stash", "osdf", "pelican"],
                    }},
                    {"range": {  #  Return only from the specific time range
                        "RecordTime": {
                            "gte": start,
                            "lt": end,
                        }
                    }}
                ]
            }
        }
    }
    return query


def main():
    """Run the main program"""

    # fetch arguments
    args = parse_args()

    # create the Elasticsearch client with auth as needed
    client_kwargs = {}
    if args.username is not None:
        client_kwargs["basic_auth"] = (args.username, args.password,)
    client = Elasticsearch(args.host, **client_kwargs)

    # run the Elasticsearch query
    query = get_query(index=args.index, ap=args.ap, start=args.start, end=args.end)
    results = scan(client, query=query, scroll="20s")

    # print results as JSON
    print(json.dumps([doc["_source"] for doc in results], indent=2))


def parse_args() -> argparse.Namespace:
    """Parse commandline arguments"""

    parser = argparse.ArgumentParser(description="Print (as JSON) all transfer ads from an AP for a given time period.")
    parser.add_argument("--host", type=str, required=True, help="Elasticsearch host")
    parser.add_argument("--index", type=str, required=True, help="Elasticsearch index (or index pattern)")
    parser.add_argument("--ap", type=str, required=True, help="Access point name")
    parser.add_argument("--user", type=str, dest="username", help="Elasticsearch username (requires password)")
    parser.add_argument("--pass", type=str, dest="password", help="Elasticsearch password")
    parser.add_argument("--start", type=int, default=int(time.time()) - 24*3600, help="Starting Unix timestamp")
    parser.add_argument("--end", type=int, default=int(time.time()), help="Ending Unix timestamp")
    args = parser.parse_args()
    if args.username is not None and args.password is None:
        parser.error("--pass is required if --user is set")
    return args


if __name__ == "__main__":
    main()
