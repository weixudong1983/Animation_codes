from manim import *

from lib import InstructionPanel
from lib.code import CodeHighlight
from lib.fakeScene import FakeScene



class QueueNode(VGroup):
    def __init__(self, value, slot_size=1.0, fill_color="#fc7e6b", text_color=BLACK, **kwargs):
        super().__init__(**kwargs)
        box = Rectangle(
            width=slot_size * 0.8, height=slot_size * 0.8,
            fill_color=fill_color, fill_opacity=1.0,
            stroke_color=WHITE, stroke_width=2
        )
        txt = Text(str(value), color=text_color, font_size=28)
        txt.move_to(box.get_center())
        self.add(box, txt)


class QueueVisual(VGroup):
    def __init__(self, queue_size=5, slot_size=1.1, center=ORIGIN,
                 bg_color="#1e2a2f", initial_values=None,
                 node_fill="#fc7e6b", node_text_color=BLACK, **kwargs):
        super().__init__(**kwargs)
        self.queue_size = queue_size
        self.slot_size = slot_size
        queue_w = slot_size * queue_size
        queue_h = slot_size * 1.1

        # 背景和白色边框
        self.bg = Rectangle(
            width=queue_w, height=queue_h,
            fill_opacity=1, fill_color=bg_color, stroke_width=0
        )
        self.border = Rectangle(
            width=queue_w, height=queue_h,
            color=WHITE, stroke_width=3, fill_opacity=0
        )

        # 各槽位中心
        y_offset = -slot_size * 0.2
        self.slot_centers = [
            np.array([-queue_w / 2 + slot_size / 2 + i * slot_size, y_offset, 0])
            for i in range(queue_size)
        ]

        # 标签
        self.front_label = Text("队首", color="#a1eaa1", font_size=28)
        self.back_label = Text("队尾", color="#fc7e6b", font_size=28)
        self.front_label.next_to(self.bg, UP + LEFT, buff=0.15)
        self.back_label.next_to(self.bg, UP + RIGHT, buff=0.15)

        # 节点组
        self.nodes = VGroup()

        # 组装
        self.add(self.bg, self.border, self.front_label, self.back_label, self.nodes)
        self.move_to(center)

        # 初始化节点
        if initial_values:
            vals = list(initial_values)
            m = len(vals)
            if m > self.queue_size:
                vals = vals[-self.queue_size:]
                m = self.queue_size
            for i, val in enumerate(vals):
                idx = self.queue_size - m + i
                node = QueueNode(val, self.slot_size,
                                 fill_color=node_fill, text_color=node_text_color)
                target = self.slot_centers[idx] + self.get_center()
                node.move_to(target)
                self.nodes.add(node)

    def enqueue(self, scene, value):
        """入队动画"""
        n = len(self.nodes)
        if n < self.queue_size:
            # 现有节点左移
            if n > 0:
                shifts = []
                for i, node in enumerate(self.nodes):
                    target = self.slot_centers[self.queue_size - n - 1 + i] + self.get_center()
                    shifts.append(node.animate.move_to(target))
                scene.play(*shifts, run_time=0.5)

            # 新节点右侧滑入
            new_node = QueueNode(value, self.slot_size)
            start_pos = self.slot_centers[-1] + RIGHT * 2.5 + self.get_center()
            new_node.move_to(start_pos)
            scene.add(new_node)
            scene.play(new_node.animate.move_to(self.slot_centers[-1] + self.get_center()), run_time=0.7)
            self.nodes.add(new_node)
        scene.wait(0.5)

    def dequeue(self, scene):
        """出队动画"""
        n = len(self.nodes)
        if n == 0:
            return
        node_out = self.nodes[0]
        out_target = self.slot_centers[self.queue_size - n] + LEFT * 2.5 + self.get_center()
        if n == 1:
            out_target = self.slot_centers[0] + LEFT * 2.5 + self.get_center()
        scene.play(node_out.animate.move_to(out_target), run_time=0.6)
        scene.play(FadeOut(node_out), run_time=0.6)
        self.nodes.remove(node_out)
        scene.wait(0.5)


