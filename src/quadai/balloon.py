"""
Main game file with three simulations:
Sim-1: Human, PID, SAC(v2_5000000), DQN
Sim-2: Human, PID, SAC1(v1_3330000), SAC2(v2_5000000) - no DQN, but two SAC variants
Sim-3: Like Sim-1 but bigger arena and more targets

Results are stored in results.xlsx with:
Columns: Simulation, TimeChosen, PID, SAC, DQN, Human
SAC variants combined with commas for Sim-2 if multiple SAC.

Sim-1 shows sun/clouds, Sim-2 and Sim-3 do not.
Sim-2 and Sim-3 have more spread out target generation.
"""

import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from random import randrange
from math import sin, cos, pi, sqrt
import numpy as np
import pygame
from pygame.locals import *
import pandas as pd

from quadai.player import HumanPlayer, PIDPlayer, SACPlayer, DQNPlayer


def correct_path(current_path):
    return os.path.join(os.path.dirname(__file__), current_path)


def show_menu(screen, WIDTH, HEIGHT):
    pygame.font.init()
    menu_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 30)
    info_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Regular.ttf"), 20)

    options = [100, 200, 250]
    selected_option = None

    while True:
        pygame.event.pump()
        top_color = (131, 176, 181)
        bottom_color = (100, 140, 150)
        for y in range(HEIGHT):
            alpha = y / HEIGHT
            r = int(top_color[0]*(1 - alpha) + bottom_color[0]*alpha)
            g = int(top_color[1]*(1 - alpha) + bottom_color[1]*alpha)
            b = int(top_color[2]*(1 - alpha) + bottom_color[2]*alpha)
            pygame.draw.line(screen,(r,g,b),(0,y),(WIDTH,y))

        title_text = menu_font.render("Choose Simulation Time:", True, (255, 255, 255))
        screen.blit(title_text,(WIDTH/2 - title_text.get_width()/2, HEIGHT/2 - 100))

        for i, opt in enumerate(options):
            opt_text = info_font.render(str(opt) + " seconds", True, (255, 255, 255))
            screen.blit(opt_text,(WIDTH/2 - opt_text.get_width()/2, HEIGHT/2 - 20 + i*40))

        inst_text = info_font.render("Use UP/DOWN to select, ENTER to confirm, ESC to quit",True,(255,255,255))
        screen.blit(inst_text,(WIDTH/2 - inst_text.get_width()/2, HEIGHT/2 + 100))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if selected_option is None:
                        selected_option = 0
                    else:
                        selected_option = (selected_option - 1) % len(options)
                elif event.key == K_DOWN:
                    if selected_option is None:
                        selected_option = 0
                    else:
                        selected_option = (selected_option + 1) % len(options)
                elif event.key == K_RETURN:
                    if selected_option is not None:
                        return options[selected_option]
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    exit()

        if selected_option is not None:
            arrow_font = info_font
            arrow_text = arrow_font.render("->", True, (255, 255, 255))
            screen.blit(arrow_text,(WIDTH/2 - 100 - arrow_text.get_width()/2, HEIGHT/2 - 20 + selected_option*40))

        pygame.display.update()


