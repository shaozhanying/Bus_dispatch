def build():  # 读取dict.dic，构建字典
    fhand = open("dict.dic", "r")  # 文件地址自行更改
    DICT = {'TOTAL_STATION': 5, 'STRATEGY': 'FCFS', 'DISTANCE': 2}  # 初始化字典，设置默认值
    for line in fhand:  # 读取文件，更新字典
        line = line.split("=")
        if(line[1].strip().isdigit()):  # 如果是数字，则转换为int
            DICT[line[0].strip()] = int(line[1].strip())
        else:
            DICT[line[0].strip()] = line[1].strip()
    fhand.close()
    return DICT  # 返回DICT

# 构建配置文件


global dict
dict = build()

# 构建读取指令的函数

# 构建时间全局变量
global time
time = 0


def get_instructions():
    instructions = []  # 初始化指令列表
    for line in iter(input, ''):  # 读取每一行指令，以空行结束
        instructions.append(line.rstrip())
    return instructions

# 构建输出函数


class BUS(object):
    def __init__(self):
        self.target = [0]*dict['TOTAL_STATION']
        self.clockwise = [0] * dict['TOTAL_STATION']
        self.counterclockwise = [0] * dict['TOTAL_STATION']
        self.direction = 0
        self.position = 0
        self.tar = 0
        self.hang = []

    def change_direction(self, direction):  # 改变方向，传入一个参数，即方向，0静止，1向前，-1向后
        self.direction = direction
    
    def If_move(self):  # 如果还有指令就return True，没指令就Return False
        for i in range(len(bus.clockwise)):
            if bus.clockwise[i] != 0 or bus.counterclockwise[i] != 0 or bus.target[i] != 0:
                return True
        else:
            return False
    
    def update_target(self, address, sign):  # 更新target，传入两个参数，一个是地址（车站号），一个是状态（1表示未到达，0表示到达）
        if sign == 1:
            self.target[address-1] = 1
        elif sign == 0:
            self.target[address-1] = 0
# 更新clockwise，传入两个参数，一个是地址（车站号），一个是状态（1表示未到达，0表示到达）

    def update_clockwise(self, address):
        self.clockwise[address-1] = 1

    # 更新counterclockwise，传入两个参数，一个是地址（车站号），一个是状态（1表示未到达，0表示到达）
    def update_counterclockwise(self, address):
        # if sign == 1:
        #     self.counterclockwise[address-1] = 1
        # elif sign == 0:
        #     self.counterclockwise[address-1] = 0
        self.counterclockwise[address-1] = 1

    def remove_target(self, item):
        self.clockwise[item] = 0
        self.counterclockwise[item] = 0
        self.target[item] = 0


class STATION(object):  # 结点
    def __init__(self, position):
        self.position = position
        self.next = None
        self.prev = None
    
    clockwise = [0] * dict['TOTAL_STATION']  # 构建clockwise列表
    counterclockwise = [0] * dict['TOTAL_STATION']  # 构建counterclockwise列表

    def update_clockwise(self, address, sign):  # 更新clockwise，传入两个参数，一个是地址（车站号），一个是状态（1表示未到达，0表示到达）
        if sign == 1:
            self.clockwise[address-1] = 1
        elif sign == 0:
            self.clockwise[address-1] = 0
    
    def update_counterclockwise(self, address, sign):  # 更新counterclockwise，传入两个参数，一个是地址（车站号），一个是状态（1表示未到达，0表示到达）
        if sign == 1:
            self.counterclockwise[address-1] = 1
        elif sign == 0:
            self.counterclockwise[address-1] = 0


