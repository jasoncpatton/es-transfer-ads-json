FROM python:3.11-slim-bookworm

RUN python3 -m pip install elasticsearch

ADD --chmod=0755 print_json_results.py /print_json_results.py
