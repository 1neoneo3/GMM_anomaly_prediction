import logging
import datetime
import os

class Logging:
   """
   このクラスのインスタンスを作成すると、
   名前付きのlogging.Loggerインスタンスが作成され、
   指定したファイルにログを出力できる。
   """
   logger = None
   def __init__(self,module_name,isLibrary=False,isTest=False):
       """
       module_name:str型、pythonのプログラム名を想定。
       is_library:bool型、defaultはfalse、ライブラリモジュールの時はTrueにする。
       """
       dt = datetime.datetime.now().strftime("%Y%m%d%H%M")
       log_path = "./logs/"
       if not os.path.isdir(log_path):
           os.makedirs(log_path)
       if not isLibrary:
           logging.basicConfig(
               level=logging.DEBUG,
               format='[%(levelname)s] %(asctime)s %(message)s , "shift-jis"',
               filename="./logs/{module_name}_{dt}.log".format(module_name=module_name,dt=dt)
           )
       self.logger = self._get_module_logger(module_name,isTest)

   def _get_module_logger(self,module_name,isTest):
       """
       ret:logging.Logger
       handlerの種類は2つ
       error_handler:warning以上のレベルのログを全プログラム共通のファイルに出力する。
       stream_handler:すべてのレベルのログをコマンドライン上に出力する。
       """
       logger = logging.getLogger(module_name)
       day = datetime.date.today().strftime("%Y%m%d")
       error_handler = logging.FileHandler(filename="./logs/aplog_{day}.log".format(day=day))
       #handlerにログレベルを指定する。
       error_handler.setLevel("INFO")
       #loggerインスタンスにhandlerを追加する。
       if isTest:
           stream_handler = logging.StreamHandler()
           stream_handler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s'))
           logger.addHandler(stream_handler)
       logger.addHandler(error_handler)
       return logger

   def debug_log(self,msg):
       """
       変数の値などをログに残す際に使う。
       """
       self.logger.debug(msg)
   
   def info_log(self,msg):
       """
       各処理の開始や終了の際に使う。
       """
       self.logger.info(msg)
   
   def warning_log(self,msg):
       """
       エラーではないが期待した処理結果でない可能性があるときに使う。
       """
       self.logger.warning(msg)
   
   def error_log(self,msg):
       """
       例外が発生したときに使う。
       except節の中でのみ使う。
       """
       self.logger.exception(msg)