import pathlib
import threading
from process import *
import subprocess
import logging
import time
from random import randint

gameList = ['genshinimpact','hd-player']

def realTimeChecker(processNameList):
    #check if game process exist > new list of running process
    gameProcess = [x for x in processNameList if checkPID(x)]
    print(gameProcess)
    #do something to annoy user
    for gP in gameProcess:
        procData = checkPID(gP)
        for p in procData:
            pName = p['name']
            pPID = p['pid']
            print(f'The PID for {pName} is {pPID}')\

def getAtLocalDir(fileName): 
    scp = pathlib.Path(__file__).parent
    fileAtLocal = scp.joinpath(fileName)
    return str(fileAtLocal).replace('\\','/')

def punishment(stack):
    py_name = "TrollWindow.py"
    py_loc = getAtLocalDir(py_name)
    args = ["python", py_loc]
    
    try:
        for x in range(stack):
            res = subprocess.Popen(args, stdout=subprocess.PIPE)
            output, error_ = res.communicate()
            if not error_:
                logger.debug(f'Punishment subprocess returns : {output}')                
            else:
                logger.error(f'Punishment subprocess error : {error_}')
    except Exception as e:
        logger.exception(e)
    finally:
        logger.debug('Punishment done')
    
    return

class warden(threading.Thread):
    def __init__(self, prisoner):
        threading.Thread.__init__(self)
        self.prisoner = prisoner
        self.exit_flag = False
        logger.debug(f'Warden thread ({self.prisoner}) is created')

    def run(self):
        # TODO Check if related process (prisoner) is running        
        # Punish if still alive
        # If not alive, warden keep monitoring
        while not self.exit_flag:
            try:
                if checkProcess(self.prisoner):
                    threading.Thread(target=punishment, args=[randint(1,2)]).start()
                    logger.debug(f'Punsihment for {self.prisoner}')                       
                time.sleep(5*60)
            except:
                self.exit_flag = True       
        

class manager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.exitLoop = False
    
    def run(self):
        
        while not self.exitLoop:
            self.activeThreadsCount = threading.active_count()
            logger.info(f'Active Thread Count : {self.activeThreadsCount}')
            for l in threading.enumerate():
                logger.info(f'Active Thread : {l}')            
            time.sleep(30)

if __name__ == "__main__":
    # realTimeChecker(gameList)
    # punishment(2)
    cells = []

    logging.basicConfig(filename=getAtLocalDir('logging.log'),format='%(asctime)s %(message)s', filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    gstEye = manager()
    gstEye.start()

    #TODO Loop through the monitor.txt file 
    prison = list() # Thread list
    prisonAddr = getAtLocalDir("monitor.txt")
    try:
        # monitor = open('PYTHON PRACTICEs\GameStudyTimer\monitor.txt','r')
        monitor = open(prisonAddr,'r')
        # cells = monitor.readlines()
        cells = monitor.read().splitlines()
        monitor.close()

    except Exception as e:
        logger.exception(e)
    finally:        
        logger.info(f'Prison Cell : {cells}')  
    #TODO Generate a warden thread on every process listed in monitor.txt
    try:
        for p in cells:
            tempPtr = warden(p)
            tempPtr.start()
            prison.append(tempPtr)
            logger.debug(tempPtr)
                        
    except Exception as e:
        logger.debug(e)
    finally:
        logger.debug('Finished wardens creation')
    
    for p in prison:
        p.join()
    gstEye.join()
    

    