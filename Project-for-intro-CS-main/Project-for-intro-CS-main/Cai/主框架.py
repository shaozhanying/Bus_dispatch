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
        self.hang=[]

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


def FCFS():  # 先来先服务策略
    bus = BUS()  # 初始化bus
    station = STATION()  # 初始化station
    instructions = get_instructions()  # 读取指令
    global time#引用全局变量time
    print_result(bus, station, time)#输出初始状态
    time += 1



def SSTF():  # 最短寻道策略
    bus = BUS()  # 初始化bus
    station = STATION()  # 初始化station
    instructions = get_instructions()  # 读取指令
    global time#引用全局变量time
    print_result(bus, station, time)#输出初始状态
    time += 1


def SCAN():  # 顺便服务策略
    bus = BUS()  # 初始化bus
    station = STATION()  # 初始化station
    instructions = get_instructions()  # 读取指令
    global time#引用全局变量time
    print_result(bus, station, time)#输出初始状态
    time += 1


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
