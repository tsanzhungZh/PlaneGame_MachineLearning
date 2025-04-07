import os
from datetime import datetime


class Logger:

    LOG_LEVELS = {
        'INFO': 0,
        'DEBUG': 1,
        'WARNING': 2,
        'ERROR': 3,
        'CRITICAL': 4
    }

    def __init__(self, log_file="log.txt", log_level='INFO', max_file_size=1024 * 1024):
        """
        增强版日志系统
        :param log_file: 日志文件路径
        :param log_level: 日志级别（DEBUG/INFO/WARNING/ERROR/CRITICAL）
        :param max_file_size: 最大文件大小（字节），超过将备份，默认1MB
        """
        self.log_file = log_file
        self.log_level = self.LOG_LEVELS.get(log_level,0)
        self.max_file_size = max_file_size

        # 初始化日志文件
        self._init_log_file()

    def _init_log_file(self):
        """初始化日志文件，处理日志轮转"""
        if os.path.exists(self.log_file):
            # 检查文件大小
            if os.path.getsize(self.log_file) >= self.max_file_size:
                # 备份旧日志
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_file = f"{self.log_file}.{timestamp}.bak"
                os.rename(self.log_file, backup_file)

        # 写入文件头
        with open(self.log_file, 'a') as f:
            f.write(f"\n\n=== Log Started at {self._get_timestamp()} ===\n")
            f.write(f"=== Log Level: {self._get_level_name(self.log_level)} ===\n\n")

    def _get_timestamp(self):
        """获取带毫秒的时间戳"""
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    def _get_level_name(self, level_value):
        """根据数值获取级别名称"""
        for name, value in self.LOG_LEVELS.items():
            if value == level_value:
                return name
        return 'UNKNOWN'

    def log(self, message, level='INFO', show_console=True):
        """
        记录日志
        :param message: 日志消息
        :param level: 日志级别
        :param show_console: 是否在控制台显示
        """
        level_value = self.LOG_LEVELS.get(level, 0)  # 默认为INFO

        if level_value >= self.log_level:
            log_entry = f"[{self._get_timestamp()}] [{level}] {message}\n"

            # 写入文件
            with open(self.log_file, 'a') as f:
                f.write(log_entry)

            # 控制台输出
            if show_console:
                print(log_entry.strip())


# 使用示例
if __name__ == "__main__":
    # 创建日志器，只记录WARNING及以上级别的日志
    logger = Logger(log_file="abc.txt")

    # 这些消息不会被记录（级别低于WARNING）
    logger.log("调试信息", 'DEBUG')
    logger.log("普通信息", 'INFO')

    # 这些消息会被记录
    logger.log("警告信息", 'WARNING')
    logger.log("错误信息", 'ERROR')
    logger.log("严重错误", 'CRITICAL')