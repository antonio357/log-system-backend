import time


class LogsStatus:
    def __init__(self):
        self.msgs = []
        self.corrupted_msgs = []
        self.prev_msg_time = None
        self.msg_time = None

    def currentTimeMili(self):
        return time.time() * 1000

    def checkMsg(self, msg):
        msgs_interval = 0
        if not self.prev_msg_time:
            self.prev_msg_time = self.currentTimeMili()
        else:
            self.msg_time = self.currentTimeMili()
            msgs_interval = self.msg_time - self.prev_msg_time
            self.prev_msg_time = self.msg_time

        if len(msg) == 256:
            self.msgs.append((msg, msgs_interval))
        else:
            self.corrupted_msgs.append((msg, msgs_interval))

    def reset(self):
        self.msgs.clear()
        self.corrupted_msgs.clear()
        self.prev_msg_time = None
        self.msg_time = None

    def printStatus(self):
        if len(self.msgs) + len(self.corrupted_msgs) > 0:
            mean_time = (sum([i[-1] for i in self.msgs]) + sum([i[-1] for i in self.corrupted_msgs])) / (
                len(self.msgs) + len(self.corrupted_msgs))
            print(f"received msgs: {len(self.msgs)} corrupted_msgs: {len(self.corrupted_msgs)} mean time: {mean_time}")
            print(f" msg example = {self.corrupted_msgs[0]}")
        else:
            print("no status")
