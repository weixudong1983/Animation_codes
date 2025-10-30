from manim import *

from datatype.StackVision import Stack
from datatype.linkStack import LinkedStack
from datatype.arrayStack import ArrayStack
from lib.InstructionPanel import InstructionPanel
from lib.code import CodeHighlight

class Stack_1_Title(Scene):
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


class Stack_2_Demo_1(Scene):
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

        self.play(stack.animate.shift(LEFT*2))


        array = ArrayStack(self, capacity=6, box_size=0.9)
        array.to_edge(UP, buff=1).shift(RIGHT*2)
        self.add(array)
        array.push(1)
        array.push(2)
        array.push(3)
        array.push(4)
    
        self.wait(2)

        linked = LinkedStack(self, start_x=-0.7,scale=0.7,start_y=-0.5)
        initial_labels = [ "4","3", "2", "1",]  # 初始元素，从左到右，左边是栈顶
        linked.build(initial_labels)
        self.wait(2)

        
# class Stack_3_Demo_1_EndLinked(Scene):
#     def construct(self):
#         # 创建堆栈实例
#         stack = LinkedStack(self, start_x=-4)
        
#               # 定位堆栈：相对于 title 的下方
#         #stack.next_to(array, DOWN, buff=1).scale(0.8).shift(RIGHT * 1)
#         #stack.to_edge( UP, buff=1).scale(0.7)
#         #stack.shift(RIGHT*5).shift(DOWN*2)
#         #self.add(stack)

#         # 构建初始堆栈（如果有初始数据）
#         initial_labels = [ "1", "2", "3","4"]  # 初始元素，从左到右，左边是栈顶
#         stack.build(initial_labels)

#         #self.wait(1)

#         # Push 操作：入栈新元素
#         #stack.push("C")
#         self.wait(1)

class Stack_4_Code_Array_1(Scene):
    def construct(self):
        # C++代码内容
        code = '''class Stack {
private:
    int* data;      // 数组存储栈元素
    int top;        // 栈顶指针，-1表示栈空
    int capacity;   // 栈容量
public:
    // 构造函数，初始化栈
    Stack(int size=6) {
        capacity = size;
        data = new int[capacity];  // 动态分配数组
        top = -1;                  // 初始栈空
    }
    // 析构函数，释放内存
    ~Stack() {
        delete[] data;
    }'''
        cl = CodeHighlight(code_string=code,scale_factor=0.9,shift_top=0.5)
        cl.add_to_scene(self)
        cl.highlight(2,5)
        self.wait(1)
        cl.highlight(7,12)
class Stack_4_Code_Array_1_0(Scene):
    def construct(self):
        # C++代码内容
        code = ''' // 判断栈是否为空
    bool isEmpty() {
        return top == -1;
    }
    // 判断栈是否满
    bool isFull() {
        return top == capacity - 1;
    }'''
        cl = CodeHighlight(code_string=code,scale_factor=1,shift_top=0.5)
        cl.add_to_scene(self)
        cl.highlight(1,4)
        self.wait(1)
        cl.highlight(5,8)
class Stack_4_Code_Array_2(Scene):
    def construct(self):
        # C++代码内容
        code = ''' // 入栈操作
    bool push(int value) {
        if (isFull()) {
            std::cout << "栈满，无法入栈！" << std::endl;
            return false;
        }
        data[++top] = value;  // top先加1，再赋值
        return true;
    }
    // 出栈操作
    bool pop() {
        if (isEmpty()) {
            std::cout << "栈空，无法出栈！" << std::endl;
            return false;
        }
        top--;  // 直接top减1，出栈元素不再访问
        return true;
    }'''
        cl = CodeHighlight(code_string=code,scale_factor=0.8,shift_top=0.5)
        cl.add_to_scene(self)
        cl.highlight(1,9)
        self.wait(1)
        cl.highlight(10,18)
        self.wait(1)


class Stack_4_Code_Array_3(Scene):
    def construct(self):
        # C++代码内容
        code = '''    // 获取栈顶元素（不出栈）
    int peek() {
        if (isEmpty()) {
            std::cout << "栈空，无栈顶元素！" << std::endl;
            return -1;  // 返回-1表示错误
        }
        return data[top];
    }
   '''
        cl = CodeHighlight(code_string=code,scale_factor=0.8,shift_top=0.5)
        cl.add_to_scene(self)
        cl.highlight(1,9)
        self.wait(1)


