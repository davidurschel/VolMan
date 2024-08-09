from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
import numpy as np


def percentage_to_db(percentage:float, minV:float=-60.0, maxV:float=0.0) -> float:
    percentage=max(min(percentage, 100.0), 0.0)
    if percentage == 0.0:
        return minV
    res = np.log((percentage/100+0.0196871)/(1.01969))/0.0657881
    return max(min(res, maxV), minV)


def set_system_volume(percentage:float):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(percentage_to_db(percentage), None)
    return


def set_app_volume(percentage:float, application:str):
    sessions = AudioUtilities.GetAllSessions()
    percentage = max(min(percentage, 100.0), 0.0)
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == application:
            volume.SetMasterVolume(percentage/100, None)
    return


'''Takes a set of all applications and the volume percentage to which they should be set'''
def set_app_volumes(applications:{str, float}):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process == None:
            continue
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        processName = session.Process.name().lower()
        if processName in applications:
            percentage = applications[processName]
            percentage = max(min(percentage, 100.0), 0.0)
            volume.SetMasterVolume(percentage/100, None)
        elif "OTHER" in applications:
            percentage = applications["OTHER"]
            percentage = max(min(percentage, 100.0), 0.0)
            volume.SetMasterVolume(percentage/100, None)
    return


'''Returns all the names of the applications for all processes that are currently visible under the volume mixer tab'''
def get_active_volume_sessions() -> list:
    res = []
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            res.append(session.Process.name())
    return res


''''''
def match_rails_to_apps(rails:list, apps) -> list:
    res = {}
    for i, rail in enumerate(rails):
        if str(i) not in apps:
            continue

        percentage = float(rail)*100.0 # rail value comes between 0 and 1
        curr_apps = apps[str(i)]
        if type(curr_apps) == list:
            for app in curr_apps:
                if app not in ["OTHER", "MASTER"]:
                    app = app.lower()
                res[app] = percentage
        elif type(curr_apps) == str:
            if curr_apps not in ["OTHER", "MASTER"]:
                    curr_apps = curr_apps.lower()
            res[curr_apps] = percentage

    return res


if __name__ == "__main__":
    print(get_active_volume_sessions())