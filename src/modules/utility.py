import os, fnmatch, re
from datetime import datetime

def printLog(text, status = 'info'):
    if 'error' in status:
        status = '-#' + status + '  #-'
    elif 'info' in status:
        status = '---#' + status + '   #-'
    else:
        status = '--#' + status + '#-'

    status = (
        status
            .upper()
            # Cyan color
            .replace('---#', '\033[36m')

            # Green color
            .replace('--#', '\033[32m')

            # Red color
            .replace('-#', '\033[91m')
            .replace('#-', '\033[0m')
    )

    text = (
        text
            .replace('--#', '\033[32m')
            .replace('-#', '\033[91m')
            .replace('#-', '\033[0m')
    )

    print("[ {0} ][ {1} ] {2}".format(datetime.now().strftime('%m-%d %H:%M'), status, text).strip())


def getHighestTemps(GPUUnits):
    temps = []
    for unit in GPUUnits:
        unit.detect()
        temps.append(unit.temperature)

    return int(round(max(temps), 2))



def getAverageTemps(GPUUnits):
    temps = []
    for unit in GPUUnits:
        unit.detect()
        temps.append(unit.temperature)

    return int(round(float(sum(temps)) / max(len(temps), 1), 2))



def calculateStep(minStep, maxStep, currentStep, targetTemp, currentTemp, stepUp=None, stepDown=None):
    if not stepUp:
        stepUp = 7

    if not stepDown:
        stepDown = 1

    currentStep = int(currentStep)

    if int(currentTemp) > int(targetTemp):
        currentStep += int(stepUp)

    elif int(currentTemp) < int(targetTemp):
        currentStep -= int(stepDown)

    return int(max(min(int(maxStep), currentStep), int(minStep)))


def explode(option, sep=',', chars=None):
    return [ chunk.strip(chars) for chunk in option.split(sep) ]


def which(name):
    found = None
    for path in os.getenv("PATH").split(os.path.pathsep):
        full_path = os.path.join(path,name)
        if os.path.exists(full_path):
            found = full_path
            break
    return found


def findFile(directory, search):
    found = None
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == search:
                found = os.path.join(root, file)
                break

        if not found:
            for dir in dirs:
                found = findFile(dir, search)
                if found:
                    break

    return found


def getOption(name, default, extra):
    if extra and name in extra:
        return extra[name]
    elif name in default:
        return default[name]
    else:
        return None


def stripAnsi(line):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)
