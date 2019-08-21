from MyLog import MyLog

def bb():
    mylog = MyLog(__name__)

    log = mylog.getLogger()

    log.info('b')