from pathlib import Path
permanent_file = Path("./configs/ban_list_permanent")


class BanHammer:
    def __init__(self):
        self.banned = dict()
        with permanent_file.open() as f:
            rows = f.readlines()
            for row in rows:
                s = row.split(';')
                self.banned[s[0]] = s[1]
