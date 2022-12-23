class Color:
    END = "\033[0"
    START = "\033[1;38;2"
    MOD = "m"

    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

    def __repr__(self):
        return f'{self.START};{self.red};{self.green};{self.blue}{self.MOD}●{self.END}{self.MOD}'

    @staticmethod
    def _is_correct_ch(channel):
        if not isinstance(channel, int):
            raise ValueError(f"{type(channel)} != int")

        if not 0 <= channel <= 255:
            raise ValueError("channel > 255 or channel < 0")

    @property
    def red(self):
        return self.red_

    @property
    def green(self):
        return self.green_

    @property
    def blue(self):
        return self.blue_

    @red.setter
    def red(self, channel):
        Color._is_correct_ch(channel)
        self.red_ = channel

    @blue.setter
    def blue(self, channel):
        Color._is_correct_ch(channel)
        self.blue_ = channel

    @green.setter
    def green(self, channel):
        Color._is_correct_ch(channel)
        self.green_ = channel

    def __eq__(self, other):
        if self is other:
            return True
        if self.red == other.red and self.green == other.green and self.blue == other.blue:
            return True
        else:
            return False

    def __add__(self, other):
        self.red += other.red
        self.green += other.green
        self.blue += other.blue
        return f'{self.START};{self.red};{self.green};{self.blue}{self.MOD}●{self.END}{self.MOD}'

    def __hash__(self):
        color_tuple = (self.red, self.green, self.blue)
        return hash(color_tuple)

    def __mul__(self, c):
        if c > 1 or c < 0:
            raise ValueError(f"{c} not in range")
        cl = - 256 * (1 - c)
        F = (259 * (cl + 255)) / (255 * (259 - cl))
        r = int(F * (self.red - 128) + 128)
        g = int(F * (self.green - 128) + 128)
        b = int(F * (self.blue - 128) + 128)
        return Color(r, g, b)

    def __rmul__(self, other):
        return self.__mul__(other)


if __name__ == '__main__':
    red = Color(255, 0, 0)
    print(red)
    green = Color(0, 255, 0)
    assert red != green
    assert red == Color(255, 0, 0)
    print(red + green)
    green = Color(0, 255, 0)
    red = Color(255, 0, 0)
    orange1 = Color(255, 165, 0)
    orange2 = Color(255, 165, 0)
    color_list = [orange1, red, green, orange2]
    print(set(color_list))
    print(0.5 * red)
