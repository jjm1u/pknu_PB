class MoveToWallError(Exception):
    """벽으로 이동하려고 할 경우 발생하는 사용자 정의 예외"""
    def __init__(self):
            super().__init__()
            
class WidthSizeError(Exception):
        """미로 가로 크기가 지정 범위 (20 ~ 70) 을 벗어날 때 발생하는 사용자 정의 예외"""
        def __init__(self, message):
            super().__init__(message)

class HeightSizeError(Exception):
    """미로 세로 크기가 지정범위 (10 ~ 60) 을 벗어날 때 발생하는 사용자 정의 예외"""
    def __init__(self, message):
        super().__init__(message)

class CheckpointNotPassedError(Exception):
    def __init__(self, message):
        super().__init__(message)
