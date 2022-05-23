import os
import discord
from dotenv import load_dotenv
from cs1graphics import *

WIDTH = 1920
HEIGHT = 1080

canvas = Canvas(WIDTH, HEIGHT)
canvas.setTitle("🎆 EF 게임부스 실시간 랭킹!! 🎇")

load_dotenv()
f = open("config.txt")
TOKEN, GUILD = f.readline().split(",")
f.close()

client = discord.Client()

games = [[],[],[],[],[],[]]
game_names = ["다트", "양궁", "스피드컵", "링", "사격", "보물찾기"]

GOLD = (204, 156, 14)
SILVER = (211, 211, 211)
BRONZE = (176, 141, 87)
BLACK = (0, 0, 0)

def create_text(msg, font_size, x, y, justif, color = BLACK):
    text = Text("\n"+msg, font_size)
    text.moveTo(x, y-HEIGHT//40)
    text.setJustification(justif)
    text.setFontColor(color)
    return text 

def create_divisions():
    rect = Rectangle(w = WIDTH, h = 5)
    rect.moveTo(WIDTH//2, HEIGHT//2)
    rect.setFillColor((0, 0, 0))
    canvas.add(rect)

    for i in range(1, 4):
        rect = Rectangle(w = 5, h = HEIGHT)
        rect.moveTo(int(WIDTH*i//3), HEIGHT//2)
        rect.setFillColor((0, 0, 0))
        canvas.add(rect)    

def draw_background():
    global canvas, games, game_names
    for i in range(3):
        text = create_text(game_names[i], 25, WIDTH//6+WIDTH//3*i, HEIGHT // 25, 'center')
        canvas.add(text)

    for i in range(3, 6):
        text = create_text(game_names[i], 25, WIDTH//6+WIDTH//3*(i-3), HEIGHT//2 + HEIGHT // 25, 'center')
        canvas.add(text)

    create_divisions()

    for game in range(6):    
        y = HEIGHT // 10
        if game >= 3:
            y += HEIGHT // 2
            
        x = WIDTH//6 + WIDTH//3 * (game % 3)
        
        for i in range(5):
            if i == 0:
                text = create_text("%i등" % (i+1), 35, x-WIDTH//7, y, 'left', GOLD)
            elif i == 1:
                text = create_text("%i등" % (i+1), 35, x-WIDTH//7, y, 'left', SILVER)
            elif i == 2:
                text = create_text("%i등" % (i+1), 35, x-WIDTH//7, y, 'left', BRONZE)
            else:
                text = create_text("%i등" % (i+1), 35, x-WIDTH//7, y, 'left')
                
            canvas.add(text)            
            y += HEIGHT // 12

def update_game(game):
    global canvas, games, game_names
    draw_background()
    game_list = games[game]
    
    y = HEIGHT // 10
    if game >= 3:
        y += HEIGHT // 2
        
    x = WIDTH//6 + WIDTH//3 * (game % 3)
    
    for i in range(5):
        if i < len(game_list):
            score, village, name = game_list[i]
        else:
            continue


        if i == 0:
            COLOR = GOLD
        elif i == 1:
            COLOR = SILVER
        elif i == 2:
            COLOR = BRONZE
        else:
            COLOR = BLACK
        
        text = create_text(name, 35, x+WIDTH//40, y, 'center', COLOR)
        if game == 2:
            text2 = create_text(str(score)+"초", 35, x+WIDTH//9, y, 'center', COLOR)
        else:
            text2 = create_text(str(score)+"점", 35, x+WIDTH//9, y, 'center', COLOR)
        text3 = create_text(str(village)+"마을", 35, x-WIDTH//13, y, 'center', COLOR)
        ranktext = create_text("%i등" % (i+1), 35, x-WIDTH//7, y, 'center', COLOR)

        canvas.add(text)
        canvas.add(text2)
        canvas.add(text3)
        canvas.add(ranktext)
        
        y += HEIGHT // 12

def update():
    canvas.clear()
    for i in range(len(game_names)):
        update_game(i)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    

@client.event
async def on_message(message):
    # Prevent bot from responding to itself.
    if message.author == client.user:
        return
        
    response = message.content
    
    if response == "?":
        await message.channel.send("형식: 게임번호 마을 이름 점수")
        
    elif response == "현황":
        for i in range(len(game_names)):
            await message.channel.send("%s: %s" % (game_names[i], str(games[i])))
    
    elif "d" in response:
        try:
            _, game_id, rank = response.split()
            game_id = int(game_id)
            rank = int(rank)
            
            del games[game_id][rank-1]
            game_name = game_names[game_id]
            await message.channel.send("%s %i등 삭제 완료" % (game_name, rank))
            update()
        except:
            await message.channel.send("삭제 실패. 형식을 다시 확인하세요")
        
    else:
        game_id, village, name, score = response.split()
        
        game_id = int(game_id)
        village = int(village)
        if game_id == 2:
            score = float(score)
        else:
            score = int(score)

        game = games[game_id]
        game_name = game_names[game_id]

        game.append((score, village, name))
        game.sort()
        if game_id != 2:
            game.reverse()
        game = game[:5]

        if game_id == 2:
            await message.channel.send("%s 점수 업데이트 완료: %i마을 %s %.1f초" % (game_name, village, name, score))
        else:
            await message.channel.send("%s 점수 업데이트 완료: %i마을 %s %i점" % (game_name, village, name, score))
        
        update()

draw_background()
client.run(TOKEN)

