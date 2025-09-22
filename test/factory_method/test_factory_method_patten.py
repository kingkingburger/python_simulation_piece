import unittest
from abc import ABC, abstractmethod
import os

# 1. Product (제품): 생성될 객체의 인터페이스
class Logger(ABC):
    """
    모든 로거가 구현해야 할 공통 인터페이스를 정의합니다.
    """
    @abstractmethod
    def log(self, message: str) -> None:
        pass

# 2. Concrete Products (구체적인 제품): 인터페이스의 실제 구현체
class FileLogger(Logger):
    """
    메시지를 파일에 기록하는 로거입니다.
    """
    def __init__(self, file_path: str):
        self._file_path = file_path
        # 테스트 실행 시 파일을 매번 초기화하기 위해 w 모드를 사용합니다.
        with open(self._file_path, 'w', encoding='utf-8') as f:
            f.write('')

    def log(self, message: str) -> None:
        with open(self._file_path, 'a', encoding='utf-8') as f:
            f.write(f"[FILE] {message}\n")

class ConsoleLogger(Logger):
    """
    메시지를 콘솔에 출력하는 로거입니다.
    """
    def log(self, message: str) -> None:
        # 테스트 용이성을 위해 실제 print 대신 결과를 리스트에 저장합니다.
        # 실제 운영 코드에서는 print(f"[CONSOLE] {message}") 를 사용합니다.
        if not hasattr(self, '_logs'):
            self._logs = []
        self._logs.append(f"[CONSOLE] {message}")
        print(f"[CONSOLE] {message}")


# 3. Creator (생성자): 제품을 생성하는 팩토리 메서드를 선언
class LoggerFactory(ABC):
    """
    로거 객체를 생성하는 팩토리의 추상 베이스 클래스입니다.
    팩토리 메서드 `create_logger`를 정의합니다.
    """
    @abstractmethod
    def create_logger(self) -> Logger:
        """팩토리 메서드: 서브클래스에서 구현해야 합니다."""
        pass

    def log_message(self, message: str) -> None:
        """
        팩토리 메서드를 사용하여 제품(로거)을 생성하고 사용하는 예시 메서드입니다.
        이 메서드는 어떤 종류의 로거가 생성되는지 알 필요가 없습니다.
        """
        logger = self.create_logger()
        logger.log(message)

# 4. Concrete Creators (구체적인 생성자): 팩토리 메서드를 실제로 구현
class FileLoggerFactory(LoggerFactory):
    """
    FileLogger 인스턴스를 생성하는 구체적인 팩토리입니다.
    """
    def __init__(self, file_path: str):
        self._file_path = file_path

    def create_logger(self) -> Logger:
        """FileLogger를 생성하여 반환합니다."""
        return FileLogger(self._file_path)

class ConsoleLoggerFactory(LoggerFactory):
    """
    ConsoleLogger 인스턴스를 생성하는 구체적인 팩토리입니다.
    """
    def create_logger(self) -> Logger:
        """ConsoleLogger를 생성하여 반환합니다."""
        return ConsoleLogger()


# 5. unittest: 팩토리 메서드 패턴 테스트
class TestLoggerFactory(unittest.TestCase):
    """
    팩토리 메서드 패턴 구현을 검증하는 테스트 스위트입니다.
    """
    def setUp(self):
        """각 테스트 메서드 실행 전에 호출됩니다."""
        self.test_log_file = "test_log.txt"

    def tearDown(self):
        """각 테스트 메서드 실행 후에 호출됩니다."""
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

    def test_file_logger_creation_and_logging(self):
        """FileLoggerFactory가 FileLogger를 올바르게 생성하고, 로그가 파일에 잘 기록되는지 테스트합니다."""
        # Arrange: FileLoggerFactory 인스턴스 생성
        factory = FileLoggerFactory(self.test_log_file)
        message_to_log = "This is a test for the file logger."

        # Act: 팩토리를 통해 로깅 실행
        factory.log_message(message_to_log)

        # Assert: 생성된 로거 타입 확인 및 파일 내용 검증
        logger = factory.create_logger()
        self.assertIsInstance(logger, FileLogger, "팩토리는 FileLogger 인스턴스를 생성해야 합니다.")

        with open(self.test_log_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        self.assertEqual(content, f"[FILE] {message_to_log}", "로그 메시지가 파일에 올바르게 기록되어야 합니다.")
        print(f"\n✅ test_file_logger_creation_and_logging 통과")


    def test_console_logger_creation_and_logging(self):
        """ConsoleLoggerFactory가 ConsoleLogger를 올바르게 생성하고, 로그가 잘 기록되는지 테스트합니다."""
        # Arrange: ConsoleLoggerFactory 인스턴스 생성
        factory = ConsoleLoggerFactory()
        message_to_log = "This is a test for the console logger."

        # Act: 팩토리를 통해 로거 생성 및 로깅 실행
        logger = factory.create_logger()
        logger.log(message_to_log)

        # Assert: 생성된 로거 타입 확인 및 내부 로그 리스트 검증
        self.assertIsInstance(logger, ConsoleLogger, "팩토리는 ConsoleLogger 인스턴스를 생성해야 합니다.")
        # ConsoleLogger는 테스트를 위해 내부적으로 _logs 리스트에 로그를 저장합니다.
        self.assertEqual(logger._logs[0], f"[CONSOLE] {message_to_log}", "로그 메시지가 콘솔 로거 내부에 올바르게 기록되어야 합니다.")
        print(f"✅ test_console_logger_creation_and_logging 통과")


# 테스트 실행
if __name__ == '__main__':
    unittest.main(verbosity=2)