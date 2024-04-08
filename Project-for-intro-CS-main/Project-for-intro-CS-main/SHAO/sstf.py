def build():  # 读取dict.dic，构建字典
    fhand = open("dict.dic", "r")  # 文件地址自行更改
    DICT = {'TOTAL_STATION': 5, 'STRATEGY': 'FCFS', 'DISTANCE': 2}  # 初始化字典，设置默认值
    for line in fhand:  # 读取文件，更新字典
        if(line[0] == '#'):
            continue
        line = line.split("=")
        if(line[1].strip().isdigit()):  # 如果是数字，则转换为int
            DICT[line[0].strip()] = int(line[1].strip())
        else:
            DICT[line[0].strip()] = line[1].strip()
    fhand.close()
    return DICT  # 返回DICT

global dict
dict=build()
# def get_instructions():
#     instructions = []  # 初始化指令列表
#     for line in iter(input, ''):  # 读取每一行指令，以空行结束
#         instructions.append(line.rstrip())
#     return instructions


class Bus(object):
    def __init__(self):
        self.target = [0]*dict['TOTAL_STATION']
        self.clockwise = [0] * dict['TOTAL_STATION']
        self.counterclockwise = [0] * dict['TOTAL_STATION']
        self.direction = 0
        self.tar = 0
        self.hang = []

    def If_move(self):  # 如果还有指令就return True，没指令就Return False
        for i in range(len(bus.clockwise)):
            if bus.clockwise[i] != 0 or bus.counterclockwise[i] != 0 or bus.target[i] != 0:
                return True
        else:
            return False

    def update_target(self, address):
        self.target[address-1] = 1
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


class Station(object):  # 结点
    def __init__(self, position):
        self.position = position
        self.next = None
        self.prev = None


class Roundlink(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def append(self, item):  # 在尾部增加一个结点，并与上一个结点双向连接，没有结点则创建结点，头结点设置的不是空结点，
        """尾部添加元素"""
        node = Station(item)
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

    def travel(self):  # 遍历链表输出，在创建完先遍历一遍，在round之前用
        cur = self._head
        while cur != None:
            print(cur.position, end='     ')
            # if (cur.mark != -1):
            #     print(cur.mark)
            cur = cur.next


def create(a, b):  # 创建链表
    for i in range(a*b):
        Stations.append(i)


def SSTF():  # 最短寻道策略
    global Stations
    global bus
    global station  # station是游标
    global dict
    global total_distance
    global instructions
    global cnt
    global _TIME
    global hang
    hang = 0
    _TIME = 0
    cnt = 0
    Stations = Roundlink()  # Stations 是链表
    bus = Bus()
    create(dict['TOTAL_STATION'], dict['DISTANCE'])
    # Stations.travel()
    Stations.round()
    station = Stations._head
    total_distance = (dict['TOTAL_STATION'])*(dict['DISTANCE'])

    def Move_func():  # 根据bus的状态移动一次
        global station
        global dict
        global bus
        global cnt
        global hang
        if (bus.tar-1)*dict['DISTANCE'] == station.position:
            bus.remove_target(bus.tar-1)
            bus.tar = 0
            bus.direction = 0
            cnt = 1
            return
        if bus.direction == -1:
            if hang == 1:
                hang = 0
            elif station.position % dict['DISTANCE'] == 0:  # 顺便服务
                i = station.position//dict['DISTANCE']
                if bus.counterclockwise[i] == 1 or bus.target[i] == 1:
                    bus.counterclockwise[i] = 0
                    bus.target[i] = 0
                    hang = 1
                    return 0
            station = station.prev
        elif bus.direction == 1:
            if hang == 1:
                hang = 0
            elif station.position % dict['DISTANCE'] == 0:
                i = station.position//dict['DISTANCE']
                if bus.clockwise[i] == 1 or bus.target[i] == 1:
                    bus.clockwise[i] = 0
                    bus.target[i] = 0
                    hang = 1
                    return 0
            station = station.next

    # def get_instruct():
    #     orders = []
    #     f = open("C:\\Users\\15695\\Desktop\\SSTF\\SSTF\\5x3\\05-in.txt", 'r')
    #     for line in f:
    #         line = line.rstrip()
    #         orders.append(line)
    #     return orders
    def get_instruct():
        import sys
        instructions = []  # 初始化指令列表
        while 1:  # 读取每一行指令，以空行结束
            line = sys.stdin.readline()
            line = line.strip('\n')
            instructions.append(line.rstrip())
            if line == "end":
                break
        return instructions

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
        print('BUS:')
        print('position:'+str(station.position))
        print("target:"+"".join(map(str, bus.target)))
        print('STATION:')
        print("clockwise:"+"".join(map(str, bus.clockwise)))
        print("counterclockwise:"+"".join(map(str, bus.counterclockwise)))

    def _Direction():  # 每次clock输出前判断方向并作出一次移动（顺，逆，或不动）
        # sourcery skip: extract-method, move-assign
        global bus
        global station
        global dict
        global cnt
        global holdup
        if not bus.If_move():
            return
        if bus.tar == 0:  # bus.tar==0?
            _min = 100
            target_station_wise = 0
            target_station_counter = 0
            for i in range(len(bus.clockwise)):  # 用来判断哪个站最近
                if bus.clockwise[i] == 1 or bus.counterclockwise[i] == 1 or bus.target[i] == 1:
                    if i in bus.hang:
                        continue
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
        if bus.direction != 0 and station.position % dict['DISTANCE'] == 0:
            now_state = station.position // dict['DISTANCE']
            if bus.direction == 1:
                if bus.clockwise[now_state] == 0 and bus.target[now_state] == 0:
                    hang = 1  # hang等于1顺便服务不能进行
            elif bus.direction == -1:
                if bus.counterclockwise[now_state] == 0 and bus.target[now_state] == 0:
                    hang = 1
        if 'end' in order:
            return 0
        if 'counterclockwise' in order:
            a = eval(order[-1])
            if cnt == 1:
                if bus.clockwise[a-1] == 0 or bus.counterclockwise[a-1] == 0 or bus.target[a-1] == 0:
                    bus.hang.append(a-1)
            bus.counterclockwise[a-1] = 1
        elif 'target' in order:  # 对顺便服务加一状态变量，关则不考虑新加指令，开则考虑。不算到挂起指令中
            a = eval(order[-1])  # 挂起指令只涉及到参评不参评
            if cnt == 1:
                if bus.clockwise[a-1] == 0 or bus.counterclockwise[a-1] == 0 or bus.target[a-1] == 0:
                    bus.hang.append(a-1)
            bus.target[a-1] = 1
        elif 'clockwise' in order:
            a = eval(order[-1])
            if cnt == 1:
                if bus.clockwise[a-1] == 0 or bus.counterclockwise[a-1] == 0 or bus.target[a-1] == 0:
                    bus.hang.append(a-1)
            bus.clockwise[a-1] = 1
        elif 'clock' in order:
            _TIME += 1
            _Direction()
            print_sstf()
            cnt = 0
            bus.hang = []


def FCFS():
    pass


def SCAN():
    pass


def main():  # 主函数
    # 选择策略
    if dict['STRATEGY'] == 'FCFS':
        FCFS()
    elif dict['STRATEGY'] == 'SSTF':
        SSTF()
    else:
        SCAN()
     
    print("end\n")  # 程序结束时输出end
    quit()  # 退出程序
 

main()  # 执行主函数
