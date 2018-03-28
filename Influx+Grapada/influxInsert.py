# {'cpu': {'cpu_temperature': 25.0, 'cpu_usage': '3.4'},
#  'gpu': [{'gpu_free_memory': ' 2241',
#           'gpu_index_id': ' 0',
#           'gpu_name': ' GeForce GTX 1050',
#           'gpu_temperature': ' 46',
#           'gpu_total_memory': ' 4041',
#           'gpu_used_memory': ' 1800',
#           'gpu_uuid': 'GPU-3506f785-594b-4517-e8f0-54ddafe98836'}],
#  'machine': {'machine_ip_address': '172.20.10.10',
#              'machine_name': 'xps',
#              'machine_os_platform': 'Linux'},
#  'memory': {'memory_total': 32128, 'memory_used': 25206}}


# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse

from influxdb import InfluxDBClient


def main(host='13.58.148.61', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'jjeaby'
    password = 'test1111'
    dbname = 'testdb'
    dbuser = 'jjeaby'
    dbuser_password = 'test1111'
    query = 'select value from cpu_load_short;'
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2009-11-10T23:00:00Z",
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + dbuser)
    client.switch_user(dbuser, dbuser_password)

    print("Write : cpu,atag=test1 idle=100,usertime=10,system=1")
    client.write(['cpu,atag=test1 idle=100,usertime=10,system=1'], {'db': dbname}, 204, 'line')

    print("Write points: {0}".format(json_body))
    client.write_points(json_body, database=dbname)
    #
    # print("Querying data: " + query)
    # result = client.query(query)
    #
    # print("Result: {0}".format(result))
    #
    # print("Switch user: " + user)
    # client.switch_user(user, password)
    #
    # print("Drop database: " + dbname)
    # client.drop_database(dbname)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='13.58.148.61',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)