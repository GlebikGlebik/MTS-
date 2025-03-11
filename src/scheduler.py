import json

class Sheduler():
    def __init__(self):
        input_dataset = open('../resources/input.schema.json', 'r', encoding='utf-8')
        self.output_dataset = {"$schema": "resources/input.schema.json", 'allocations': {}, "allocation_failures": []}
        self.input_data = json.load(input_dataset)
        self.cpu = None
        self.ram = None
        self.vm = None

    def host_free_space_check(self):
        for host in self.input_data['hosts']:
            if self.input_data['hosts'][host]['cpu'] * 0.8 - self.cpu >= self.cpu and self.input_data['hosts'][host]['ram'] * 0.8 - self.ram >= self.ram:
                self.output_dataset['allocations'].setdefault(host, []).append(self.vm)
                break
        else:
            self.allocation_failures()

    def allocation_failures(self):
        self.output_dataset['allocation_failures'].append(self.vm)

    def allocations(self):
        for self.vm in self.input_data["virtual_machines"]:
            self.cpu, self.ram = self.input_data['virtual_machines'][self.vm]['cpu'], self.input_data['virtual_machines'][self.vm]['ram']
            self.host_free_space_check()

    def output_schema_creator(self):
        self.allocations()
        with open('../resources/output.schema.json', 'w', encoding='utf-8') as output_schema:
            json.dump(self.output_dataset, output_schema, ensure_ascii=False, indent=2)

def main():
    sh = Sheduler()
    sh.output_schema_creator()

if __name__ == '__main__':
    main()