# ---------- CircularQueueVisual: 下方循环队列（格子+索引下方、rear 环回） ----------
class CircularQueueVisual(VGroup):
    def __init__(self, capacity=6, box_size=0.9, gap=0.12, **kwargs):
        super().__init__(**kwargs)
        self.capacity = capacity
        self.box_size = box_size
        self.gap = gap
        self.front = 0
        self.rear = 0
        self.boxes = []
        self.value_texts = [None] * capacity
        self.index_labels = []
        # 创建一列 boxes 的 VGroup 再一次性 arrange（避免重复 add 导致索引重叠）
        boxes_group = VGroup()
        for i in range(capacity):
            box = Square(self.box_size, stroke_color=BLUE, stroke_width=3).set_fill("#f4d03f", opacity=0)
            boxes_group.add(box)
            self.boxes.append(box)
        boxes_group.arrange(RIGHT, buff=self.gap)
        # 添加到整体，并为每个 box 添加 index 标签（在下方）
        self.add(boxes_group)
        for i, box in enumerate(self.boxes):
            idx_label = Text(str(i), font_size=20)
            idx_label.next_to(box, DOWN, buff=0.25)
            self.index_labels.append(idx_label)
            self.add(idx_label)

        # F/B 指针
        self.front_label = Text("F", color=GREEN, font_size=36)
        self.back_label = Text("R", color=RED, font_size=36)
        self.update_pointer_positions()
        self.add(self.front_label, self.back_label)

    def update_pointer_positions(self):
        # 将 F/B 放到对应 box 的上方
        # 注意：如果 boxes 列有变换（移动），这里应再次调用
        self.front_label.next_to(self.boxes[self.front], UP, buff=0.25)
        self.back_label.next_to(self.boxes[self.rear], UP, buff=0.25)
        if(self.front == self.rear):
            self.back_label.next_to(self.boxes[self.rear], UP, buff=0.25).shift(RIGHT*0.2)
            self.front_label.next_to(self.boxes[self.front], UP, buff=0.25).shift(LEFT*0.2)

    def enqueue(self, value, scene: Scene):
        # 判满（rear+1 == front）时认为满
        next_rear = (self.rear + 1) % self.capacity
        if next_rear == self.front:
            # 队满（你可以在这里做提示动画）
            warn = Text("Queue full!", font_size=24, color=YELLOW).next_to(self, UP, buff=0.2)
            scene.play(FadeIn(warn), run_time=0.4)
            scene.wait(0.6)
            scene.play(FadeOut(warn), run_time=0.3)
            return

        # 在 self.rear 的格子中显示值（淡入）
        target = self.boxes[self.rear]
        # 如果已有旧文本（应该为 None），先移除
        if self.value_texts[self.rear] is not None:
            scene.play(FadeOut(self.value_texts[self.rear]), run_time=0.2)
        text = Text(str(value), font_size=28, color=BLACK).move_to(target.get_center())
        self.value_texts[self.rear] = text
        # 将格子填色并淡入文字
        target.set_fill("#f4d03f", opacity=1)
        scene.play(FadeIn(text), run_time=0.35)

        # 更新 rear 指针（环回）
        self.rear = next_rear
        # 更新指针位置
        #self.update_pointer_positions()
        scene.play(
            self.front_label.animate.next_to(self.boxes[self.front], UP, buff=0.25),
            self.back_label.animate.next_to(self.boxes[self.rear], UP, buff=0.25),
            run_time=0.25,
        )

    def dequeue(self, scene: Scene):
        # 判空
        if self.front == self.rear:
            warn = Text("Queue empty!", font_size=24, color=YELLOW).next_to(self, UP, buff=0.2)
            scene.play(FadeIn(warn), run_time=0.35)
            scene.wait(0.5)
            scene.play(FadeOut(warn), run_time=0.25)
            return

        # 在 front 位置淡出文字并清空填充
        if self.value_texts[self.front] is not None:
            scene.play(FadeOut(self.value_texts[self.front]), run_time=0.35)
            self.value_texts[self.front] = None
        # 清除格子填充
        self.boxes[self.front].set_fill("#f4d03f", opacity=0)

        # front 环移
        self.front = (self.front + 1) % self.capacity
        #self.update_pointer_positions()
        scene.play(
            self.front_label.animate.next_to(self.boxes[self.front], UP, buff=0.25),
            self.back_label.animate.next_to(self.boxes[self.rear], UP, buff=0.25),
            run_time=0.25,
        )

    def set_data(self, data_list):
        # 将指定数据写入循环队列（data_list 的长度 <= capacity -1）
        # 先清空
        for i in range(self.capacity):
            if self.value_texts[i] is not None:
                self.value_texts[i].become(Text(str(i), font_size=20))  # 替换为 index 文本占位
            self.boxes[i].set_fill("#f4d03f", opacity=0)
            self.value_texts[i] = None

        # 把 data_list 从 front 开始写（将 front 设为 0, rear 随数据量移动）
        self.front = 0
        self.rear = 0
        for v in data_list:
            self.enqueue(v, scene=FakeScene())  # 使用辅助场景仅改变内部状态（无动画）
        # 重新更新指针位置（enqueue 已更新）
        self.update_pointer_positions()