class Roundlink(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def append(self, item):  # 在尾部增加一个结点，并与上一个结点双向连接，没有结点则创建结点，头结点设置的不是空结点，
        """尾部添加元素"""
        node = STATION(item)
        if self.is_empty():
            self._head = node
        else:
            cur = self._head
            while cur.next is not None:
                cur = cur.next
            cur.next = node
            node.prev = cur

    def round(self):  # 链表首尾相连，形成循环，记住最后用，因为如果用了就意味着链表的next永远不等于None
        cur = self._head
        while cur.next != None:
            cur = cur.next
        cur.next = self._head
        self._head.prev = cur


def create(a, b):  # 创建链表
    for i in range(a*b):
        Stations.append(i)


def FCFS():  # 先来先服务策略
    def print_result(bus, station, time):  # 传入三个参数，一个是bus，一个是station，一个是时间
        print("TIME:", time)
        print("BUS:")
        print("position:"+str(bus.position))
        print("target:"+"".join(map(str, bus.target)))
        print("STATION:")
        print("clockwise:"+"".join(map(str, station.clockwise)))
        print("counterclockwise:"+"".join(map(str, station.counterclockwise)))  # 删掉换行符，符合文档要求
    
    bus = BUS()  # 初始化bus
    station = STATION(0)  # 初始化station
    instructions = get_instructions()  # 读取指令
    global time  # 引用全局变量time
    print_result(bus, station, time)  # 输出初始状态
    time += 1
    global move_instructions
    global counter  # move_instruction计数器
    counter = 0
    move_instructions = []
    for instruction in instructions:
        if instruction == 'clock' or instruction == 'end':
            continue
        instruction = instruction.split(" ")
        move_instructions.append((instruction[0], int(instruction[1])))
    global current_instruction
    current_instruction = ("", 0, 0)

    def isdone(current_instruction):  # 判断当前指令是否完成
        if bus.position == (current_instruction[1] - 1) * dict['DISTANCE'] and current_instruction[2] == 1:
            return True
        else:
            return False
    
    def select_direction(bus, address):
        judge_direction = {"clockwise": 0, "counterclockwise": 0}
        difference = (address - 1)*dict['DISTANCE'] - bus.position
        if difference > 0:
            judge_direction["clockwise"] = difference
            judge_direction["counterclockwise"] = dict['DISTANCE'] * dict['TOTAL_STATION'] - difference
        elif difference < 0:
            judge_direction["counterclockwise"] = -difference
            judge_direction["clockwise"] = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
        elif difference == 0:
            bus.change_direction(0)
            return None
        
        if judge_direction["clockwise"] > judge_direction["counterclockwise"]:
            bus.change_direction(-1)
        elif judge_direction["clockwise"] < judge_direction["counterclockwise"]:
            bus.change_direction(1)
        else:
            bus.change_direction(1)
               
    for instruction in instructions:
        instruction = instruction.split(" ")

        if instruction[0] == "clock":  # 如果是clock指令
            bus.position = bus.position + bus.direction
            if bus.position < 0:
                bus.position = dict['DISTANCE'] * dict['TOTAL_STATION'] + bus.position
            if bus.position >= dict['DISTANCE'] * dict['TOTAL_STATION']:
                bus.position = bus.position - dict['DISTANCE'] * dict['TOTAL_STATION']  # 如果position大于总长度，则做减法
            if current_instruction[2] == 0:  # 当前指令完成
                # 根据当前指令的状态更新station的clockwise和counterclockwise或者更新bus的target
                if current_instruction[0] == "target":
                    bus.update_target(current_instruction[1], 0)
                elif current_instruction[0] == "clockwise":
                    station.update_clockwise(current_instruction[1], 0)
                elif current_instruction[0] == "counterclockwise":
                    station.update_counterclockwise(current_instruction[1], 0)
                
                if counter != len(move_instructions):
                    while current_instruction[1] == move_instructions[counter][1]:
                        if move_instructions[counter][0] == "target":
                            bus.update_target(move_instructions[counter][1], 0)
                        elif move_instructions[counter][0] == "clockwise":
                            station.update_clockwise(move_instructions[counter][1], 0)
                        elif move_instructions[counter][0] == "counterclockwise":
                            station.update_counterclockwise(move_instructions[counter][1], 0)
                        counter = counter + 1
                    current_instruction = (move_instructions[counter][0], move_instructions[counter][1], 1)
                    counter = counter + 1
                select_direction(bus, current_instruction[1])
            
            else:  # 当前指令未完成
                if isdone(current_instruction):  # 判断当前指令是否完成
                    current_instruction = (current_instruction[0], current_instruction[1], 0)
                    bus.change_direction(0)

            print_result(bus, station, time)
            time = time + 1
        elif instruction[0] == "target":  # 如果是target指令
            bus.update_target(int(instruction[1]), 1)
        
        elif instruction[0] == "clockwise":
            station.update_clockwise(int(instruction[1]), 1)

        elif instruction[0] == "counterclockwise":
            station.update_counterclockwise(int(instruction[1]), 1)

        elif instruction[0] == "end": 
            break


def SSTF():  # 最短寻道策略
    global Stations
    global bus
    global station  # station是游标
    global dict
    global instructions
    global cnt
    global _TIME
    _TIME = 0
    dict = build()
    Stations = Roundlink()  # Stations 是链表
    bus = BUS()
    create(dict['TOTAL_STATION'], dict['DISTANCE'])
    Stations.round()
    station = Stations._head

    def Move_func():  # 根据bus的状态移动一次
        global station
        global dict
        global bus
        global cnt
        if (bus.tar-1)*dict['DISTANCE'] == station.position:  # 公交车到达指令地点，停下消除指令
            bus.remove_target(bus.tar-1)
            bus.tar = 0
            bus.direction = 0
            cnt = 1
            return
        if bus.direction == -1:
            if station.position % dict['DISTANCE'] == 0:  # 顺便服务
                i = station.position//dict['DISTANCE']
                if bus.counterclockwise[i] == 1 or bus.target[i] == 1:
                    bus.counterclockwise[i] = 0
                    bus.target[i] = 0
                    return 0
            station = station.prev
        elif bus.direction == 1:
            if station.position % dict['DISTANCE'] == 0:
                i = station.position//dict['DISTANCE']
                if bus.clockwise[i] == 1 or bus.target[i] == 1:
                    bus.clockwise[i] = 0
                    bus.target[i] = 0
                    return 0
            station = station.next

    def get_instruct():
        orders = []
        f = open("C:\\Users\\15695\\Desktop\\SSTF\\12-沿某个方向行驶-in.txt", 'rt')
        for line in f:
            line = line.rstrip()
            orders.append(line)
        return orders

    def _Distance(item):  # 返回最短对某一个节点的顺逆最短路径,item=i+1
        global dict
        global station
        wise = 0
        counter = 0
        cur = station
        while cur.position != (item)*dict['DISTANCE']:
            cur = cur.next
            wise += 1
        cur = station
        while cur.position != (item)*dict['DISTANCE']:
            cur = cur.prev
            counter += 1
        if wise == 0 or counter == 0:
            return 0, 0
        elif wise <= counter:
            return wise, 1
        else:
            return counter, -1

    def print_sstf():
        global station
        global bus
        print('TIME:'+str(_TIME))
        print('Bus:')
        print('positon:'+str(station.position))
        print("target:"+"".join(map(str, bus.target)))
        print('STATION:')
        print("clockwise:"+"".join(map(str, bus.clockwise)))
        print("counterclockwise:"+"".join(map(str, bus.counterclockwise))+'\n')

    def _Direction():  # 每次clock输出前判断方向并作出一次移动（顺，逆，或不动）
        global bus
        global station
        global dict
        global cnt
        if not bus.If_move():
            return
        if bus.tar == 0:  # bus.tar==0?
            _min = 100
            target_station_wise = 0
            target_station_counter = 0
            for i in range(len(bus.clockwise)):  # 用来判断哪个站最近
                if bus.clockwise[i] == 1 or bus.counterclockwise[i] == 1 or bus.target[i] == 1:
                    a, b = _Distance(i)
                    if a == 0:
                        break
                    if _min >= a:
                        if b == 1:
                            target_station_wise = i+1
                            target_station_counter = 0
                        elif b == -1 and _min > a:
                            target_station_wise = 0
                            target_station_counter = i+1
                        _min = a
            if a == 0:
                bus.remove_target(i)
                cnt = 1
                return
            if target_station_wise == 0:
                bus.direction = -1
                bus.tar = target_station_counter
            else:
                bus.direction = 1
                bus.tar = target_station_wise
            Move_func()
        else:  # 当前确定指令未完成
            Move_func()
            return 0
    instructions = get_instruct()
    print_sstf()
    for order in instructions:
        if 'end' in order:
            print_sstf()
            return 0
        if 'counterclockwise' in order:
            a = eval(order[-1])
            if cnt == 0:
                bus.counterclockwise[a-1] = 1
            else:
                bus.hang.append(order)
        elif 'target' in order:
            a = eval(order[-1])
            if cnt == 0:
                bus.target[a-1] = 1
            else:
                bus.hang.append(order)
        elif 'clockwise' in order:
            a = eval(order[-1])
            if cnt == 0:
                bus.clockwise[a-1] = 1
            else:
                bus.hang.append(order)
        elif 'clock' in order:
            _TIME += 1
            _Direction()
            print_sstf()
            cnt = 0
            for orders in bus.hang:
                if 'target' in orders:
                    a = eval(orders[-1])
                    bus.target[a-1] = 1
                elif 'counterclockwise' in orders:
                    a = eval(order[-1])
                    bus.counterclockwise[a-1] = 1
                elif 'clockwise' in orders:
                    a = eval(orders[-1])
                    bus.clockwise[a-1] = 1
                bus.hang = []


def SCAN():  # 顺便服务策略
    # 构建输出函数
    def print_result(bus, station, time):  # 传入三个参数，一个是bus，一个是station，一个是时间
        print("TIME:", time)
        print("BUS:")
        print("position:"+str(bus.position))
        print("target:"+"".join(map(str, bus.target)))
        print("STATION:")
        print("clockwise:"+"".join(map(str, station.clockwise)))
        print("counterclockwise:"+"".join(map(str, station.counterclockwise)))  # 删掉换行符，符合文档要求
    
    bus = BUS()  # 初始化bus
    station = STATION(0)  # 初始化station
    instructions = get_instructions()  # 读取指令
    global time
    time = 0
    print_result(bus, station, time)  # 输出初始状态
    move_instructions = []  # 待完成指令列表
    current_instruction = ("", 0, 0, 0)  # 指令元组

    t = 0
    while 1:  # 判断第一次运行
        instruction = instructions[t]
        t += 1
        instruction = instruction.split(" ")
        if(instruction[0] != 'clock'):
            move_instructions.append((instruction[0], int(instruction[1])))  # 添加元组
        if(instructions[t] == 'clock'):  # 读取完第一次运行的请求
            break
        
    def passingly_service(bus, station):  # 判断是否构成顺便服务函数
        address = int(bus.position / dict['DISTANCE'] + 1)
        sign = 0
        if bus.target[address - 1] == 1:
            sign = 1
        elif station.clockwise[address - 1] == 1:
            sign = 1
        elif station.counterclockwise[address - 1] == 1:
            sign = 1
        return sign
        
    def distance(bus, address):  # 判断去往某一站点的距离和最近方向
        judge_direction = {"clockwise": 0, "counterclockwise": 0}
        difference = (address - 1)*dict['DISTANCE'] - bus.position
        direction = 0  # 0不动， 1顺时针，-1逆时针
        # 判断距离
        if difference > 0:
            judge_direction["clockwise"] = difference
            judge_direction["counterclockwise"] = dict['DISTANCE'] * dict['TOTAL_STATION'] - difference
        elif difference < 0:
            judge_direction["counterclockwise"] = -difference
            judge_direction["clockwise"] = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
        elif difference == 0:
            bus.change_direction(0)
            return None
        # 判断方向
        if judge_direction["clockwise"] > judge_direction["counterclockwise"]:  # 如果顺时针更远的话，选择逆时针方向
            bus.change_direction(-1)
            direction = -1
        elif judge_direction["clockwise"] < judge_direction["counterclockwise"]:  # 如果逆时针更远的话，选择顺时针方向
            bus.change_direction(1)
            direction = 1
        else:
            bus.change_direction(1)  # 距离相同选择顺时针
            direction = 1
        return min(judge_direction["clockwise"], judge_direction["counterclockwise"]), direction  # 返回距离该站点最近的距离和方向

    def slect_move(move_instructions, bus):  # 运行路线判断函数
        num = len(move_instructions)  # 判断有几个待完成指令
        mindistance = dict['DISTANCE'] * dict['TOTAL_STATION']  # 待完成指令中最短距离
        address = 1  # 最近站点
        request = ''  # 要求
        for first_move in range(num):
            dis, direct = distance(bus, move_instructions[first_move][1])
            if dis < mindistance:
                mindistance = dis
                request = move_instructions[first_move][0]
                address = move_instructions[first_move][1]
                final_direction = direct
        return request, address, final_direction
    
    def isdone(current_instruction):  # 判断当前指令是否完成
        if bus.position == (current_instruction[1] - 1) * dict['DISTANCE'] and current_instruction[3] == 1:
            return True
        else:
            return False

    def direction_distance(bus, station, direction, instruction):
        if instruction == "target":
            if(direction == 1):
                max = [0, 0]
                min = [0, dict["DISTANCE"] * dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if bus.target[i] == 0:
                        continue
                    else:
                        difference = i*dict['DISTANCE'] - bus.position
                        if difference < 0:
                            difference = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0], max[1]), (min[0], min[1])
            elif(direction == -1):
                max = [0, 0]
                min = [0, dict["DISTANCE"] * dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if bus.target[i] == 0:
                        continue
                    else:
                        difference = bus.position - i*dict['DISTANCE']
                        if difference < 0:
                            difference = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0], max[1]), (min[0], min[1])
        elif instruction == "clockwise":
            if(direction == 1):
                max = [0, 0]
                min = [0, dict["DISTANCE"] * dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.clockwise[i] == 0:
                        continue
                    else:
                        difference = i*dict['DISTANCE'] - bus.position
                        if difference < 0:
                            difference = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0], max[1]), (min[0], min[1])
            elif(direction == -1):
                max = [0, 0]
                min = [0, dict["DISTANCE"] * dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.clockwise[i] == 0:
                        continue
                    else:
                        difference = bus.position - i*dict['DISTANCE']
                        if difference < 0:
                            difference = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0], max[1]), (min[0], min[1])
        elif instruction == "counterclockwise":
            if(direction == 1):
                max = [0, 0]
                min = [0, dict["DISTANCE"] * dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.counterclockwise[i] == 0:
                        continue
                    else:
                        difference = i*dict['DISTANCE'] - bus.position
                        if difference < 0:
                            difference = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0], max[1]), (min[0], min[1])
            elif(direction == -1):
                max = [0, 0]
                min = [0, dict["DISTANCE"] * dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.counterclockwise[i] == 0:
                        continue
                    else:
                        difference = bus.position - i*dict['DISTANCE']
                        if difference < 0:
                            difference = dict['DISTANCE'] * dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0], max[1]), (min[0], min[1])

    def determine_move(bus, station, current_instruction):
        if current_instruction[2] == 1:
            target_max, target_min = direction_distance(bus, station, 1, "target")
            clockwise_max, clockwise_min = direction_distance(bus, station, 1, "clockwise")
            counterclockwise_max, counterclockwise_min = direction_distance(bus, station, 1, "counterclockwise")
            if min(target_min[1], clockwise_min[1], counterclockwise_min[1]) * 2 > dict['DISTANCE'] * dict['TOTAL_STATION']:
                target_max, target_min = direction_distance(bus, station, -1, "target")
                clockwise_max, clockwise_min = direction_distance(bus, station, -1, "clockwise")
                counterclockwise_max, counterclockwise_min = direction_distance(bus, station, -1, "counterclockwise")
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x: x[1])
                return -1, (max_list[2][2], max_list[2][0])

            else:
                # 把target_max, clockwise_max, counterclockwise_max 三个元组按照第二个元素排序
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x: x[1])
                return 1, (max_list[2][2], max_list[2][0])
        elif current_instruction[2] == -1:
            target_max, target_min = direction_distance(bus, station, -1, "target")
            clockwise_max, clockwise_min = direction_distance(bus, station, -1, "clockwise")
            counterclockwise_max, counterclockwise_min = direction_distance(bus, station, -1, "counterclockwise")
            if min(target_min[1], clockwise_min[1], counterclockwise_min[1]) * 2 > dict['DISTANCE'] * dict['TOTAL_STATION']:
                target_max, target_min = direction_distance(bus, station, 1, "target")
                clockwise_max, clockwise_min = direction_distance(bus, station, 1, "clockwise")
                counterclockwise_max, counterclockwise_min = direction_distance(bus, station, 1, "counterclockwise")
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x: x[1])
                return 1, (max_list[2][2], max_list[2][0])

            else:
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x: x[1])
                return -1, (max_list[2][2], max_list[2][0])

    sign = 0
    passingly_sign = 0

    for instruction in instructions:
        instruction = instruction.split(" ")

        if instruction[0] == 'clock':
            time += 1  # 每读到clock计时
            if(sign != 0 and current_instruction[0] == ""):  # 如果sign不为0的时候获得first_move_instruction
                first_move_request, first_move_address, first_move_direction = slect_move(move_instructions, bus)
                current_instruction = (first_move_request, first_move_address, first_move_direction, 1)
                bus.change_direction(first_move_direction)

            if passingly_sign == 1:
                bus.change_direction(0)
                address = int(bus.position / dict['DISTANCE'] + 1)
                if bus.target[address - 1] == 1:
                    bus.update_target(address, 0)
                if station.clockwise[address - 1] == 1:
                    station.update_clockwise(address, 0)
                if station.counterclockwise[address - 1] == 1:
                    station.update_counterclockwise(address, 0)
                passingly_sign = 0
            bus.position = bus.position + bus.direction
            bus.change_direction(current_instruction[2])
            if bus.position < 0:
                bus.position = dict['DISTANCE'] * dict['TOTAL_STATION'] + bus.position
            if bus.position >= dict['DISTANCE'] * dict['TOTAL_STATION']:
                bus.position = bus.position - dict['DISTANCE'] * dict['TOTAL_STATION']  # 如果position大于总长度，则做减法
            if current_instruction[3] == 0:  # 当前指令完成
                # 根据当前指令的状态更新station的clockwise和counterclockwise或者更新bus的target
                address = int(bus.position / dict['DISTANCE'] + 1)
                if bus.target[address - 1] == 1:
                    bus.update_target(address, 0)
                if station.clockwise[address - 1] == 1:
                    station.update_clockwise(address, 0)
                if station.counterclockwise[address - 1] == 1:
                    station.update_counterclockwise(address, 0)
                
                # 检查方向是否发生变化, 最长（目标），最短（方向）
                if(current_instruction[0] != ""):
                    direction, destination = determine_move(bus, station, current_instruction)
                    bus.change_direction(direction)
                    current_instruction = (destination[0], destination[1], direction, 1)
            else:  # 当前指令未完成
                if isdone(current_instruction):  # 判断当前指令是否完成
                    current_instruction = (current_instruction[0], current_instruction[1], current_instruction[2], 0)
                    bus.change_direction(0)
                # 判断是否能顺便服务
                if(bus.position % dict['DISTANCE'] == 0 and bus.position != (current_instruction[1] - 1)*dict['DISTANCE']):
                    passingly_sign = passingly_service(bus, station)
            
            print_result(bus, station, time)
        elif instruction[0] == "target":  # 如果是target指令
            if(sign == 0):
                sign = 1
            bus.update_target(int(instruction[1]), 1)
        
        elif instruction[0] == "clockwise":
            if(sign == 0):
                sign = 1
            station.update_clockwise(int(instruction[1]), 1)

        elif instruction[0] == "counterclockwise":
            if(sign == 0):
                sign = 1
            station.update_counterclockwise(int(instruction[1]), 1)

        elif instruction[0] == "end": 
            break


def main():  # 主函数
    # 选择策略
    if dict['STRATEGY'] == 'FCFS':
        FCFS()
    elif dict['STRATEGY'] == 'SSTF':
        SSTF()
    else:
        SCAN()
    
    print("end")  # 程序结束时输出end
    quit()  # 退出程序


main()  # 执行主函数
