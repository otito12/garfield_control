GARFIELD_CMDS = {
    "move_to_base": {
        "phrase": set(["post","orange","go","move","to","base","origin","pose"]),
        "pose": {
        "l_hip": {"angle": 50,"time":600},
        "l_knee":{"angle":61 , "time":600 },
        "l_calf":{"angle": 60, "time":600 },
        "r_hip":{"angle": 37, "time":600 },
        "r_knee":{"angle": 1, "time":600 },
        "r_calf":{"angle": 175, "time":600 }
    }
    },
    "move_to_ready": {
        "phrase": set(["post","already","go","move","to","ready","pose"]),
        "pose": {
        "l_hip": {"angle": 50,"time":600},
        "l_knee":{"angle":13.9 , "time":600 },
        "l_calf":{"angle": 8, "time":600 },
        "r_hip":{"angle": 36, "time":600 },
        "r_knee":{"angle": 46, "time":600 },
        "r_calf":{"angle": 228, "time":600 }
        }
    },
    "mic_check": {
        "phrase": set(["can","you","hear","me"])
        }
}

def _get_highest_phrase(token_cmd):
    apply_cmd = None
    max_phrase_percent = 0
    for key in GARFIELD_CMDS.keys():
        # what percentage of my phrase is inside the command?
        # return the phrase with the highest precentage
        phrase_perc = len(GARFIELD_CMDS[key]["phrase"].intersection(token_cmd)) / len(GARFIELD_CMDS[key]["phrase"])
        if  phrase_perc > max_phrase_percent:
            max_phrase_percent = phrase_perc
            apply_cmd = key   
    return apply_cmd

def _apply_pose(garfield,apply_cmd):
    garfield.l_hip.move(GARFIELD_CMDS[apply_cmd]["pose"]["l_hip"]["angle"],
                            time=GARFIELD_CMDS[apply_cmd]["pose"]["l_hip"]["time"])

    garfield.l_knee.move(GARFIELD_CMDS[apply_cmd]["pose"]["l_knee"]["angle"],
                        time=GARFIELD_CMDS[apply_cmd]["pose"]["l_knee"]["time"])

    garfield.l_calf.move(GARFIELD_CMDS[apply_cmd]["pose"]["l_calf"]["angle"],
                        time=GARFIELD_CMDS[apply_cmd]["pose"]["l_calf"]["time"])

    garfield.r_hip.move(GARFIELD_CMDS[apply_cmd]["pose"]["r_hip"]["angle"],
                        time=GARFIELD_CMDS[apply_cmd]["pose"]["r_hip"]["time"])

    garfield.r_knee.move(GARFIELD_CMDS[apply_cmd]["pose"]["r_knee"]["angle"],
                        time=GARFIELD_CMDS[apply_cmd]["pose"]["r_knee"]["time"])

    garfield.r_calf.move(GARFIELD_CMDS[apply_cmd]["pose"]["r_calf"]["angle"],
                        time=GARFIELD_CMDS[apply_cmd]["pose"]["r_calf"]["time"])

def speech_to_command(garfield, cmd):
    apply_cmd = _get_highest_phrase(set(cmd.split(' ')) )
    print("I will be applying:",apply_cmd)
    print(cmd)
    if apply_cmd == "move_to_base":
        _apply_pose(garfield,apply_cmd)
    elif apply_cmd == "move_to_ready":
        _apply_pose(garfield,apply_cmd)
    elif apply_cmd == "mic_check":
        garfield.speak("I can hear you")
    else:
        garfield.speak("I do not recognize that command")
    
    
    




