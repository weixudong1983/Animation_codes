# ---------- FakeScene: 用于 set_data 内部写入不产生动画的替代对象 ----------
class FakeScene:
    def play(self, *args, **kwargs): pass
    def wait(self, *args, **kwargs): pass
