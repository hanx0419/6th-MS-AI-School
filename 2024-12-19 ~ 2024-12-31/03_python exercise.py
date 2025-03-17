import turtle

class Rectangle:
    def __init__(self):
        """사각형 객체 생성"""
        self.x = 0
        self.y = 0
        self.width = 50  # 기본 너비
        self.height = 50  # 기본 높이
        self.color = 'black'

    def set_rectangle(self, x, y, width=50, height=50, color='black'):
        """사각형 속성 설정"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        """사각형을 그리는 메서드"""
        turtle.penup()
        turtle.goto(self.x, self.y)
        turtle.pendown()
        turtle.pencolor(self.color)

        for _ in range(2):
            turtle.forward(self.width)
            turtle.right(90)
            turtle.forward(self.height)
            turtle.right(90)

def get_mouse_click_coor(x, y):
    """마우스 클릭 시 사각형을 그리는 함수"""
    print(f"Clicked at: {x}, {y}")
    rect = Rectangle()
    rect.set_rectangle(x, y, 50, 50, 'blue')  # 클릭 위치에 사각형 생성
    rect.draw()

# 메인 실행 부분
if __name__ == "__main__":
    turtle.speed(0)  # 거북이 속도 설정
    turtle.onscreenclick(get_mouse_click_coor)  # 마우스 클릭 이벤트 등록

    turtle.mainloop()  # 터틀 그래픽 창 유지