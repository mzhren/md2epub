#!/usr/bin/env python3
"""
macOS应用程序调试脚本
捕获应用程序崩溃时的错误信息，将日志写入用户桌面
"""
import sys
import os
import traceback
import datetime

def setup_error_logging():
    # 将日志输出到桌面文件
    desktop_path = os.path.expanduser("~/Desktop")
    log_file = os.path.join(desktop_path, "md2epub_crash_log.txt")
    
    # 重定向标准错误输出
    sys.stderr = open(log_file, "w")
    
    # 设置未捕获异常处理器
    def exception_handler(exc_type, exc_value, exc_traceback):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sys.stderr.write(f"[{timestamp}] 未捕获的异常:\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=sys.stderr)
        sys.stderr.flush()
    
    sys.excepthook = exception_handler
    
    return log_file

if __name__ == "__main__":
    log_path = setup_error_logging()
    print(f"错误日志将保存到: {log_path}")
    
    # 导入并运行主程序
    try:
        import app  # 导入主程序模块
        app.main()  # 调用主程序入口函数
    except Exception as e:
        print(f"程序启动失败: {e}")
        traceback.print_exc()