class Stack_5_Code_Array_Instruction(Scene):
    def construct(self):
        instructions_list = [
            "Stack stack(5);",
            "stack.push(10);",
            "stack.push(20);",
            "stack.push(30);",
            "stack.peek();",
            "stack.pop();",
            "stack.pop();",
        ]
        # 使用 InstructionPanel 管理指令列表与高亮框，便于复用
        panel = InstructionPanel(
            instructions_list,
            t2c={"push": RED, "pop": RED,  "peek": RED, "Stack": YELLOW,
                 "5": BLUE, "10": BLUE, "20": BLUE, "30": BLUE},
            start_index=0,
        )
        panel.add_to_scene(self)

        stack = Stack().shift(UP*1.5 ).shift(LEFT*1.5)
        self.play(Create(stack))

        array = ArrayStack(self)
        array.shift(RIGHT*3)

        for instr in instructions_list[1:]:
            panel.next(self)  # 高亮下一行指令

            if "push" in instr:
                try:
                    value = int(instr.split("(")[1].split(")")[0])
                except Exception:
                    value = None
                if value is not None:
                    stack.push(self,value)
                    array.push(value)
            elif "pop" in instr:
                stack.pop(self)
                array.pop()
       
        self.wait(1)


class Stack_6_Linked_Demo_1(Scene):
    def construct(self):

        linked = LinkedStack(self, start_x=-2)
        # 构建初始堆栈（如果有初始数据）
        initial_labels = [ "2","1" ]  # 初始元素，从左到右，左边是栈顶
        linked.build(initial_labels)

        stack = Stack().shift(UP*1 ).shift(LEFT*4)
        self.play(Create(stack))
        
              # 定位堆栈：相对于 title 的下方
        #stack.next_to(array, DOWN, buff=1).scale(0.8).shift(RIGHT * 1)
        #stack.to_edge( UP, buff=1).scale(0.7)
        #stack.shift(RIGHT*5).shift(DOWN*2)
        #self.add(stack)

        stack.push(self, 1,time=0)
        stack.push(self, 2,time=0)

        self.wait(1)

        stack.pop(self)
        linked.pop()

        stack.push(self, 3)
        linked.push( "3")
        


class Stace_Demo(Scene):
    def construct(self):

        stack = LinkedStack(self, start_x=-4,scale_factor=0.2,shift_right=2,shift_down=2)
        
              # 定位堆栈：相对于 title 的下方
        #stack.next_to(array, DOWN, buff=1).scale(0.8).shift(RIGHT * 1)
        #stack.to_edge( UP, buff=1).scale(0.7)
        #stack.shift(RIGHT*5).shift(DOWN*2)
        #self.add(stack)

        # 构建初始堆栈（如果有初始数据）
        initial_labels = [ "1", "2", "3","4"]  # 初始元素，从左到右，左边是栈顶
        stack.build(initial_labels)

        stack = Stack().shift(UP*1.5 ).shift(LEFT*1.5)
        self.play(Create(stack))
        stack.push(self, 1,time=0)
        stack.push(self, 2,time=0)
        stack.push(self, 3,time=0)
        stack.push(self, 4,time=0)



        # stack = Stack().shift(UP * 0.18)

        # self.play(Create(stack))
            # 构建初始堆栈（如果有初始数据）
        # initial_labels = ["A", "B"]  # 初始元素，从左到右，左边是栈顶
        #  # 创建堆栈实例
        # stack = ArrayStack(self, initial_data=initial_labels,capacity=6, box_size=0.9)

    
        # #stack.set_data(initial_labels)

        # self.wait(1)

        # # Push 操作：入栈新元素
        # stack.push("C")
        # self.wait(1)

        # stack.push("D")
        # self.wait(1)

        # # Pop 操作：出栈
        # stack.pop()
        # self.wait(1)

        # stack.pop()
        # self.wait(1)

        # stack.pop()  # 栈空时无操作
        # self.wait(1)

        # # 再次 push
        # stack.push("E")
        # self.wait(2)
        # return

        # # 下方循环队列
        # circular = ArrayStack(capacity=6, box_size=0.9)
        # circular.to_edge(UP, buff=1)
        # self.add(circular)
        # self.wait(1)

        # circular.push(12, self)
        # circular.push(1, self)
        # circular.push(2, self)
        # circular.push(3, self)
        # circular.pop(self)
        # circular.push(0, self)
        # circular.push(4, self)
        # circular.push(5, self)
        # circular.push(6, self)

        # self.wait(2)

