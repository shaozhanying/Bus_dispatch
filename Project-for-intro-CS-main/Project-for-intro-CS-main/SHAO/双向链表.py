lst = [
    "TOTAL_STATION",
    "STRATEGY",
    "DISTANCE",
    "end",
    "clock",
    "counterclockwise",
    "clockwise",
    "target",
]


class Bus(object):
    native_space = "Bus:"

    def __init__(self, item):
        self.tar = "0000000000"
        self.wise = "0000000000"
        self.counterclockwise = "0000000000"


class Station(object):
    def __init__(self, position):
        self.position = f"position:{str(position)}"
        self.sta = "STATION:"
        self.next = None
        self.prev = None
        self.mark = -1


class Roundlink(object):
    def __init__(self):
        self._head = None

    def is_empty(self):
        return self._head is None

    def append(self, item):
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

    def round(self):
        cur = self._head
        while cur.next is not None:
            cur = cur.next
        cur.next = self._head
        self._head.prev = cur

    def travel(self):
        cur = self._head
        while cur != None:
            print(cur.position, end="     ")
            if cur.mark != -1:
                print(cur.mark)
            cur = cur.next

    def Mark(self, i, cnt):
        cur = self._head
        for _ in range(i):  # 找到那个结点
            cur = cur.next
        cur.mark = (i + 1) // cnt


global run
run = Roundlink()


def create(a, b):
    for i in range(a * b):
        run.append(i)
        if (i + 1) % b == 0:
            run.Mark(i, b)


with open("C:\\Users\\15695\\Desktop\\新建 文本文档 (2).txt", "rt") as f:
    lst2 = [f.readline() for _ in range(3)]
    if lst[0] in lst2[0] or lst[0] in lst2[1] or lst[0] in lst[2]:
        print(1)
    else:
        create(5, 2)
    run.travel()
