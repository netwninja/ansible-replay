import time
from colorama import Fore, Back, Style
import re

colors = {'ok': 'GREEN', 'changed': 'YELLOW', 'unreachable': 'RED', 'failed': 'RED', 'other': 'WHITE'}

host_timer = 0.5

def itemcolor(items):
    result_colors = {'other': 'WHITE'}
    for item in items:
        if "=" in item:
            name, number = item.split('=')
            if int(number) == 0:
                result_colors[name] = 'WHITE'
            else:
                result_colors[name] = colors[name]
    if result_colors['failed'] == 'RED':
        result_colors['other'] = 'RED'
    elif result_colors['unreachable'] == 'RED':
        result_colors['other'] = 'RED'
    elif result_colors['changed'] == 'YELLOW':
        result_colors['other'] = 'YELLOW'
    elif result_colors['ok'] == 'GREEN':
        result_colors['other'] = 'GREEN'

    return result_colors


with open('sample.log', 'r') as ansible_log:
    out_file = ansible_log.readlines()

play_recap = False

for line in out_file:
    line = line.strip()
    if not play_recap:
        if 'ok:' in line:
            time.sleep(host_timer)
            print(Fore.GREEN + line)
        elif 'fatal:' in line:
            time.sleep(host_timer)
            print (Fore.RED + line)
        elif 'changed:' in line:
            time.sleep(host_timer)
            print (Fore.YELLOW + line)
        elif 'skipping:' in line:
            time.sleep(host_timer)
            print (Fore.BLUE + line)
        elif 'included:' in line:
            time.sleep(host_timer)
            print (Fore.BLUE + line)
        elif 'TASK' in line:
            print (Fore.WHITE + line)
            time.sleep(0.5)
            raw_input('')
        elif 'PLAY RECAP' in line:
            print (Fore.WHITE + line)
            play_recap = True
            time.sleep(0.5)
            raw_input('')
        else:
            time.sleep(0.5)
            print (line)
    else:
        try:
            lines = line.split()
            _, sp1, sp2, sp3, sp4, sp5, _ = re.split("\S+", line)
            colors_dict = itemcolor(lines)

            print ("{}{}{}{}{}{}{}{}{}{}{}".format(getattr(Fore, colors_dict['other']) + lines[0], sp1,
                                                   getattr(Fore, colors_dict['other']) + lines[1], sp2,
                                                   getattr(Fore, colors_dict['ok']) + lines[2], sp3,
                                                   getattr(Fore, colors_dict['changed']) + lines[3], sp5,
                                                   getattr(Fore, colors_dict['unreachable']) + lines[4], sp5,
                                                   getattr(Fore, colors_dict['failed']) + lines[5]))
        except:
            pass