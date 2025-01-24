from manimlib import *
PURE_RED = "#FF0000"
PURE_RED = "#00FF00"
PURE_BLUE = "#0000FF"



class ReverseLinkedListLeetcode(Scene):

    def construct(self):

        self.camera.frame.scale(1.1)
        self.camera.frame.shift(RIGHT)

        a1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("1", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(a1).set_z_index(1).scale(1.37)
        a=VGroup(a1, text).scale(0.756).shift(LEFT*5.2)


        b1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("2", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(b1).set_z_index(1).scale(1.37)
        b=VGroup(b1, text).scale(0.756).shift(LEFT*3.5).next_to(a, RIGHT, buff=2.1)


        c1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("3", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(c1).set_z_index(1).scale(1.37)
        c=VGroup(c1, text).scale(0.756).shift(LEFT*3.5).next_to(b, RIGHT, buff=2.1)

        d1 = (
    RoundedRectangle(width=2.4, height=2.4, stroke_width=30, fill_opacity=1)
    .set_fill(GREEN, opacity=1)      # Fully opaque fill
    .set_stroke(GREEN, opacity=0.6)  # 70% opaque stroke
    .scale(0.77)
    
)

        text=Text("4", font=BOLD, stroke_width=3, font_size=80).set_color(BLACK).move_to(d1).set_z_index(1).scale(1.37)
        d=VGroup(d1, text).scale(0.756).shift(LEFT*3.5).next_to(c, RIGHT, buff=2.1)







        self.play(GrowFromCenter(a), GrowFromCenter(b), GrowFromCenter(c), GrowFromCenter(d),)
        self.wait(2)

        arrow = Arrow(a.get_right()+RIGHT*0.14, b.get_left()+LEFT*0.14, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow1 = Arrow(b.get_right()+RIGHT*0.14, c.get_left()+LEFT*0.14, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow2 = Arrow(c.get_right()+RIGHT*0.14, d.get_left()+LEFT*0.14, buff=0.1).set_color(GREY_D).set_stroke(width=8)
        arrow3 = arrow2.copy().shift(RIGHT*3.52)
        self.play(ShowCreation(arrow), ShowCreation(arrow1), ShowCreation(arrow2), ShowCreation(arrow3))

        self.wait(2)

        head = Text("head").set_color(BLACK).next_to(a, UP).shift(UP*0.42)
        self.play(GrowFromCenter(head))
        self.wait(2)
        tail = Text("tail").set_color(BLACK).next_to(d, UP).shift(UP*0.42)
        self.play(GrowFromCenter(tail))
        self.wait(2)



        self.play(self.camera.frame.animate.shift(RIGHT*15))

        source_code = r'''

        def reverseList(self, head):
            prev = None
            current = head
        
            while current:
                next_node = current.next 
                current.next = prev 
                prev = current  
                current = next_node
            
            return prev

        
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "while": BLUE_E,
            "reverseList": "#FF0000",
            "in": BLUE_E,
            "for": BLUE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "range":PURE_RED,
            "len":PURE_RED,
            "canCompleteCircuit":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "sum":PURE_RED,
            "True":BLUE_E,
            "False":BLUE_E,
            "del":BLUE_E
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(1.32).shift(RIGHT*15.8).scale(0.72)


        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        # Animate it onto the scene
        self.play(Write(code))
        self.wait(1)


        rect = SurroundingRectangle(code[:26], color=PURE_BLUE, stroke_width=5).scale(1.2)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[26:47], color=PURE_BLUE, stroke_width=5).scale(1.2)))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(LEFT*15))

        self.wait(2)

        self.play(FadeOut(head), FadeOut(tail))
        self.wait(2)

        prev = Text("prev").set_color(BLACK).next_to(head, UP)
        self.play(GrowFromCenter(prev))
        self.wait(2)
        current = Text("current").set_color(BLACK).next_to(a, DOWN, buff=0.7)
        self.play(GrowFromCenter(current))

        self.wait(2)

        self.play(self.camera.frame.animate.shift(RIGHT*15))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[47:60], color=PURE_BLUE, stroke_width=5).scale(1.1)))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[60:82], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[82:99], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[99:111], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[111:128], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[128:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(Uncreate(rect))
        self.wait(1)

        self.play(self.camera.frame.animate.shift(LEFT*15), FadeOut(code))

        self.play(self.camera.frame.animate.scale(1.2),
                  )
        self.play(VGroup(a,b,c,d,arrow1, arrow, arrow2, arrow3).animate.scale(1.17),
                  current.animate.next_to(a, DOWN, buff=0.7),
                  prev.animate.next_to(a, UP, buff=1.3).shift(RIGHT*1.8),
                  self.camera.frame.animate.shift(DOWN*1.34+DOWN*0.8),
                  current.animate.shift(LEFT+DOWN*0.12))



        self.wait()

        source_code = r'''

            while current:
                next_node = current.next 
                current.next = prev 
                prev = current  
                current = next_node


        
'''

        # Map each substring to a desired color
        color_map = {
            
            "class": BLUE_E,
            "def": BLUE_E,
            "if": BLUE_E,
            "elif": BLUE_E,
            "while": BLUE_E,
            "reverseList": "#FF0000",
            "in": BLUE_E,
            "for": BLUE_E,
            "self": PURPLE_E,
            "__init__":PURE_RED,
            "kruskal": PURE_RED,
            "find": PURE_RED,
            "append":PURE_RED,
            "sort":PURE_RED,
            "range":PURE_RED,
            "len":PURE_RED,
            "canCompleteCircuit":PURE_RED,
            "not":BLUE_E,
            "disjoint":BLACK,
            "chain":BLACK,
            "__str__":PURE_RED,
            "enumerate":PURE_RED,
            "return":BLUE_E,
            "index":BLACK,
            "HashTable":PURE_RED,
            "_hash":PURE_RED,
            "insert":PURE_RED,
            "None":BLUE_E,
            "get":PURE_RED,
            "remove":PURE_RED,
            "sum":PURE_RED,
            "True":BLUE_E,
            "False":BLUE_E,
            "del":BLUE_E
        }

        

        # Create a Code mobject with syntax highlighting
        code = Text(source_code).set_color(BLACK).scale(1.32).scale(0.66).next_to(c, DOWN, buff=0.7).shift(DOWN*2.2).scale(1.2)


        # Apply color for each key-value in the map
        for word, color in color_map.items():
            code.set_color_by_text(word, color)

        # Animate it onto the scene
        self.play(Write(code))
        self.wait(1)  

        rect = SurroundingRectangle(code[:13], color=PURE_BLUE, stroke_width=5).scale(1.1)
        self.play(ShowCreation(rect))

        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[13:35], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)
        next_node = Text("next_node").set_color(BLACK).next_to(b, DOWN, buff=0.7)
        self.play(ShowCreation(next_node))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(code[35:52], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)
        self.play(Transform(arrow, Arrow(a.get_right()+RIGHT*0.22, prev.get_bottom(), buff=0.1).set_color(GREY_D).set_stroke(width=8)))  
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[52:64], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)
        self.play(prev.animate.next_to(current, DOWN, buff=0.4))
        self.wait(1)
        self.play(Transform(arrow, Arrow(a.get_left()+LEFT*0.22, a.get_left()+LEFT*2.3, buff=0.1).set_color(GREY_D).set_stroke(width=8)),
                  self.camera.frame.animate.shift(LEFT*1.4))  
        self.wait(1)
        self.play(self.camera.frame.animate.shift(RIGHT*1.4))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(code[64:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)
        self.play(current.animate.next_to(next_node, DOWN, buff=0.18),
                  prev.animate.shift(UP*0.75))
        self.wait(2)

        self.play(Transform(rect,SurroundingRectangle(code[:13], color=PURE_BLUE, stroke_width=5).scale(1.1) ))
        self.wait(2)
        self.play(Transform(rect, SurroundingRectangle(code[13:35], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait(2)

        self.play(next_node.animate.next_to(c, DOWN, buff=0.7),
                  current.animate.next_to(b, DOWN, buff=0.76))
        
        self.wait(2)

        self.play(Transform(rect, SurroundingRectangle(code[35:52], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(Transform(arrow1, Arrow(b.get_left()+LEFT*0.22, a.get_right()+RIGHT*0.22, buff=0.1).set_color(GREY_D).set_stroke(width=8)))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[52:64], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(prev.animate.next_to(current, DOWN, buff=0.4))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[64:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(current.animate.next_to(next_node, DOWN, buff=0.18),
                  prev.animate.shift(UP*0.75))
        
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[:13], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[13:35], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()

        self.play(next_node.animate.next_to(d, DOWN, buff=0.7),
                  current.animate.next_to(c, DOWN, buff=0.76))
        
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(code[35:52], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(Transform(arrow2, Arrow(c.get_left()+LEFT*0.22, b.get_right()+RIGHT*0.22, buff=0.1).set_color(GREY_D).set_stroke(width=8)))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[52:64], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(prev.animate.next_to(current, DOWN, buff=0.4))
        self.wait()
        self.play(Transform(rect, SurroundingRectangle(code[64:], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()
        self.play(current.animate.next_to(next_node, DOWN, buff=0.18),
                  prev.animate.shift(UP*0.75))
        
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[:13], color=PURE_BLUE, stroke_width=5).scale(1.1))) 
        self.wait()

        self.play(Transform(rect, SurroundingRectangle(code[13:35], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        self.wait()

        self.play(next_node.animate.shift(RIGHT*4.5),
                  current.animate.next_to(d, DOWN, buff=0.76),
                  self.camera.frame.animate.shift(RIGHT*2.96))
                   
        
        
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[35:52], color=PURE_BLUE, stroke_width=5).scale(1.1)))
        
        self.play(Transform(arrow3, Arrow(d.get_left()+LEFT*0.22, c.get_right()+RIGHT*0.22, buff=0.1).set_color(GREY_D).set_stroke(width=8)))

        self.play(Transform(rect, SurroundingRectangle(code[52:64], color=PURE_BLUE, stroke_width=5).scale(1.1)))  

        self.play(prev.animate.next_to(current, DOWN, buff=0.4))

        self.play(Transform(rect, SurroundingRectangle(code[64:], color=PURE_BLUE, stroke_width=5).scale(1.1)))

        self.play(current.animate.next_to(next_node, DOWN, buff=0.18),
                  prev.animate.shift(UP*0.75))
        
        self.wait(1)

        self.play(Transform(rect, SurroundingRectangle(code[:13], color="#FF0000", stroke_width=5).scale(1.1)))

        self.wait(1)

        self.play(FadeOut(VGroup(prev, current, next_node, rect ,code)),
                  self.camera.frame.animate.shift(LEFT*5.2+UP*2.33))
        
        self.wait(1)

        head = Text("head").set_color(BLACK).next_to(d, UP).shift(UP*0.62)
        tail = Text("tail").set_color(BLACK).next_to(a, UP).shift(UP*0.62)  



        self.play(GrowFromCenter(head), GrowFromCenter(tail))   

        self.wait(2)


      



   


        self.embed()