def balloon(sim_mode="sim1"):
    if sim_mode == "sim1":
        WIDTH, HEIGHT = 800, 800
        targets_count = 100
        players = [
            HumanPlayer(),
            PIDPlayer(),
            SACPlayer(model_path="models/sac_model_v2_5000000_steps.zip", name="SAC"),
            DQNPlayer()
        ]
        sim_name = "Sim-1"
        sim_description = "This simulation tests four drones: Human, PID, SAC, DQN. A baseline scenario."

        sun = pygame.image.load(correct_path("assets/balloon-flat-asset-pack/png/background-elements/sun.png"))
        sun.set_alpha(124)
        cloud1 = pygame.image.load(correct_path("assets/balloon-flat-asset-pack/png/background-elements/cloud-1.png"))
        cloud1.set_alpha(124)
        cloud2 = pygame.image.load(correct_path("assets/balloon-flat-asset-pack/png/background-elements/cloud-2.png"))
        cloud2.set_alpha(124)
        x_cloud1, y_cloud1, speed_cloud1 = (150, 200, 0.3)
        x_cloud2, y_cloud2, speed_cloud2 = (400, 500, -0.2)

    elif sim_mode == "sim2":
        WIDTH, HEIGHT = 900, 900
        targets_count = 200
        players = [
            HumanPlayer(),
            PIDPlayer(),
            SACPlayer(model_path="models/sac_model_v1_3330000_steps.zip", name="SAC1"),
            SACPlayer(model_path="models/sac_model_v2_5000000_steps.zip", name="SAC2")
        ]
        sim_name = "Sim-2"
        sim_description = "This simulation compares Manual, PID, and two SAC variants in a larger arena."
        sun = cloud1 = cloud2 = None
        x_cloud1 = y_cloud1 = speed_cloud1 = 0
        x_cloud2 = y_cloud2 = speed_cloud2 = 0

    elif sim_mode == "sim3":
        WIDTH, HEIGHT = 950, 950
        targets_count = 150
        players = [
            HumanPlayer(),
            PIDPlayer(),
            SACPlayer(model_path="models/sac_model_v2_5000000_steps.zip", name="SAC"),
            DQNPlayer()
        ]
        sim_name = "Sim-3"
        sim_description = "This simulation is like Sim-1 but with a bigger arena and more targets."
        sun = cloud1 = cloud2 = None
        x_cloud1 = y_cloud1 = speed_cloud1 = 0
        x_cloud2 = y_cloud2 = speed_cloud2 = 0

    else:
        WIDTH, HEIGHT = 800, 800
        targets_count = 100
        players = [
            HumanPlayer(),
            PIDPlayer(),
            SACPlayer(model_path="models/sac_model_v2_5000000_steps.zip", name="SAC"),
            DQNPlayer()
        ]
        sim_name = "Sim-1"
        sim_description = "This simulation tests four drones: Human, PID, SAC, DQN. A baseline scenario."
        sun = pygame.image.load(correct_path("assets/balloon-flat-asset-pack/png/background-elements/sun.png"))
        sun.set_alpha(124)
        cloud1 = pygame.image.load(correct_path("assets/balloon-flat-asset-pack/png/background-elements/cloud-1.png"))
        cloud1.set_alpha(124)
        cloud2 = pygame.image.load(correct_path("assets/balloon-flat-asset-pack/png/background-elements/cloud-2.png"))
        cloud2.set_alpha(124)
        x_cloud1, y_cloud1, speed_cloud1 = (150, 200, 0.3)
        x_cloud2, y_cloud2, speed_cloud2 = (400, 500, -0.2)

    FPS = 60
    gravity = 0.08
    mass = 1
    arm = 25

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    time_limit = show_menu(screen, WIDTH, HEIGHT)

    player_width = 80
    player_animation_speed = 0.3
    player_animation = []
    for i in range(1, 5):
        image = pygame.image.load(correct_path(os.path.join("assets/balloon-flat-asset-pack/png/objects/drone-sprites","drone-"+str(i)+".png")))
        image.convert()
        player_animation.append(pygame.transform.scale(image, (player_width, int(player_width*0.30))))

    target_width = 30
    target_animation_speed = 0.1
    target_animation = []
    for i in range(1, 8):
        image = pygame.image.load(correct_path(os.path.join("assets/balloon-flat-asset-pack/png/balloon-sprites/red-plain","red-plain-"+str(i)+".png")))
        image.convert()
        target_animation.append(pygame.transform.scale(image,(target_width,int(target_width*1.73))))

    name_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 20)
    name_hud_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 15)
    time_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 30)
    score_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Regular.ttf"), 20)
    respawn_timer_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Bold.ttf"), 90)
    respawning_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Regular.ttf"), 15)
    sim_info_font = pygame.font.Font(correct_path("assets/fonts/Roboto-Regular.ttf"), 18)

    def display_info(position, player):
        name_text = name_font.render(player.name, True, (255,255,255))
        screen.blit(name_text,(position,100))
        target_text = score_font.render("Score: "+str(player.target_counter),True,(255,255,255))
        screen.blit(target_text,(position,125))
        if player.dead:
            respawning_text = respawning_font.render("Respawning...",True,(255,255,255))
            screen.blit(respawning_text,(position,150))

    # More randomization for sim2 and sim3
    if sim_mode == "sim2" or sim_mode == "sim3":
        left_margin = 50
        right_margin = 50
        top_margin = 50
        bottom_margin = 50
        targets = []
        for i in range(targets_count):
            x_pos = randrange(left_margin, WIDTH - right_margin)
            y_pos = randrange(top_margin, HEIGHT - bottom_margin)
            targets.append((x_pos, y_pos))
    else:
        # sim1 default
        targets = []
        for i in range(targets_count):
            targets.append((randrange(200, WIDTH-200), randrange(200, HEIGHT-200)))

    FramePerSec=pygame.time.Clock()
    time=0
    step=0
    respawn_timer_max=3
    running=True
    game_over=False
    results_saved=False

    while running:
        for event in pygame.event.get():
            if event.type==QUIT:
                running=False

        if game_over:
            screen.fill((0,0,0))
            final_title = time_font.render("Simulation Over!", True, (255,255,255))
            screen.blit(final_title,(WIDTH/2-final_title.get_width()/2,HEIGHT/2-150))

            score_y = HEIGHT/2-50
            pid_score=""
            sac_score=""
            dqn_score=""
            human_score=""
            sac_variants=[]

            scores=[(p.name,p.target_counter)for p in players]
            for p_name,p_score_val in scores:
                p_score_line=score_font.render(f"{p_name} collected: {p_score_val}",True,(255,255,255))
                screen.blit(p_score_line,(WIDTH/2-p_score_line.get_width()/2,score_y))
                score_y+=40
                if p_name=="PID": pid_score=str(p_score_val)
                elif p_name=="Human": human_score=str(p_score_val)
                elif p_name=="DQN": dqn_score=str(p_score_val)
                elif p_name.startswith("SAC"):
                    sac_variants.append(f"{p_name}={p_score_val}")

            if len(sac_variants)>0:
                sac_score=",".join(sac_variants)

            saved_msg="Results saved to results.xlsx"
            saved_text=score_font.render(saved_msg,True,(255,255,255))
            screen.blit(saved_text,(WIDTH/2-saved_text.get_width()/2,score_y+40))

            close_text=score_font.render("Close the window to exit.",True,(255,255,255))
            screen.blit(close_text,(WIDTH/2-close_text.get_width()/2,score_y+80))
            pygame.display.update()
            FramePerSec.tick(FPS)

            if not results_saved:
                result_row={
                    "Simulation": sim_name,
                    "TimeChosen": str(time_limit),
                    "PID": pid_score,
                    "SAC": sac_score,
                    "DQN": dqn_score,
                    "Human": human_score
                }
                results_df=pd.DataFrame([result_row])
                excel_path=os.path.join(os.path.dirname(__file__),"../../","results.xlsx")
                if not os.path.exists(excel_path):
                    with pd.ExcelWriter(excel_path,engine="openpyxl")as writer:
                        results_df.to_excel(writer,sheet_name="Results",index=False)
                else:
                    existing_df=pd.read_excel(excel_path,sheet_name="Results")
                    combined_df=pd.concat([existing_df,results_df],ignore_index=True)
                    with pd.ExcelWriter(excel_path,engine="openpyxl",mode='w')as writer:
                        combined_df.to_excel(writer,sheet_name="Results",index=False)

                results_saved = True
            continue

        top_color=(131,176,181)
        bottom_color=(100,140,150)
        for y in range(HEIGHT):
            alpha=y/HEIGHT
            r=int(top_color[0]*(1-alpha)+bottom_color[0]*alpha)
            g=int(top_color[1]*(1-alpha)+bottom_color[1]*alpha)
            b=int(top_color[2]*(1-alpha)+bottom_color[2]*alpha)
            pygame.draw.line(screen,(r,g,b),(0,y),(WIDTH,y))

        sim_name_text=name_font.render(sim_name,True,(255,255,255))
        screen.blit(sim_name_text,(20,20))
        line_surface=sim_info_font.render(sim_description,True,(255,255,255))
        screen.blit(line_surface,(20,50))

        time+=1/60
        step+=1

        time_text_surf=time_font.render("Time: "+str(int(time_limit-time)),True,(255,255,255))
        screen.blit(time_text_surf,(WIDTH-time_text_surf.get_width()-20,20))

        if sim_mode == "sim1":
            x_cloud1 += speed_cloud1
            if x_cloud1 > WIDTH:
                x_cloud1 = -cloud1.get_width()
            screen.blit(cloud1, (x_cloud1, y_cloud1))

            x_cloud2 += speed_cloud2
            if x_cloud2 < -cloud2.get_width():
                x_cloud2 = WIDTH
            screen.blit(cloud2, (x_cloud2, y_cloud2))

            screen.blit(sun, (WIDTH-170, -50))

        for player_index,player in enumerate(players):
            if not player.dead:
                if player.target_counter<len(targets):
                    dist=sqrt((player.x_position-targets[player.target_counter][0])**2+(player.y_position-targets[player.target_counter][1])**2)
                else:
                    dist=0

                if player.name=="PID":
                    error_x=(targets[player.target_counter][0]-player.x_position) if player.target_counter<len(targets)else 0
                    error_y=(targets[player.target_counter][1]-player.y_position) if player.target_counter<len(targets)else 0
                    obs=[error_x,player.x_speed,error_y,player.y_speed,player.angle,player.angular_speed]
                    thruster_left,thruster_right=player.act(obs)

                elif player.name.startswith("SAC")or player.name=="DQN":
                    angle_to_up=player.angle/180*pi
                    velocity=sqrt(player.x_speed**2+player.y_speed**2)
                    angle_velocity=player.angular_speed
                    if player.target_counter<len(targets):
                        distance_to_target=dist/500
                        angle_to_target=np.arctan2(targets[player.target_counter][1]-player.y_position,targets[player.target_counter][0]-player.x_position)
                    else:
                        distance_to_target=0
                        angle_to_target=0
                    angle_target_and_velocity=angle_to_target-np.arctan2(player.y_speed,player.x_speed)
                    obs_7=np.array([angle_to_up,velocity,angle_velocity,distance_to_target,angle_to_target,angle_target_and_velocity,distance_to_target],dtype=np.float32)
                    thruster_left,thruster_right=player.act(obs_7)
                else:
                    thruster_left,thruster_right=player.act([])

                player.x_acceleration=0
                player.y_acceleration=gravity
                player.angular_acceleration=0

                player.x_acceleration+=(-(thruster_left+thruster_right)*sin(player.angle*pi/180)/mass)
                player.y_acceleration+=(-(thruster_left+thruster_right)*cos(player.angle*pi/180)/mass)
                player.angular_acceleration+=(arm*(thruster_right-thruster_left)/mass)

                player.x_speed+=player.x_acceleration
                player.y_speed+=player.y_acceleration
                player.angular_speed+=player.angular_acceleration

                player.x_position+=player.x_speed
                player.y_position+=player.y_speed
                player.angle+=player.angular_speed

                if player.target_counter<len(targets):
                    dist=sqrt((player.x_position-targets[player.target_counter][0])**2+(player.y_position-targets[player.target_counter][1])**2)
                    if dist<50:
                        player.target_counter+=1
                        if player.target_counter>=len(targets):
                            game_over=True
                    elif dist>1000:
                        player.dead=True
                        player.respawn_timer=respawn_timer_max

            else:
                if player.name=="Human":
                    respawn_text=respawn_timer_font.render(str(int(player.respawn_timer)+1),True,(255,255,255))
                    respawn_text.set_alpha(124)
                    screen.blit(respawn_text,(WIDTH/2-respawn_text.get_width()/2,HEIGHT/2-respawn_text.get_height()/2))

                player.respawn_timer-=1/60
                if player.respawn_timer<0:
                    player.dead=False
                    (player.angle,player.angular_speed,player.angular_acceleration)=(0,0,0)
                    (player.x_position,player.x_speed,player.x_acceleration)=(WIDTH/2,0,0)
                    (player.y_position,player.y_speed,player.y_acceleration)=(HEIGHT/2,0,0)

            if not game_over and player.target_counter<len(targets):
                target_sprite=target_animation[int(step*target_animation_speed)%len(target_animation)]
                target_sprite.set_alpha(player.alpha)
                screen.blit(target_sprite,(targets[player.target_counter][0]-int(target_sprite.get_width()/2),targets[player.target_counter][1]-int(target_sprite.get_height()/2)))

            player_sprite=player_animation[int(step*player_animation_speed)%len(player_animation)]
            player_copy=pygame.transform.rotate(player_sprite,player.angle)
            player_copy.set_alpha(player.alpha)
            screen.blit(player_copy,(player.x_position-int(player_copy.get_width()/2),player.y_position-int(player_copy.get_height()/2)))

            name_hud_text=name_hud_font.render(player.name,True,(255,255,255))
            screen.blit(name_hud_text,(player.x_position-int(name_hud_text.get_width()/2),player.y_position-40-int(name_hud_text.get_height()/2)))

        info_x_start=20
        for i,p in enumerate(players):
            display_info(info_x_start+i*120,p)

        if time>time_limit:
            game_over=True

        pygame.display.update()
        FramePerSec.tick(FPS)

    pygame.quit()
