import time
import pygame
import pygame.freetype
import random

# Màu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (187, 238, 255)
PURPLE = (192, 204, 255)

# Tạo cửa sổ game
WIN = pygame.display.set_mode((640, 480))


class Screen:  # hiển thị tất cả những đối tượng có trên màn hình game (tiêu đề của từng màn hình, điểm của người chơi)
    Font = None

    def __init__(self, next_screen, *text):
        self.background = pygame.Surface((640, 480))  # Tạo khung để gán màu hoặc hình ảnh
        self.background.fill(BLUE)  # Gán màu hoặc hình ảnh

        y = 80
        if text:
            Screen.Font = pygame.freetype.SysFont('times', 32)  # (font chữ, kích thước)
            for line in text:
                Screen.Font.render_to(self.background, (120, y), line, BLACK)  # (surface, vị trí hiển thị (x, y), text, màu)
                y += 50  # cứ mỗi 1 dòng trong *text được hiển thị thì y sẽ di chuyển xuống 50 đơn vị

        self.next_screen = next_screen
        self.add_text = None

    def start(self, text):
        self.add_text = text

    def draw(self):
        WIN.blit(self.background, (0, 0))  # in đè lên cả khung hình
        if self.add_text:
            y = 180
            for line in self.add_text:
                Screen.Font.render_to(WIN, (120, y), line, BLACK)
                y += 50

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # hoạt động khi bấm nút space
                    return self.next_screen, None


class SettingScreen:  # Vị trí hiển thị các câu hỏi, câu trả lời cũng như kiểm tra vị trí chuột

    def __init__(self):
        self.background = pygame.Surface((640, 480))
        self.background.fill(BLUE)

        Screen.Font.render_to(self.background, (120, 50), 'Select your difficulty level', BLACK)

        self.rects = []
        x = 120
        y = 120
        for i in range(4):
            rect = pygame.Rect(x, y, 80, 80)  # tạo khung để chọn (x, y, chiều rộng, chiều cao)
            self.rects.append(rect)  # thêm rect vào trong list
            x += 100

    def start(self, *args):
        pass

    def draw(self):
        WIN.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:  # kiểm tra vị trí chuột trên cả cửa sổ màn hình
            if rect.collidepoint(pygame.mouse.get_pos()):  # collidepoint để kiểm tra có nằm trong vùng được con chuột đang hiển thị ko
                                                           # pygame.mouse.get_pos() lấy vị trí con trỏ chuột
                pygame.draw.rect(WIN, PURPLE, rect)
            pygame.draw.rect(WIN, PURPLE, rect, 5)  # vẽ viền qua phần chọn
            Screen.Font.render_to(WIN, (rect.x + 30, rect.y + 30), str(n), BLACK)  # (surface, vị trí hiển thị (x, y), text, màu)
            n += 1  # mỗi lần lặp thì n thêm 1 để hiển thị ra màn hình

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:  # kiểm tra chuột có được bấm không
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        return 'GAME', GameLevel()


class GameLevel:  # Câu hỏi, đáp án,
    def __init__(self):

        self.questions = [
            ('Tìm x: (5-x) + (6+x) = 11', 3),
            ('Tìm x: 4(x+7) + 11(x-2) -3 = 0', 2),
            ('Tìm số còn thiếu 1357986_2', 4),
            ('Vịt Donald đi bằng mấy chân ?', 2),
            ('Có bao nhiêu chữ C: Con cua 8 cẳng 2 càng ', 1)
        ]
        self.current_question = None
        self.game_state = None
        self.background = None
        self.right = 0
        self.wrong = 0

    def pop_question(self):
        ques = random.choice(self.questions)  # random câu hỏi
        self.questions.remove(ques)  # bỏ đi câu hỏi vừa được random ra khỏi list để tránh bị lặp câu
        self.current_question = ques  # câu hỏi hiển thị hiện tại sẽ bằng ques
        return ques

    def answer(self, answer):
        if answer == self.current_question[1]:  # câu trả lời được chọn nếu trùng với đáp án
            time.sleep(0.5)     # dừng lại trước khi chuyển sang câu hỏi mới để tránh bị chọn liền 2 câu hỏi
            self.right += 1
        else:
            time.sleep(0.5)
            self.wrong += 1

    def get_result(self):
        return f'{self.right} answers correct', f'{self.wrong} answers wrong', '', 'Good!' \
            if self.right > self.wrong else 'You can do better!'


class GamePlay(GameLevel):
    def __init__(self):
        super().__init__()
        self.rects = []
        x = 120
        y = 120

        for n in range(4):  # tạo ra khung chọn đáp án
            rect = pygame.Rect(x, y, 400, 80)
            self.rects.append(rect)
            y += 90

        self.game_level = None

    def start(self, game_level):
        self.background = pygame.Surface((640, 480))
        self.background.fill(BLUE)
        self.game_level = game_level
        question, answer = game_level.pop_question()
        Screen.Font.render_to(self.background, (120, 50), question, BLACK)

    def draw(self):
        WIN.blit(self.background, (0, 0))
        n = 1
        for rect in self.rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(WIN, PURPLE, rect)
            pygame.draw.rect(WIN, PURPLE, rect, 5)
            Screen.Font.render_to(WIN, (rect.x + 30, rect.y + 30), str(n), BLACK)
            n += 1

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                n = 1
                for rect in self.rects:
                    if rect.collidepoint(event.pos):
                        self.game_level.answer(n)  # dòng 109 ( kiểm tra đáp án ) n: biến answer
                        if self.game_level.questions:  # mỗi khi hiển thị câu hỏi chạy lại phần gameplay
                                                       # chạy lại gameplay đồng nghĩa với tạo ra khung dáp án mới
                            return 'GAME', self.game_level  # nếu còn câu hỏi tiếp tục thực hiện
                        else:
                            return 'RESULT', self.game_level.get_result()  # Khi đã hết câu hỏi chuyển đến phần hiển thị kết quả
                    n += 1


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screens = {
        'TITLE': Screen('SETTING', 'Welcome to the game', '', '', '', 'Press [Space] to start'),
        'SETTING': SettingScreen(),
        'GAME': GamePlay(),
        'RESULT': Screen('TITLE', 'Here is your result:'),
    }  # Tham khảo trên mạng
    """
    'SETTING': tạo vị trí hiển thị các câu hỏi, câu trả lời cũng như kiểm tra vị trí chuột
    'GAME': Chạy câu hỏi, Nhận câu trả lời 
    'TITLE': chạy SETTING, hiển thị phần *text
    'RESULT': giống với TITLE nhưng phần này chỉ đc gọi ra khi chạy hết phần câu hỏi 
              nên *text sẽ hiển thị 'Here is your result:' và phần kết quả
    """


    screen = screens['TITLE']
    while True:
        clock.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False

        result = screen.update(events)
        if result:
            next_screen, level = result
            if next_screen:
                screen = screens[next_screen]
                screen.start(level)

        screen.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
