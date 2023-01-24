from datetime import datetime, timedelta
from ftplib import FTP_TLS
import time
import os
import re


class Logger:
    def __init__(self, uniqueFileNamePrefics="log", logsFolder="logs", specifiedTailName=None, lock=None, logsExpiringTime=None):
        if not specifiedTailName:  # if not specified - filename will contain current date/time
            fileName = f"{uniqueFileNamePrefics}_{time.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
        else:
            fileName = f"{uniqueFileNamePrefics}_{specifiedTailName}.txt"

        if not os.path.exists(logsFolder):
            os.mkdir(logsFolder)

        # os.path.abspath()
        self.__file = open(os.path.join(logsFolder, fileName), 'a', encoding='utf-8')
        self.__fileName = fileName
        self.__logsFolder = logsFolder
        self.__list_errors = []
        self.__threadLock = lock
        self.__expiringTime = logsExpiringTime
        self.__ftpLoginCredentials = None
        self.__uniqueFileNamePrefics = uniqueFileNamePrefics
        self._log("Log file opened.", "INFO")

    def setFTPCredentials(self, host, user, password):
        self.__ftpLoginCredentials = (host, user, password)

    def _log(self, text: str, logType: str):
        # if in thread-mode, firstly lock logger:
        if self.__threadLock:
            self.__threadLock.acquire()
            
        text = f'{logType} [{time.strftime("%Y.%m.%d %X")}]: {text}'
        print(text)
        self.__file.write(text+"\n")

        # then release:
        if self.__threadLock:
            self.__threadLock.release()

    def info(self, text: str):
        self._log(text, "INFO")

    def warning(self, text: str):
        self._log(text, "WARNING")

    def error(self, text: str):
        self._log(text, "ERROR")
        self.__list_errors.append(text)

    def get_list_errors(self):
        return self.__list_errors

    def clear_list_errors(self):
        self.__list_errors.clear()

    def __del__(self):
        self.info("Log file closed.")
        # if have log/pass for FTP server:
        # login before closing file
        if self.__ftpLoginCredentials:
            host = self.__ftpLoginCredentials[0]
            user = self.__ftpLoginCredentials[1]
            password = self.__ftpLoginCredentials[2]
            ftps = FTP_TLS(host=host)
            ftps.encoding = "utf-8"
            ftps.set_debuglevel(1)
            self.info(ftps.login(user=user, passwd=password))
            self.info(ftps.prot_p())

        self.__file.close()
 
        # delete old logs
        if self.__expiringTime != None:  # if not None
            availableFiles = os.listdir(self.__logsFolder)
            availableFiles.remove(self.__fileName)  # not checking current logfile
            for fileName in availableFiles:  # check each older log, if
                dateGroups = re.findall(r"(\d{4})-(\d{2})-(\d{2})", fileName)
                if dateGroups:
                    dateGroup = dateGroups[0]
                    fileDatetime = datetime(year=int(dateGroup[0]), month=int(dateGroup[1]), day=int(dateGroup[2]))
                    if datetime.now() >= fileDatetime + timedelta(days=self.__expiringTime):
                        os.remove(os.path.abspath(os.path.join(self.__logsFolder, fileName)))
                else:
                    print(f"Cant find date groups in file name: '{fileName}'")

        # send to FTP
        if self.__ftpLoginCredentials:
            dirPath = '/'  # variable for accumulating path
            for nextDir in [self.__logsFolder, self.__uniqueFileNamePrefics]:  # list of desired directories
                # os.path.join()
                dirList = ftps.nlst(os.path.dirname(dirPath))
                if dirPath+nextDir not in dirList:
                    ftps.mkd(dirPath+nextDir)   # create directory on the FTP
                dirPath = f"{dirPath}{nextDir}/"  # add new dir name

                with open(os.path.join(self.__logsFolder, self.__fileName), "rb") as file:
                    ftps.storlines(f"STOR {self.__logsFolder}/{self.__uniqueFileNamePrefics}/{self.__fileName}", file)

                ftps.close()
