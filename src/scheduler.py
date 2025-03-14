import json

class Sheduler:
    def __init__(self):
        self.current_input = {}
        self.current_output = {
            "$schema": "resources/input.schema.json",
            'allocations': {},
            "allocation_failures": [],
            'migrations': {}
        }
        self.previous_output = {}
        self.previous_input = {}
        self.vm_cpu = None
        self.vm_ram = None
        self.vm = None
        self.process = None
        self.sorted_hosts = None
        self.test_output = {}

    def host_free_space_check(self):
        # Сортируем хосты по текущей загруженности
        sorted_hosts = sorted(self.current_input['hosts'].items(), key=lambda item: (
            sum(self.current_input['virtual_machines'][vm]['cpu'] for vm in
                self.current_output['allocations'].get(item[0], [])) / item[1]['cpu'],
            sum(self.current_input['virtual_machines'][vm]['ram'] for vm in
                self.current_output['allocations'].get(item[0], [])) / item[1]['ram']
        ))

        for host in self.current_input['hosts']:
            self.current_output['allocations'].setdefault(host, [])

        for host in sorted_hosts:
            # Считаем использованные ресурсы
            used_cpu = sum(
                self.current_input['virtual_machines'][vm]['cpu'] for vm in self.current_output['allocations'][host[0]])
            used_ram = sum(
                self.current_input['virtual_machines'][vm]['ram'] for vm in self.current_output['allocations'][host[0]])

            # Проверяем, можно ли разместить ВМ
            if (used_cpu + self.vm_cpu <= host[1]['cpu'] * 0.8) and (used_ram + self.vm_ram <= host[1]['ram'] * 0.8):
                self.current_output['allocations'][host[0]].append(self.vm)
                return  # ВМ успешно размещена, выходим из функции

        # Если не удалось разместить ВМ, вызываем отметку о невозможности размещения
        self.allocation_failures()

    def allocation_failures(self):
        self.current_output['allocation_failures'].append(self.vm)

    def allocations(self):
        # Сортируем все вм по их требованиям по убыванию
        sorted_vms = sorted(self.current_input["virtual_machines"].items(),
                            key=lambda item: (item[1]['cpu'] + item[1]['ram']),
                            reverse=True)

        for self.vm, resources in sorted_vms:
            self.vm_cpu, self.vm_ram = resources['cpu'], resources['ram']
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
        self.current_output = {"$schema": "resources/input.schema.json", 'allocations': {}, "allocation_failures": [],
                               'migrations': {}}
        self.allocations()
        self.migrations()
        self.current_output_generation()

    def current_output_generation(self):
        self.previous_output = self.current_output.copy()
        self.previous_input = self.current_input.copy()
        print(json.dumps(self.current_output, ensure_ascii=False, indent=2))


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

