from MyLog import MyLog
import a
import b

a.aa()
b.bb()

mylog=MyLog(__name__)

log=mylog.getLogger()

log.info('c')