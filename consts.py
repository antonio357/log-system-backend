from enum import Enum


class LogsConn(Enum):
    URL = "ws://192.168.1.199:81"
    START_LOGS_CMD = "start logs"
    STOP_LOGS_CMD = "stop logs"
