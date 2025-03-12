import json

class Sheduler:
    def __init__(self):
        self.current_input = {}
        self.current_output = {"$schema": "resources/input.schema.json", 'allocations': {}, "allocation_failures": [], 'migrations': {}}
        self.previous_output = {}
        self.previous_input = {}
        self.cpu = None
        self.ram = None
        self.vm = None

    def host_free_space_check(self):
        for host in self.current_input['hosts']:
            self.current_output['allocations'].setdefault(host, [])
        for host in self.current_input['hosts']:
            if self.current_input['hosts'][host]['cpu'] * 0.8 - self.cpu >= self.cpu and self.current_input['hosts'][host][
                'ram'] * 0.8 - self.ram >= self.ram:
                self.current_output['allocations'][host].append(self.vm)
                break
        else:
            self.allocation_failures()

    def allocation_failures(self):
        self.current_output['allocation_failures'].append(self.vm)

    def allocations(self):
        for self.vm in self.current_input["virtual_machines"]:
            self.cpu, self.ram = self.current_input['virtual_machines'][self.vm]['cpu'], self.current_input['virtual_machines'][self.vm]['ram']
            self.host_free_space_check()

    def migrations(self):
        if not self.previous_input:
            return
        for previous_host in self.previous_input['hosts']:
            if self.previous_output['allocations'][previous_host] == self.current_output['allocations'][previous_host]:
                continue
            if not self.previous_output['allocations'][previous_host]:
                pass
            else:
                for vm in self.previous_output['allocations'][previous_host]:
                    for host in self.previous_input['hosts']:
                        if vm in self.current_output['allocations'][host] and host != previous_host:
                            self.current_output['migrations'].setdefault(vm, {'from': previous_host, 'to': host})



    def run(self):
        self.current_output = {"$schema": "resources/input.schema.json", 'allocations': {}, "allocation_failures": [], 'migrations': {}}
        self.allocations()
        self.migrations()
        self.current_output_generation()

    def current_output_generation(self):
        self.previous_output = self.current_output.copy()
        self.previous_input = self.current_input.copy()
        print(json.dumps(self.current_output, ensure_ascii=False, indent=2))
        with open('../resources/output.schema.json', 'w', encoding='utf-8') as output_schema:
            json.dump(self.current_output, output_schema, ensure_ascii=False, indent=2)

def main():
    sh = Sheduler()
    while True:
        try:
            # Чтение данных из входного файла
            input_line = input()  # Используем input() для чтения данных по строкам
            if not input_line.strip():  # Если строка пустая, выходим из цикла
                break
            sh.current_input = json.loads(input_line)
            sh.run()
        except KeyboardInterrupt:
            break  # Позволяет прервать выполнение Ctrl+C

if __name__ == '__main__':
    main()
