import subprocess
from multiprocessing import Process


def run_cmd(cmd):
    subprocess.Popen(cmd, shell=True)


if __name__ == "__main__":
    cmd_list = [
        "pnpm --dir Web serve",
        "cd gateway && go mod tidy && go run main.go",
        "cd patient && go mod tidy && go run main.go",
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
