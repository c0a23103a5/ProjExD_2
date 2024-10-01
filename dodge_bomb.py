import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5), 
    pg.K_DOWN:(0, 5), 
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
    }

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:  pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん,または,爆弾のRect
    戻り値：真理値タプル（横判定結果, 縦判定結果）
    画面外ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen: pg.display):
    """
    引数：スクリーンオブジェクト
    スクリーンにゲームオーバー画面を表示する関数
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(255//2)
    font_ = pg.font.Font(None, 80)
    txt = font_.render("Game Over", True, (255, 255, 255))
    k_img = pg.image.load("fig/8.png")
    k_rct = k_img.get_rect()
    k_rct.center = 300, 200
    screen.blit(go_img, (0, 0))
    screen.blit(txt, [WIDTH//2, HEIGHT//2])
    screen.blit(k_img, k_rct)
    pg.display.update()
    time.sleep(5)


def change_bomb():
    """
    爆弾の速度と大きさのリストをまとめたタプルを返す関数
    """
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    
    return accs, bb_imgs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    #bb_rct.centerx = random.randint(0, WIDTH)
    #bb_rct.centery = random.randint(HEIGHT, 0)
    
    vx, vy = +5, +5  # 爆弾の速度
    
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])  # 背景描画
        if kk_rct.colliderect(bb_rct):
            #こうかとんと重なっていたらmain関数から脱出
            game_over(screen)
            return
            #print("GAME OVER")
            

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # (横移動量, 縦移動量)
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横移動量
                sum_mv[1] += tpl[1]  # 縦移動量
        kk_rct.move_ip(sum_mv)  # こうかとんの移動
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-(sum_mv[0]), -(sum_mv[1]))  # 端の処理（こうかとん）
        
        bb_accs, bb_imgs = change_bomb()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))

        bb_rct.move_ip((avx, avy))  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        screen.blit(kk_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
