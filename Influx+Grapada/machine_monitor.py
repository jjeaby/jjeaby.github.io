import datetime
import json
import os
import pprint
import socket
import subprocess
import sys
import time

from influxdb import InfluxDBClient

try:
    delay = int(sys.argv[1])
except:
    delay = 4


def machine_information():
    socket_instance = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    machine_info = {}
    try:
        socket_instance.connect(('192.0.0.8', 1027))
        info = os.popen('uname -a').readlines()[-1].split()[0:]
        machine_info = {
            "machine_os_platform": info[0],
            "machine_name": info[1],
            "machine_ip_address": socket_instance.getsockname()[0]
        }

    except socket.error:
        machine_info["machine_ip_address"] = "OffLine"
        return machine_info

    return machine_info


def get_gpu_infomation():
    whereis_nvidia_smi_cmd = [r"whereis", "nvidia-smi"]
    whereis_nvidia_smi_cmd_output = str(subprocess.check_output(whereis_nvidia_smi_cmd))
    whereis_nvidia_smi_path = str(whereis_nvidia_smi_cmd_output.split(" ")[1])
    nvidia_smi_output = [whereis_nvidia_smi_path, "--format=csv,noheader,nounits",
                         "--query-gpu=uuid,index,name,memory.total,memory.used,memory.free,temperature.gpu"]
    gpu_data = str(subprocess.check_output(nvidia_smi_output).decode("utf-8")).split(os.linesep)
    # gpu_data = r'GPU-fbce4a93-3a20-a778-aa32-4b396f8df6d8, 0, GeForce GTX 1080 Ti, 11172, 10, 11162, 35', r'GPU-5fa30715-d37c-d266-0f11-e76c147b809a, 1, GeForce GTX 1080 Ti, 11171, 4547, 6624, 43', ''
    gpu_info = []
    for idx, data in enumerate(gpu_data):
        gpu_value = data.split(",")
        if len(gpu_value) > 1:
            temp_info = {"gpu" + str(idx) + "_uuid": gpu_value[0].strip(),
                         "gpu" + str(idx) + "_index_id": gpu_value[1].strip(),
                         "gpu" + str(idx) + "_name": gpu_value[2].strip(),
                         "gpu" + str(idx) + "_total_memory": gpu_value[3].strip(),
                         "gpu" + str(idx) + "_used_memory": gpu_value[4].strip(),
                         "gpu" + str(idx) + "_free_memory": gpu_value[5].strip(),
                         "gpu" + str(idx) + "_temperature": gpu_value[6].strip()}
            gpu_info.append(temp_info)
    return gpu_info


def memory_information():
    memory_total, memory_used, memory_free = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    memory_info = {
        "memory_total": memory_total,
        "memory_used": memory_used,
        "memory_free": memory_free
    }

    return memory_info


def cpu_infomation():
    cpu_usage = str(round(float(
        os.popen(
            '''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),
        1))

    cpu_info = {"cpu_usage": cpu_usage}
    cpu_temperature = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone0/temp']).decode("utf-8")
    cpu_info["cpu_temperature"] = float(cpu_temperature) / 1000

    return cpu_info


def influxInput(server_info):
    host = '13.58.148.61'
    port = 8086
    """Instantiate a connection to the InfluxDB."""
    user = 'jjeaby'
    password = 'test1111'
    dbname = 'testdb'

    client = InfluxDBClient(host, port, user, password, dbname)

    print("Write : cpu,atag=test1 idle=100,usertime=10,system=1")
    client.write(['cpu,atag=test1 idle=100,usertime=10,system=1'], {'db': dbname}, 204, 'line')

    machine = server_info["machine"]
    cpu = server_info["cpu"]
    memory = server_info["memory"]
    gpu = server_info["gpu"]

    fields_data = {}

    for data in dict(machine.items()):
        fields_data[data] = machine[data].strip()
    for data in dict(cpu.items()):
        fields_data[data] = cpu[data]
    for data in dict(memory.items()):
        fields_data[data] = memory[data]
    for idx, list in enumerate(gpu):
        for data in dict(list.items()):
            fields_data[data] = gpu[idx][data].strip()
    fields_data = json.dumps(fields_data)
    print(fields_data)
    now = datetime.datetime.today()
    print(now)
    points = []
    point = {"measurement": 'machine_information',
             # "time": str(now.strftime('%Y-%m-%d %H:%M:%S')),
             "time": 1000000000 * int(now.strftime('%s')),
             # "fields": fields_data
             }
    point["fields"] = json.loads(fields_data)

    print(point)
    points.append(point)
    ret = client.write_points(points)
    print("DB 입력 성공[" + str(ret) + "]")
    pprint.pprint(point)


if __name__ == '__main__':

    while True:
        server_info = {
            "machine": machine_information(),
            "cpu": cpu_infomation(),
            "gpu": get_gpu_infomation(),
            "memory": memory_information(),
        }

        influxInput(server_info)
        time.sleep(delay)

#
# {'cpu': {'cpu_temperature': 31.0, 'cpu_usage': '5.5'},
#  'gpu': [{'gpu_free_memory': ' 11162',
#           'gpu_index_id': ' 0',
#           'gpu_name': ' GeForce GTX 1080 Ti',
#           'gpu_temperature': ' 49',
#           'gpu_total_memory': ' 11172',
#           'gpu_used_memory': ' 10',
#           'gpu_uuid': 'GPU-fbce4a93-3a20-a778-aa32-4b396f8df6d8'},
#          {'gpu_free_memory': ' 6624',
#           'gpu_index_id': ' 1',
#           'gpu_name': ' GeForce GTX 1080 Ti',
#           'gpu_temperature': ' 49',
#           'gpu_total_memory': ' 11171',
#           'gpu_used_memory': ' 4547',
#           'gpu_uuid': 'GPU-5fa30715-d37c-d266-0f11-e76c147b809a'}],
#  'machine': {'machine_ip_address': '192.168.10.210',
#              'machine_name': 'rosamia',
#              'machine_os_platform': 'Linux'},
#  'memory': {'memory_total': 129363, 'memory_used': 87786}}
