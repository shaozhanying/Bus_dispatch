def FCFS():#先来先服务策略
    def print_result(bus, station, time):  #  传入三个参数，一个是bus，一个是station，一个是时间
        print("TIME:",time)
        print("BUS:")
        print("position:"+str(bus.position))
        print("target:"+"".join(map(str, bus.target)))
        print("STATION:")
        print("clockwise:"+"".join(map(str, station.clockwise)))
        print("counterclockwise:"+"".join(map(str, station.counterclockwise))) #删掉换行符，符合文档要求
    
    bus = BUS()#初始化bus
    station = STATION(0)#初始化station
    instructions = get_instructions()#读取指令
    global time#引用全局变量time
    print_result(bus, station, time)#输出初始状态
    time += 1
    global move_instructions
    global counter #move_instruction计数器
    counter = 0
    move_instructions =[]
    for instruction in instructions:
        if instruction == 'clock' or instruction == 'end':
            continue
        instruction = instruction.split(" ")
        move_instructions.append((instruction[0], int(instruction[1])))
    global current_instruction
    current_instruction = ("", 0, 0)


    def isdone(current_instruction):#判断当前指令是否完成
        if bus.position == (current_instruction[1] - 1) * dict['DISTANCE'] and current_instruction[2] == 1:
            return True
        else:
            return False
    
    def select_direction(bus,address):
        judge_direction = {"clockwise":0,"counterclockwise":0}
        difference = (address -1)*dict['DISTANCE'] - bus.position
        if difference > 0:
            judge_direction["clockwise"] = difference
            judge_direction["counterclockwise"] = dict['DISTANCE']* dict['TOTAL_STATION'] - difference
        elif difference < 0:
            judge_direction["counterclockwise"] = -difference
            judge_direction["clockwise"] = dict['DISTANCE']* dict['TOTAL_STATION'] + difference
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

        if instruction[0] == "clock":#如果是clock指令
            bus.position = bus.position + bus.direction
            if bus.position < 0:
                bus.position = dict['DISTANCE'] * dict['TOTAL_STATION'] + bus.position
            if bus.position >= dict['DISTANCE'] * dict['TOTAL_STATION']:
                bus.position = bus.position - dict['DISTANCE'] * dict['TOTAL_STATION']  #如果position大于总长度，则做减法
            if current_instruction[2] == 0:#当前指令完成
                #根据当前指令的状态更新station的clockwise和counterclockwise或者更新bus的target
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
            
            else:#当前指令未完成
                if isdone(current_instruction):#判断当前指令是否完成
                    current_instruction = (current_instruction[0], current_instruction[1], 0)
                    bus.change_direction(0)

            print_result(bus, station, time)
            time = time + 1
        elif instruction[0] == "target":#如果是target指令
            bus.update_target(int(instruction[1]), 1)
        
        elif instruction[0] == "clockwise":
            station.update_clockwise(int(instruction[1]), 1)

        elif instruction[0] == "counterclockwise":
            station.update_counterclockwise(int(instruction[1]), 1)

        elif instruction[0] == "end": 
            break