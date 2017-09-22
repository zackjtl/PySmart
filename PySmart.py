import osinfo
import re
from ctypes import *

_libPath = osinfo.libdir + '\\SmartSDK_1288_Win32.dll'
_smartLib = WinDLL(_libPath)

_smartLib.GetMPVersion.restype = c_char_p
_smartLib.GetFlashType.restype = c_char_p
_smartLib.GetFlashID.restype = c_char_p
_smartLib.GetHWVersion.restype = c_char_p
_smartLib.GetFWVersion.restype = c_char_p
_smartLib.GetRemainingLife.restype = c_float
_smartLib.GetECCUncorrectableCount.restype = c_ushort
_smartLib.GetInitialBadBlockCount.restype = c_ushort
_smartLib.GetMinSpareBlockCount.restype = c_ushort
_smartLib.GetLaterBadBlockCount.restype = c_ushort
_smartLib.GetTotalCECount.restype = c_byte
_smartLib.GetECCCapacity.restype = c_byte
_smartLib.GetEraseCountOffset.restype = c_ushort
_smartLib.GetHeaderVersion.restype = c_byte

_drive = ''

def Initial(_driveName:str):
    global _drive
    _drive = _driveName
    # Use SMART Version 2 transaction
    _smartLib.SetTransactionVersion(2) 
    
def Read():
    global _drive
    strBuf = create_string_buffer(_drive.encode('utf-8'))
    _smartLib.SetDiskName(strBuf)        
    _smartLib.GetSmartInfo.restype = c_byte
    ret = _smartLib.GetSmartInfo()
    
    _smartLib.CloseDeviceHandle()

    return ret

def GetErrorMessage():
    _smartLib.GetErrorMessage.restype = c_char_p
    ret = _smartLib.GetErrorMessage()
    return ret.decode('utf-8')

class BasicSmartInfo:
    def __init__(self):
        self.MPVersionStr = ''
        self.FlashTypeStr = ''
        self.FlashIDStr = ''
        self.TotalCECount = 0
        self.ECCCapacity = 0
        self.HWVersionStr = ''
        self.FWVersionStr = ''
        self.AbnormalShutdownCount = 0
        self.ECCUncCount = 0
        self.PowerCycleCount = 0
        self.FactoryBadBlocks = 0
        self.MininumSpareBlocks = 0
        self.LaterBadBlocks = 0
        self.TotalEraseCount = 0
        self.AverageEraseCount = 0
        self.MaximumEraseCount = 0 
        self.MinimumEraseCount = 0
        self.LifeIndicator = 0.0
        self.TotalVBCount = 0
        self.VBMultiplier = 0
        self.HeaderVersion = 0
        self.EraseCountOffset = 0
    
    def reset(self):
        self.MPVersionStr = _smartLib.GetMPVersion().decode('utf-8')
        self.FlashTypeStr = _smartLib.GetFlashType().decode('utf-8')
        self.FlashIDStr = _smartLib.GetFlashID().decode('utf-8')
        self.TotalCECount = int(_smartLib.GetTotalCECount())
        self.ECCCapacity = int(_smartLib.GetECCCapacity())
        self.HWVersionStr = _smartLib.GetHWVersion().decode('utf-8')
        self.FWVersionStr = _smartLib.GetFWVersion().decode('utf-8')
        self.AbnormalShutdownCount = int(_smartLib.GetAbnormalShutdownCount())
        self.ECCUncCount = int(_smartLib.GetECCUncorrectableCount())
        self.PowerCycleCount = _smartLib.GetPowerCycleCount()
        self.FactoryBadBlocks = int(_smartLib.GetInitialBadBlockCount())
        self.MininumSpareBlocks = int(_smartLib.GetMinSpareBlockCount())
        self.LaterBadBlocks = int(_smartLib.GetLaterBadBlockCount())
        self.TotalEraseCount = _smartLib.GetTotalEraseCount()
        self.AverageEraseCount = _smartLib.GetAverageEraseCount()
        self.MaximumEraseCount = _smartLib.GetMaxEraseCount()
        self.MinimumEraseCount = _smartLib.GetMinEraseCount()
        self.LifeIndicator = _smartLib.GetRemainingLife()
        self.TotalVBCount = _smartLib.GetTotalVBCountOfFlash()
        self.VBMultiplier = _smartLib.GetVBMultiplier()
        self.HeaderVersion = int(_smartLib.GetHeaderVersion())
        self.EraseCountOffset = int(_smartLib.GetEraseCountOffset())        

    def __str__(self):
        txt = ''
        #members = dir(self)
        for key in self.__dict__:
            if not key.startswith('__') and not key.endswith('__'):                
                value = self.__dict__[key]
                
                if not re.match('<function.*?>', str(value)):
                    #field = 'self.{}'.format(key)     
                    if (key is 'LifeIndicator'):   
                        val_str = str(value)
                        point_at = val_str.find('.')
                        end_pos = min(len(val_str), point_at+3)
                        txt += '{: <22}: {} %\n'.format(key, val_str[:end_pos])
                    else:
                        txt += '{: <22}: {}\n'.format(key, str(value))
        return txt
        
def GetBasicSmartInfo():
    info = BasicSmartInfo()
    info.reset()

    return info