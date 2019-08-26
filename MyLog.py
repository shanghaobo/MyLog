import logging
import os
from logging import handlers
from threading import Lock
import time

lock=Lock()

class MyTimedRotatingFileHandler(handlers.TimedRotatingFileHandler):
    #重写方法 增加线程锁
    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + "." +
                                     time.strftime(self.suffix, timeTuple))
        # if os.path.exists(dfn):
        #     os.remove(dfn)
        # self.rotate(self.baseFilename, dfn)
        with lock:#增加线程锁 防止多线程操作出错
            if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
                self.rotate(self.baseFilename, dfn)

        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                newRolloverAt += addend
        self.rolloverAt = newRolloverAt


class MyLog:
    logger=None
    def __init__(self,name,filename='log.log'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        format = '[%(asctime)s] [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'
        log_path = os.path.join(os.getcwd(), "logs")
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_filepath = os.path.join(log_path, filename)
        th = MyTimedRotatingFileHandler(filename=log_filepath,when='midnight',encoding='utf-8')
        # th = handlers.TimedRotatingFileHandler(filename=log_filepath,when='S')
        # th.suffix='%Y-%m-%d_%H-%M-%S.log'
        th.setFormatter(logging.Formatter(format,datefmt))
        self.logger.addHandler(th)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(format,datefmt))
        self.logger.addHandler(console)


def getLogger(name):
    mylog=MyLog(name)
    return mylog.logger