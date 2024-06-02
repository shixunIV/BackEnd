import subprocess
from multiprocessing import Process
import os


def generate_config():
    if os.path.exists("./config.yml"):
        return
    with open("./config.yml", "w") as file:
        file.write("neo4j:\n")
        file.write("  port: 7687\n")
        file.write("  user: neo4j\n")
        file.write("  password: 12345678\n")
        file.write("openai:\n")
        file.write("  api_key: sk-a8czoHecLh1RoKlq82FeBa497dD4413dAc6c471dB1A83373\n")
        file.flush()


def run_cmd(cmd):
    subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    generate_config()
    cmd_list = [
        "pnpm --dir Web serve",
        "cd gateway && go mod tidy && go run main.go",
        "cd users && go mod tidy && go run main.go",
        "cd neo4j && python main.py",
    ]

    # 创建一个列表来存储进程
    process_list = []

    # 为每个cmd命令创建一个进程，并将进程添加到列表中
    for cmd in cmd_list:
        process = Process(target=run_cmd, args=(cmd,))
        process_list.append(process)

    # 启动所有进程
    for process in process_list:
        process.start()

    # 等待所有进程结束
    for process in process_list:
        process.join()
