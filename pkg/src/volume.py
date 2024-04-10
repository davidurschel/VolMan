from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import numpy as np


def PercentageToDB(percentage:float, minV:float=-60.0, maxV:float=0.0) -> float:
    percentage=max(min(percentage, 100.0), 0.0)
    if percentage == 0.0:
        return minV
    res = np.log((percentage/100+0.0196871)/(1.01969))/0.0657881
    return max(min(res, maxV), minV)


def SetSystemVolume(percentage:float):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(PercentageToDB(percentage), None)
    return


def SetApplicationVolume(percentage:float, application:str):
    sessions = AudioUtilities.GetAllSessions()
    percentage = max(min(percentage, 100.0), 0.0)
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == application:
            volume.SetMasterVolume(percentage/100, None)
    return


"""Takes a set of all applications and the volume percentage to which they should be set"""
def SetApplicationVolumes(applications:{str, float}):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process == None:
            continue
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        processName = session.Process.name()
        if processName in applications:
            percentage = applications[processName]
            percentage = max(min(percentage, 100.0), 0.0)
            volume.SetMasterVolume(percentage/100, None)
    return


"""Returns all the names of the applications for all processes that are currently visible under the volume mixer tab"""
def GetActiveVolumeSessions() -> list:
    res = []
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            res.append(session.Process.name())
    return res
