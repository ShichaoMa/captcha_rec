#!/bin/python3.6
# -*- coding:utf-8 -*-
import os
import time
import socket
import select
import traceback
import threading

from queue import Queue, Empty
from argparse import ArgumentParser

from log_to_kafka import Logger
from multi_thread_closing import MultiThreadClosing

from utils import common_stop_start_control
from utils.captcha import binarized


class Recognition(Logger, MultiThreadClosing):
    """
        amazon专用验证码识别程序
    """
    name = "recognition"

    def __init__(self, settings):
        Logger.__init__(self, settings)
        MultiThreadClosing.__init__(self)
        self.readable = Queue()
        self.host = self.settings.get("CAPTCHA_RECOGNITION_HOST")
        self.port = self.settings.get("CAPTCHA_RECOGNITION_PORT")
        self.server = None
        self.callback = binarized

    def setup(self):
        self.server = socket.socket()
        self.server.bind((self.host, self.port))
        print("Recognization server starting up ...")
        print("Listening on http://%s:%d/" % (self.host, self.port))
        print("Hit Ctrl-C to quit.")
        self.server.listen(10)
        t = threading.Thread(target=self.poll_queue)
        self.threads.append(t)
        t.start()

    def poll_queue(self):
        """
            子进程从验证码通道里取出客户端socket进行验证码识别
        """
        while self.alive or self.readable.qsize():
            now = time.time()
            client = None
            try:
                client, addr, t = self.readable.get_nowait()
                if now-t > 20:
                    self.logger.debug("Abandon client from %s:%s. "%addr)
                    client.close()
                    continue
                self.recognize(client, addr, t)
            except Empty:
                self.logger.debug("No client. ")
                time.sleep(1)
            except Exception:
                self.logger.error("Error in poll_queue: %s. " % traceback.format_exc())
            finally:
                if client:
                    client.close()

    def start(self):
        """
            将接收到的socket链接放入验证码通道交付给子进程处理
        """
        try:
            self.setup()
            while self.alive or [x for x in self.threads if x.is_alive()]:
                try:
                    rd_lst, _, _ = select.select([self.server], [], [], 0.1)
                    if not rd_lst:
                        time.sleep(1)
                    for rd in rd_lst:
                        client, addr = rd.accept()
                        self.readable.put((client, addr, time.time()))
                except Exception:
                    self.logger.error("Error in start: %s. " % traceback.format_exc())
        finally:
            if self.server:
                self.server.close()

    def recognize(self, client, addr, t):
        """
            接收验证码字节流，并判断是否超时，如果超时60，则丢弃，否则返回处理结果
        """
        try:
            self.logger.info("Receive captcha from %s:%s. " % addr)
            buf = client.recv(102400)
            alphabet = self.callback(buf)
            if time.time()-t > 60:
                self.logger.info("Time out. ")
            else:
                if isinstance(alphabet, str):
                    alphabet = alphabet.encode("utf-8")
                client.send(alphabet)
                self.logger.info("Send result:%s to %s:%s. "%((alphabet, )+addr))
        except Exception:
            self.logger.error("Error in recognize: %s. "%traceback.format_exc())

    @classmethod
    def run(cls):
        parser = ArgumentParser()
        parser.add_argument("-s", "--settings", default="settings.py")
        from settings import BASENAME, LOG_DIR
        # 这个log是代替的标准输出和标准错误
        monitor_log_path = os.path.join(BASENAME, LOG_DIR, os.path.splitext(os.path.basename(__file__))[0] + ".log")
        args = common_stop_start_control(parser, monitor_log_path, 2)
        rg = cls(args.settings)
        rg.set_logger()
        rg.start()


if __name__ == "__main__":
    Recognition.run()