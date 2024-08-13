import psutil
from tabulate import tabulate

from .ai_extension import ai_exposed_function


@ai_exposed_function
def list_drive_letters(reason: str = None) -> str:
    """
    This function returns a list of all the drive letters on the computer.
    :param reason: The reason for the function call.
    :return: A string containing the list of drive letters.
    """
    # 获取所有磁盘分区信息
    partitions = psutil.disk_partitions()
    drive_info_list = [collect_partition_info(partition) for partition in partitions]
    # 使用 tabulate 生成表格
    headers = ['分区', '挂载点', '文件系统类型', '总大小', '已用大小', '可用大小', '使用百分比']
    table_str = tabulate(drive_info_list, headers=headers, tablefmt="pretty")
    # 打印表格
    return table_str


def collect_partition_info(partition):
    partition_usage = psutil.disk_usage(partition.mountpoint)
    if partition_usage is None:
        return [
            partition.device,
            partition.mountpoint,
            partition.fstype,
            "unknown",
            "unknown",
            "unknown",
            "unknown"
        ]
        # return {
        #     "分区": partition.device,
        #     "挂载点": partition.mountpoint,
        #     "文件系统类型": partition.fstype,
        #     "总大小": "unknown",
        #     "已用大小": "unknown",
        #     "可用大小": "unknown",
        #     "使用百分比": "unknown"
        # }
    return [
        partition.device,
        partition.mountpoint,
        partition.fstype,
        f"{partition_usage.total / (1024 ** 3):.2f} GB",
        f"{partition_usage.used / (1024 ** 3):.2f} GB",
        f"{partition_usage.free / (1024 ** 3):.2f} GB",
        f"{partition_usage.percent}%"
    ]
    # return {
    #     "分区": partition.device,
    #     "挂载点": partition.mountpoint,
    #     "文件系统类型": partition.fstype,
    #     "总大小": f"{partition_usage.total / (1024 ** 3):.2f} GB",
    #     "已用大小": f"{partition_usage.used / (1024 ** 3):.2f} GB",
    #     "可用大小": f"{partition_usage.free / (1024 ** 3):.2f} GB",
    #     "使用百分比": f"{partition_usage.percent}%"
    # }


def touch():
    pass
