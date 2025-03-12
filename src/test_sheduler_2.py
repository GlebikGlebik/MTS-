import json

def main():
    host6 = [
      "vm123",
      "vm130",
      "vm134",
      "vm142",
      "vm17",
      "vm24",
      "vm35",
      "vm42",
      "vm50",
      "vm66",
      "vm72",
      "vm79",
      "vm87",
      "vm91",
      "vm99"
    ]
    while True:
        try:
            # Чтение данных из входного файла
            input_line = input()  # Используем input() для чтения данных по строкам
            if not input_line.strip():  # Если строка пустая, выходим из цикла
                break
            current_input = json.loads(input_line)
            print(current_input)
            sum_cpu = 0
            sum_ram = 0
            for vm, resources in current_input["virtual_machines"].items():
                if vm in host6:
                    sum_cpu += resources['cpu']
                    sum_ram += resources['ram']
                    print()
                    print(vm, resources)
                    print()
                    print("Итого:", sum_cpu, sum_ram)
        except KeyboardInterrupt:
            break  # Позволяет прервать выполнение Ctrl+C

if __name__ == '__main__':
    main()

# 34 - 150 - 70% - host0
# 21 - 99 - 65% - host1
# 34 - 185 - 70%  - host2
# 21 - 98 - 65% - host6