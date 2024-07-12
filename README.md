# es-transfer-ads-json
Print (as JSON) all transfer ads from an AP for a given time period.

## Usage
```shell
docker run -it --rm docker.io/jasoncpatton/transfer-ads-to-json:latest /print_json_results.py \
    --host <elasticsearch-host-URL> \
    --index <elasticsearch-index-pattern> \
    --ap <access-point-hostname> \
    --user <elasticsearch-username> \
    --pass <elasticsearch-password> \
    --start <unix-timestamp> \
    --end <unix-timestamp>
```