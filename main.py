import pygame
import pgzrun
import random
WIDTH = 800
HEIGHT= 600
TITLE ="meu jogo"
pontos = 0
pontos_vitoria = 100
vidas = 3
estado_jogo ="jogando"
RAIO_DE_VIZAO_QD = 180**2
rota_patrulha = [(100,100), (600,100)]
indice_rota = 0
VELOCIDADE_inimigo_PATRULHA = 1.5
VELOCIDADE_inimigo_PEERSEGUICAO  =  1.5
estado_inimigo = "patrulha"


heroi = Actor("heroi")
heroi.pos = (400,400)
moeda = Actor("moeda", (400, 300))
inimigo = Actor("caval",(700, 500))


def reiniciar_jogo():
    global estado_jogo, estado_inimigo, indice_rota
    estado_jogo = "jogando"
    estado_inimigo = "patrulha"
    indice_rota = 0
    heroi.pos = (100, 500)
    inimigo.pos =(400, 100)

def draw():
    global pontos
    global vidas
    global estado_jogo, estado_inimigo
    if estado_jogo == "jogando":
        screen.fill((0, 0, 225))
        heroi.draw()
        moeda.draw()
        inimigo.draw()
        screen.draw.text(f"pontos: {pontos}/{pontos_vitoria}", topleft=(20, 20), fontsize=32, color="pink", shadow=(1, 1), scolor="black")
        screen.draw.text(f"vidas: {vidas}/{vidas}", topleft=(40, 40), fontsize=32, color="pink", shadow=(1, 1), scolor="black")
        if estado_inimigo == "perseguicao":
            cor_vizao = (255, 50, 50)
        else:
            cor_vizao =(100 ,100 ,255)
        screen.draw.circle(inimigo.pos, 180, cor_vizao)
        if estado_inimigo =="perseguicao":
            status_alerta = "alerta: inimigo te viu"
        else:
            status_alerta = "status: oculto"
        screen.draw.text(status_alerta, midbottom=(WIDTH // 2, HEIGHT - 15), fontsize=22, color="crimson" if estado_inimigo == "perseguicao" else "lime")
    elif estado_jogo == "vitoria":
        screen.draw.text("escapou", center=(WIDTH // 2,250), fontsize=50, color="lightgreen", shadow=(2,2), scolor= "black")
        screen.draw.text("precione [R] para jogar novamente",center=(WIDTH // 2,350),fontsize= 26, color="yellow")
    elif estado_jogo =="GAMEOVER":
        screen.draw.text("game over", center=(WIDTH // 2, 220), fontsize=64, color="red", shadow=(2,2), scolor="black")



def update():
    global pontos, vidas, estado_jogo
    if keyboard.right:
        heroi.x = heroi.x +1
    if keyboard.left:
        heroi.x = heroi.x -1
    if keyboard.up:
        heroi.y = heroi.y -1
    if keyboard.down:
        heroi.y = heroi.y +1

    if  heroi.colliderect(moeda):
        moeda.x = random.randint(50, WIDTH - 50)
        moeda.y = random.randint(50, HEIGHT - 50)
        pontos = pontos +1

        if estado_jogo in ["vitoria", "gameover"]:
            if keyboard.r:
                reiniciar_jogo()
                return
    



    atualizar_ia_inimigo()


    
    if heroi.colliderect(inimigo):
        vidas = vidas -1 
        if vidas <=0:
            estado_jogo = "GAMEOVER"
            
        else:
            inimigo.x =random.choice([60, WIDTH -60])
            inimigo.y =random.choice([60, WIDTH -60])

def atualizar_ia_inimigo():
    global estado_inimigo, indice_rota, estado_jogo
    dx = heroi.x - inimigo.x
    dy = heroi.y - inimigo.y
    distancia_qd = dx**2 + dy**2

    if distancia_qd <= RAIO_DE_VIZAO_QD:
        estado_inimigo = "perseguicao"
    else:
        estado_inimigo = "patrulha"
    
    if estado_inimigo == "perseguicao":
        if inimigo.x < heroi.x : inimigo.x += VELOCIDADE_inimigo_PEERSEGUICAO
        elif inimigo.x > heroi.x : inimigo.x -= VELOCIDADE_inimigo_PEERSEGUICAO

        if inimigo.y > heroi.y: inimigo.y -= VELOCIDADE_inimigo_PEERSEGUICAO
        if inimigo.y < heroi.y: inimigo.y += VELOCIDADE_inimigo_PEERSEGUICAO

    elif estado_inimigo == "patrulha":
        alvo_x, alvo_y  = rota_patrulha[indice_rota]
        if inimigo.x < alvo_x: inimigo.x += VELOCIDADE_inimigo_PATRULHA
        elif inimigo.x > alvo_x: inimigo.x -= VELOCIDADE_inimigo_PATRULHA

        if inimigo.y > alvo_y: inimigo.y -= VELOCIDADE_inimigo_PATRULHA
        if inimigo.y < alvo_y: inimigo.y += VELOCIDADE_inimigo_PATRULHA 

        if abs(inimigo.x - alvo_x) <5 and abs (inimigo.y - alvo_y) < 5:
            indice_rota = (indice_rota + 1) % len (rota_patrulha)









pgzrun.go()