class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class NullHandler:
    def __init__(self, successor):
        self.__successor = successor

    def handle(self, char, event):
        if self.__successor:
            return self.__successor.handle(char, event)


class IntHandler(NullHandler):
    def handle(self, char, event):
        if isinstance(event, EventGet) and (event.value == int):
            return char.integer_field
        elif isinstance(event, EventSet) and isinstance(event.value, int):
            char.integer_field = event.value
        else:
            return super().handle(char, event)


class FloatHandler(NullHandler):
    def handle(self, char, event):
        if isinstance(event, EventGet) and (event.value == float):
            return char.float_field
        elif isinstance(event, EventSet) and isinstance(event.value, float):
            char.float_field = event.value
        else:
            return super().handle(char, event)


class StrHandler(NullHandler):
    def handle(self, char, event):
        if isinstance(event, EventGet) and (event.value == str):
            return char.string_field
        elif isinstance(event, EventSet) and isinstance(event.value, str):
            char.string_field = event.value
        else:
            return super().handle(char, event)


class EventGet:
    def __init__(self, value):
        self.value = value


class EventSet:
    def __init__(self, value):
        self.value = value



obj = SomeObject()
obj.integer_field = 42
obj.float_field = 3.14
obj.string_field = "some text"
chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
print(chain.handle(obj, EventGet(int)))
print(chain.handle(obj, EventGet(float)))
print(chain.handle(obj, EventGet(str)))
chain.handle(obj, EventSet(100))
print(chain.handle(obj, EventGet(int)))
chain.handle(obj, EventSet(0.5))
print(chain.handle(obj, EventGet(float)))
chain.handle(obj, EventSet('new text'))
print(chain.handle(obj, EventGet(str)))