class Queue2_Title(Scene):
    def construct(self):
        title = Text("队列").to_edge(UP).scale(1.3).shift(DOWN*0.3).set_color(GREEN)
        subTitle = Text("循环队列").next_to(title,DOWN, buff=0.1).scale(0.7).set_color(GREEN)
        self.play(Write(title))
        self.play(Write(subTitle))
        self.wait(0.4)

        description = (
            "描述：\n"
            "\t什么是循环队列？和普通队列有啥区别？\n"
            "\t入队、出队，头尾指针如何循环？\n"
            "\t代码思路 & 图解，小白也能看懂！"
        )
        problem_text = Text(description,line_spacing=2).scale(0.65).next_to(subTitle, DOWN, buff=0.5)
        self.play(Write(problem_text), run_time=3)

        self.wait(1.8)
# ---------- InstructionPanel: 可复用的指令列表 + 高亮组件 ----------


# ---------- Demo Scene ----------
class Queue2_Demo(Scene):
    def construct(self):
        #self.camera.background_color = "#333333"

        # 上方线性队列（带底色条）
        qv = QueueVisual(initial_values=[], center=UP * 1.5).shift(UP)
        self.add(qv)

         # 下方循环队列
        circular = CircularQueueVisual(capacity=6, box_size=0.9)
        circular.next_to(qv,DOWN, buff=1)
        self.add(circular)

        # 入队
        self.wait(1)

        qv.enqueue(self, 9)
        circular.enqueue(9, self)

        qv.enqueue(self, 8)
        circular.enqueue(8, self)

        qv.enqueue(self, 7)
        circular.enqueue(7, self)

        qv.dequeue(self)
        circular.dequeue(self)

        qv.dequeue(self)
        circular.dequeue(self)


        qv.enqueue(self, 2)
        circular.enqueue(2, self)

        qv.enqueue(self, 5)
        circular.enqueue(5, self)


        qv.enqueue(self, 11)
        circular.enqueue(11, self)

        qv.enqueue(self, 13)
        circular.enqueue(13, self)



     
        self.wait(3.0)




    
class Queue2_CodeIsFullIsEmpty_1(Scene):
    def construct(self):
        # C++代码内容
        code = '''// 容量初始化为实际容量+1，用于区分队满和队空
class CircularQueue {
private:
    std::vector<int> data;
    int capacity;
    int front;
    int rear;
public:
    // 实际容量为 n，内部数组容量为 n+1
    CircularQueue(int n) 
    : data(n + 1), capacity(n + 1), front(0), rear(0) {}
    // 判满
    bool isFull() const { 
        return (rear + 1) % capacity == front; 
    }
    // 判空
    bool isEmpty() const { 
        return front == rear; 
    }
};'''
        cl = CodeHighlight(code_string=code,scale_factor=0.8)
        cl.add_to_scene(self)

        cl.highlight( 4, 7, color=YELLOW)
        # 框选isFull函数
        cl.highlight( 9, 11, color=YELLOW)
        # 框选isEmpty函数
        cl.highlight( 12, 15, color=YELLOW)
        cl.highlight( 16, 19, color=YELLOW)

        # 最终保持代码显示
        #cl.wait(1)

class Queue2_CodeEnDeQueue_2(Scene):
    def construct(self):
        # C++代码内容
        code = ''' // 入队，成功返回 true，队满返回 false
    bool enqueue(int value) {
        if (isFull()) return false;
        data[rear] = value;
        rear = (rear + 1) % capacity;
        return true;
    }
    // 出队，成功返回 true，队空返回 false
    bool dequeue() {
        if (isEmpty()) return false;
        front = (front + 1) % capacity;
        return true;
    }'''
        cl = CodeHighlight(code_string=code,scale_factor=0.9)
        cl.add_to_scene(self)

        cl.highlight( 1, 7, color=YELLOW)

        cl.highlight( 8, 13, color=YELLOW)


