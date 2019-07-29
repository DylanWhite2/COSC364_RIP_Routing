#!/bin/bash

# Example Network
gnome-terminal --window --geometry 85x14+0+0 --title 'Router 1' -- bash -c 'python3 main.py config/router-1.json'
sleep 0.5
gnome-terminal --window --geometry 85x14+700+0 --title 'Router 2' -- bash -c 'python3 main.py config/router-2.json'
sleep 0.5
gnome-terminal --window --geometry 85x14+0+265 --title 'Router 3' -- bash -c 'python3 main.py config/router-3.json'
sleep 0.5
gnome-terminal --window --geometry 85x14+700+265 --title 'Router 4' -- bash -c 'python3 main.py config/router-4.json'
sleep 0.5
gnome-terminal --window --geometry 85x14+0+530 --title 'Router 5' -- bash -c 'python3 main.py config/router-5.json'
sleep 0.5
gnome-terminal --window --geometry 85x14+700+530 --title 'Router 6' -- bash -c 'python3 main.py config/router-6.json'
sleep 0.5
gnome-terminal --window --geometry 85x14+0+795 --title 'Router 7' -- bash -c 'python3 main.py config/router-7.json'
gnome-terminal --window --geometry 85x14+700+795 --title 'CPU Usage' -- bash -c 'sar 1 1000'

#Simple Split Horizon Poison Reverse Test
# gnome-terminal --window --geometry 85x14+0+0 --title 'Router 8' -- bash -c 'python3 main.py config/router-8.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+700+0 --title 'Router 9' -- bash -c 'python3 main.py config/router-9.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+0+265 --title 'Router 10' -- bash -c 'python3 main.py config/router-10.json'


#Minimum Hop Test
# gnome-terminal --window --geometry 85x14+0+0 --title 'Router 1' -- bash -c 'python3 main.py config_2/router-1.json'
#sleep 0.5
# gnome-terminal --window --geometry 85x14+700+0 --title 'Router 2' -- bash -c 'python3 main.py config_2/router-2.json'
#sleep 0.5
# gnome-terminal --window --geometry 85x14+0+265 --title 'Router 3' -- bash -c 'python3 main.py config_2/router-3.json'
#sleep 0.5
# gnome-terminal --window --geometry 85x14+700+265 --title 'Router 4' -- bash -c 'python3 main.py config_2/router-4.json'
#sleep 0.5
# gnome-terminal --window -geometry 85x14+0+530 --title 'Router 5' -- bash -c 'python3 main.py config_2/router-5.json'
#sleep 0.5
# gnome-terminal --window --geometry 85x14+700+530 --title 'Router 6' -- bash -c 'python3 main.py config_2/router-6.json'
#sleep 0.5
# gnome-terminal --window --title 'Router 7' -- bash -c 'python3 main.py config_2/router-7.json'


# Network Example From Routing Notes
# gnome-terminal --window --geometry 85x14+0+0 --title 'Router 1' -- bash -c 'python3 main.py config_3/router-1.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+700+0 --title 'Router 2' -- bash -c 'python3 main.py config_3/router-2.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+0+265 --title 'Router 3' -- bash -c 'python3 main.py config_3/router-3.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+700+265 --title 'Router 4' -- bash -c 'python3 main.py config_3/router-4.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+0+530 --title 'Router 5' -- bash -c 'python3 main.py config_3/router-5.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+700+530 --title 'Router 6' -- bash -c 'python3 main.py config_3/router-6.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+0+795 --title 'Router 7' -- bash -c 'python3 main.py config_3/router-7.json'
# sleep 0.5
# gnome-terminal --window --geometry 85x14+700+795 --title 'Router 8' -- bash -c 'python3 main.py config_3/router-8.json'
# gnome-terminal --window --geometry 85x14+2000+795 --title 'CPU Usage' -- bash -c 'sar 1 1000'
