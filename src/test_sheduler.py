import sys
import json
from src.draft_sheduler import *


class Tester:
    def __init__(self):
        self.sh = Sheduler()
        self.current_output = {}
        self.test_output = {}

    def tester(self):
        for host, host_resources in self.sh.current_input['hosts'].items():
            used_cpu, used_ram = 0, 0
            for vm in self.current_output['allocations'].get(host, []):
                used_cpu += self.sh.current_input['virtual_machines'][vm]['cpu']
                used_ram += self.sh.current_input['virtual_machines'][vm]['ram']
            self.test_output.setdefault(host, {'cpu': f'загружено на {used_cpu * 100 / host_resources["cpu"]}%','ram': f'загружено на {used_ram * 100 / host_resources["ram"]}%'})


def main():
    test = Tester()
    while True:
        try:
            input_line = sys.stdin.read()  # Чтение всех данных из stdin
            if not input_line.strip():  # Если строка пустая, выходим из цикла
                break

            test.current_output = json.loads(input_line)
            test.tester()
            print(json.dumps(test.test_output, ensure_ascii=False, indent=2))

        except KeyboardInterrupt:
            break  # Позволяет прервать выполнение Ctrl+C


if __name__ == '__main__':
    main()