class Queue2_CodePrint_3(Scene):
    def construct(self):
        # C++代码内容
        code = '''// 打印队列中的有效元素
    void printQueue() const {
        std::cout << "Queue: ";
        int i = front;
        while (i != rear) {
            std::cout << data[i] << " ";
            i = (i + 1) % capacity;
        }
        std::cout << std::endl;
    }
    // 获取队头元素，假设队列非空
    int getFront() const {
        return data[front];
    }'''
        cl = CodeHighlight(code_string=code,scale_factor=0.9)
        cl.add_to_scene(self)

        cl.highlight( 1,10, color=YELLOW)

        cl.highlight( 11, 14, color=YELLOW)



class Queue2_End(Scene):
    highlight_box: SurroundingRectangle
    instructions: VGroup
    start_index: int = 0
    def construct(self):
        #self.camera.background_color = "#333333"

        # 上方线性队列（带底色条）
        qv = QueueVisual(initial_values=[], center=UP * 1.5)
        qv.shift(RIGHT*2).shift(UP*0.5)
        self.add(qv)

         # 下方循环队列
        circular = CircularQueueVisual(capacity=6, box_size=0.9)
        circular.next_to(qv,DOWN, buff=1)
        self.add(circular)

        instructions_list = [
            "CircularQueue q(5);",
            "q.enqueue(10)",
            "q.enqueue(20)",
            "q.enqueue(30)",
            "q.enqueue(40)",
            "q.enqueue(70)",
            "q.dequeue()",
            "q.dequeue()",
            "q.enqueue(40)"
        ]
        # 使用 InstructionPanel 管理指令列表与高亮框，便于复用
        panel = InstructionPanel(
            instructions_list,
            t2c={"dequeue": RED, "enqueue": RED, "CircularQueue": YELLOW,
                 "5": BLUE, "10": BLUE, "20": BLUE, "30": BLUE, "40": BLUE, "70": BLUE},
            start_index=0,
        )
        panel.add_to_scene(self)

        # 遍历指令并执行对应的队列操作，同时移动高亮
        for instr in instructions_list[1:]:
            panel.next(self)  # 高亮下一行指令
            if "enqueue" in instr:
                try:
                    value = int(instr.split("(")[1].split(")")[0])
                except Exception:
                    value = None
                if value is not None:
                    qv.enqueue(self, value)
                    circular.enqueue(value, self)
            elif "dequeue" in instr:
                qv.dequeue(self)
                circular.dequeue(self)

        return
        # 入队
        self.wait(1)

        qv.enqueue(self, 9)
        circular.enqueue(9, self)

        qv.enqueue(self, 8)
        circular.enqueue(8, self)

        qv.enqueue(self, 7)
        circular.enqueue(7, self)

        qv.dequeue(self)
        circular.dequeue(self)

        qv.dequeue(self)
        circular.dequeue(self)


        qv.enqueue(self, 2)
        circular.enqueue(2, self)

        qv.enqueue(self, 5)
        circular.enqueue(5, self)


        qv.enqueue(self, 11)
        circular.enqueue(11, self)

        qv.enqueue(self, 13)
        circular.enqueue(13, self)


        self.wait(3.0)
    def instructions_next(self):
        self.start_index += 1
        self.play(self.highlight_box.animate.move_to(self.instructions[self.start_index]), run_time=1)
        self.wait(0.5)  # 短暂暂停
    def add_instructions_and_highlight(self, instructions_list, t2c={},highlight_color=YELLOW, buff=0.1, start_index=0):
        self.start_index = start_index
        # 创建指令VGroup，垂直排列
        self.instructions = VGroup(*[Text(instr, font_size=28,font="sans-serif",t2c=t2c) for instr in instructions_list]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT, buff=1.5)  # 左侧，buff=1.5以避免与代码重叠
        self.instructions.shift(UP)
        self.add(self.instructions)

        # 初始高亮框
        self.highlight_box = SurroundingRectangle(self.instructions[start_index], color=highlight_color, buff=buff, corner_radius=0, stroke_width=2)
        self.add(self.highlight_box)
        
        # 返回highlight_box以便后续动画移动
        #return highlight_box, instructions