def SCAN():  # 顺便服务策略
    # 构建输出函数
    def print_result(bus, station, time):  #  传入三个参数，一个是bus，一个是station，一个是时间
        print("TIME:",time)
        print("BUS:")
        print("position:"+str(bus.position))
        print("target:"+"".join(map(str, bus.target)))
        print("STATION:")
        print("clockwise:"+"".join(map(str, station.clockwise)))
        print("counterclockwise:"+"".join(map(str, station.counterclockwise))) #删掉换行符，符合文档要求
    
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
        if(instructions[t] == 'clock'): # 读取完第一次运行的请求
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
            dis ,direct= distance(bus, move_instructions[first_move][1])
            if dis < mindistance:
                mindistance = dis
                request = move_instructions[first_move][0]
                address = move_instructions[first_move][1]
                final_direction = direct
        return  request, address, final_direction
    
    def isdone(current_instruction):  # 判断当前指令是否完成
        if bus.position == (current_instruction[1] - 1) * dict['DISTANCE'] and current_instruction[3] == 1:
            return True
        else:
            return False

    def direction_distance(bus, station, direction, instruction):
        if instruction == "target":
            if(direction == 1):
                max = [0, 0]
                min = [0, dict["DISTANCE"]* dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if bus.target[i] == 0:
                        continue
                    else:
                        difference = i*dict['DISTANCE'] - bus.position
                        if difference < 0:
                            difference = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0],max[1]), (min[0],min[1])
            elif(direction == -1):
                max = [0, 0]
                min = [0, dict["DISTANCE"]* dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if bus.target[i] == 0:
                        continue
                    else:
                        difference = bus.position - i*dict['DISTANCE']
                        if difference < 0:
                            difference = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0],max[1]), (min[0],min[1])
        elif instruction == "clockwise":
            if(direction == 1):
                max = [0, 0]
                min = [0, dict["DISTANCE"]* dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.clockwise[i] == 0:
                        continue
                    else:
                        difference = i*dict['DISTANCE'] - bus.position
                        if difference < 0:
                            difference = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0],max[1]), (min[0],min[1])
            elif(direction == -1):
                max = [0, 0]
                min = [0, dict["DISTANCE"]* dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.clockwise[i] == 0:
                        continue
                    else:
                        difference = bus.position - i*dict['DISTANCE']
                        if difference < 0:
                            difference = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0],max[1]), (min[0],min[1])
        elif instruction == "counterclockwise":
            if(direction == 1):
                max = [0, 0]
                min = [0, dict["DISTANCE"]* dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.counterclockwise[i] == 0:
                        continue
                    else:
                        difference = i*dict['DISTANCE'] - bus.position
                        if difference < 0:
                            difference = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0],max[1]), (min[0],min[1])
            elif(direction == -1):
                max = [0, 0]
                min = [0, dict["DISTANCE"]* dict['TOTAL_STATION']]
                for i in range(dict['TOTAL_STATION']):
                    if station.counterclockwise[i] == 0:
                        continue
                    else:
                        difference = bus.position - i*dict['DISTANCE']
                        if difference < 0:
                            difference = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
                        if difference < min[1]:
                            min[1] = difference
                            min[0] = i+1
                        if difference > max[1]:
                            max[1] = difference
                            max[0] = i+1
                return (max[0],max[1]), (min[0],min[1])

    def determine_move(bus, station, current_instruction):
        if current_instruction[2] == 1:
            target_max, target_min = direction_distance(bus, station, 1, "target")
            clockwise_max, clockwise_min = direction_distance(bus, station, 1, "clockwise")
            counterclockwise_max, counterclockwise_min = direction_distance(bus, station, 1, "counterclockwise")
            if min(target_min[1], clockwise_min[1], counterclockwise_min[1]) * 2 > dict['DISTANCE']* dict['TOTAL_STATION']:
                target_max, target_min = direction_distance(bus, station, -1, "target")
                clockwise_max, clockwise_min = direction_distance(bus, station, -1, "clockwise")
                counterclockwise_max, counterclockwise_min = direction_distance(bus, station, -1, "counterclockwise")
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x:x[1])
                return -1, (max_list[2][2], max_list[2][0])

            else:
                #把target_max, clockwise_max, counterclockwise_max 三个元组按照第二个元素排序
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x:x[1])
                return 1, (max_list[2][2], max_list[2][0])
        elif current_instruction[2] == -1:
            target_max, target_min = direction_distance(bus, station, -1, "target")
            clockwise_max, clockwise_min = direction_distance(bus, station, -1, "clockwise")
            counterclockwise_max, counterclockwise_min = direction_distance(bus, station, -1, "counterclockwise")
            if min(target_min[1], clockwise_min[1], counterclockwise_min[1]) * 2 > dict['DISTANCE']* dict['TOTAL_STATION']:
                target_max, target_min = direction_distance(bus, station, 1, "target")
                clockwise_max, clockwise_min = direction_distance(bus, station, 1, "clockwise")
                counterclockwise_max, counterclockwise_min = direction_distance(bus, station, 1, "counterclockwise")
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x:x[1])
                return 1, (max_list[2][2], max_list[2][0])

            else:
                max_list = [(target_max[0], target_max[1], "target"), (clockwise_max[0], clockwise_max[1], "clockwise"), (counterclockwise_max[0], counterclockwise_max[1], "counterclockwise")]
                max_list.sort(key=lambda x:x[1])
                return -1, (max_list[2][2], max_list[2][0])

    sign = 0
    passingly_sign = 0

    for instruction in instructions:
        instruction = instruction.split(" ")

        if instruction[0] == 'clock':
            time += 1  # 每读到clock计时
            if(sign != 0 and current_instruction[0] == ""):  # 如果sign不为0的时候获得first_move_instruction
                first_move_request , first_move_address, first_move_direction= slect_move(move_instructions, bus)
                current_instruction = (first_move_request, first_move_address, first_move_direction, 1)
                bus.change_direction(first_move_direction)

            if passingly_sign == 1:
                bus.change_direction(0)
                address = int(bus.position / dict['DISTANCE']+ 1)
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
                bus.position = bus.position - dict['DISTANCE'] * dict['TOTAL_STATION']  #如果position大于总长度，则做减法
            if current_instruction[3] == 0:#当前指令完成
                #根据当前指令的状态更新station的clockwise和counterclockwise或者更新bus的target
                address = int(bus.position / dict['DISTANCE']+ 1)
                if bus.target[address - 1] == 1:
                    bus.update_target(address, 0)
                if station.clockwise[address - 1] == 1:
                    station.update_clockwise(address, 0)
                if station.counterclockwise[address - 1] == 1:
                    station.update_counterclockwise(address, 0)
                
                #检查方向是否发生变化, 最长（目标），最短（方向）
                if(current_instruction[0] != ""):
                    direction , destination = determine_move(bus, station, current_instruction)
                    bus.change_direction(direction)
                    current_instruction = (destination[0], destination[1], direction, 1)
            else:#当前指令未完成
                if isdone(current_instruction):#判断当前指令是否完成
                    current_instruction = (current_instruction[0], current_instruction[1], current_instruction[2], 0)
                    bus.change_direction(0)
                #判断是否能顺便服务
                if(bus.position % dict['DISTANCE'] == 0 and bus.position != (current_instruction[1] - 1)*dict['DISTANCE']):
                    passingly_sign = passingly_service(bus, station)
            
            print_result(bus, station, time)
        elif instruction[0] == "target":  #如果是target指令
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