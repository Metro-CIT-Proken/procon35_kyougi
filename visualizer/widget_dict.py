class WidgetDict:
    def __init__(self):
        self.zoom = 1
        self.zoom_direction = 0

        self.board_width = 0
        self.board_height = 0
        self.dis_board = [[]]
        self.answer = {
                        "n": 0,
                        "ops": [
                                ]
                        }
        self.start_board = [[]]
        self.goal_board = [[]]
        self.start_widget = None
        self.goal_widget = None
        self.double_widget = None

