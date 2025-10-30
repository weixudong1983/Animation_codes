from manim import *

from datatype.StackVision import Stack
from datatype.linkStack import LinkedStack
from datatype.arrayStack import ArrayStack
from lib.code import CodeHighlight

class Stack_Title(Scene):
    def construct(self):
        title = Text("堆栈 Stack").to_edge(UP).scale(1.3).shift(DOWN*0.3).set_color(GREEN)
        subTitle = Text("先进后出（LIFO）").next_to(title,DOWN, buff=0.1).scale(0.7).set_color(GREEN)
        self.play(Write(title))
        self.play(Write(subTitle))
        self.wait(0.4)

        description = (
            "主要内容:\n"
            "\t堆栈的定义与核心特性\n"
            "\t入栈（push）与出栈（pop）操作\n"
            "\t顺序栈与链式栈的对比"
        )
        problem_text = Text(description,line_spacing=2).scale(0.65).next_to(subTitle, DOWN, buff=0.5)
        self.play(Write(problem_text), run_time=3)

        self.wait(1.8)


class Stace_Demo_1(Scene):
    def construct(self):
        stack = Stack().shift(UP ).shift(LEFT*2)
        self.play(Create(stack))

        self.wait(0.8)

        stack.push(self, 4)
        stack.push(self, 5)
        stack.pop(self)
        stack.pop(self)
        stack.push(self, 1)
        stack.push(self, 2)
        stack.push(self, 3)
        stack.push(self, 4)
        stack.push(self, 5)
        stack.push(self, 6)
        stack.push(self, 7)
        self.wait(1)

        stack.pop(self)
        stack.pop(self)
        stack.pop(self)


        array = ArrayStack(capacity=6, box_size=0.9)
        array.to_edge(UP, buff=1).shift(RIGHT*2)
        self.add(array)
        array.set_data([1,2,3,4],self )
        #self.wait(1)

        

        # 创建堆栈实例
        stack = LinkedStack(self, start_x=-4)
        stack.to_edge( UP, buff=1).scale(0.7)
        stack.shift(RIGHT*2).shift(DOWN*2)
        self.add(stack)

        # 构建初始堆栈（如果有初始数据）
        initial_labels = [ "1", "2", "3","4"]  # 初始元素，从左到右，左边是栈顶
        stack.build(initial_labels)

        #self.wait(1)

        # Push 操作：入栈新元素
        #stack.push("C")
        self.wait(1)





class Stace_Demo(Scene):
    def construct(self):
        # stack = Stack().shift(UP * 0.18)

        # self.play(Create(stack))
         # 创建堆栈实例
        stack = ArrayStack(self, start_x=-4)

        # 构建初始堆栈（如果有初始数据）
        initial_labels = ["A", "B"]  # 初始元素，从左到右，左边是栈顶
        stack.build(initial_labels)

        self.wait(1)

        # Push 操作：入栈新元素
        stack.push("C")
        self.wait(1)

        stack.push("D")
        self.wait(1)

        # Pop 操作：出栈
        stack.pop()
        self.wait(1)

        stack.pop()
        self.wait(1)

        stack.pop()  # 栈空时无操作
        self.wait(1)

        # 再次 push
        stack.push("E")
        self.wait(2)
        return

        # 下方循环队列
        circular = ArrayStack(capacity=6, box_size=0.9)
        circular.to_edge(UP, buff=1)
        self.add(circular)
        self.wait(1)

        circular.push(12, self)
        circular.push(1, self)
        circular.push(2, self)
        circular.push(3, self)
        circular.pop(self)
        circular.push(0, self)
        circular.push(4, self)
        circular.push(5, self)
        circular.push(6, self)

        self.wait(2)

