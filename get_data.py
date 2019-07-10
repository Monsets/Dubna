import json
import subprocess
import time
import os

user = 'tut099'
password = 'jggjpbwbz'

path_to_dirs = 'videos'

with open('answers.json') as f:
    data = json.load(f)

libs = ['Bus_11_front_door', 'Bus_11_rear_door', 'Bus_14_front_door', 'Bus_14_rear_door', 'Bus_9_front_door', 'Bus_9_rear_door']

subprocess.call(["mkdir", 'videos/'])
for lib in libs:
    subprocess.call(["mkdir", 'videos/' + lib])

for num, key in enumerate(data.keys()):
    arg1 = key
    arg2 = key.split('/')[1]
    #subprocess.Popen(['sshpass', '-p', password, 'scp', '-r', 'user' + '@hydra.jinr.ru:/zfs/hybrilit.jinr.ru/scratch/HackDubna/Train_data/' + \
    #                  arg1, '/videos/' + arg2])

    time.sleep(6)
    print(arg1, arg2)
    print("Downloaded {} / {}".format(num, len(data.keys())))