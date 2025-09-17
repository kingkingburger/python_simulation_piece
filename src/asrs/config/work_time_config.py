class WorkTimeConfig:
    def __init__(self):
          self.inbound_time: float = 1.0
          self.outbound_time: float = 1.0

    def delay_time(self, time: float):
        time.sleep(time)

