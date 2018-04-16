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
import datetime
from influxdb import InfluxDBClient


def main(host='127.0.0.1', port=8086):
    """Instantiate a connection to the InfluxDB."""
    user = 'jjeaby'
    password = 'jjeaby'
    dbname = 'testdb'
    query = 'select value from cpu_load_short;'

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Write : cpu,atag=test1 idle=100,usertime=10,system=1")
    client.write(['cpu,atag=test1 idle=100,usertime=10,system=1'], {'db': dbname}, 204, 'line')

    now = datetime.datetime.now()
    points = []
    point = {
        "measurement": 'chq',
        "time": str(now.strftime('%Y-%m-%d %H:%M:%S')),
        "fields": {
            'machine_ip_address': '192.168.10.210',
            'machine_name': 'rosamia',
            'machine_os_platform': 'Linux',
            'memory_total': 129363,
            'memory_used': 87786,
            'cpu_temperature': 31.0,
            'cpu_usage': '5.5',
            'gpu_free_memory_0': ' 11162',
            'gpu_index_id_0': ' 0',
            'gpu_name_0': ' GeForce GTX 1080 Ti',
            'gpu_temperature_0': ' 49',
            'gpu_total_memory_0': ' 11172',
            'gpu_used_memory_0': ' 10',
            'gpu_uuid_0': 'GPU-fbce4a93-3a20-a778-aa32-4b396f8df6d8',
            'gpu_free_memory_1': ' 6624',
            'gpu_index_id_1': ' 1',
            'gpu_name_1': ' GeForce GTX 1080 Ti',
            'gpu_temperature_1': ' 49',
            'gpu_total_memory_1': ' 11171',
            'gpu_used_memory_1': ' 4547',
            'gpu_uuid_1': 'GPU-5fa30715-d37c-d266-0f11-e76c147b809a',
        }
    }

    points = []
    points.append(point)

    client.write_points(points)


    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Create a retention policy")
    client.create_retention_policy('awesome_policy', '3d', 3, default=True)

    print("Switch user: " + user)
    client.switch_user(user, password)


    print("Querying data: " + query)
    result = client.query(query)

    print("Result: {0}".format(result))

    print("Switch user: " + user)
    client.switch_user(user, password)

    print("Drop database: " + dbname)
    client.drop_database(dbname)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='127.0.0.1',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
