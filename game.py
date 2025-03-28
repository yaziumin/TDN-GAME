import pyxel
SCREEN_WIDTH=160
SCREEN_HEIGHT=120
Gendai_INTERVAL=2
GAME_OVER_DISPLAY_TIME=60
START_SCENE="start"
PLAY_SCENE="play"
#現代アート先輩はリストの要素のため、以下が必要となる
class Gendai:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self):
        if self.y<SCREEN_HEIGHT:
            self.y+=5
    def draw(self):
        #左から描画するx座標y座標画像バンク番号画像座標画像の幅高さ消す色
        pyxel.blt(self.x,self.y,0,8,0,8,8,pyxel.COLOR_BLACK)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH,SCREEN_HEIGHT,title="ただのゲーム")
        pyxel.load("my_resource.pyxres")
        self.jp_font=pyxel.Font("umplus_j10r.bdf")
        pyxel.playm(0,loop=True)
        self.current_scene=START_SCENE
        self.countdown_timer = 30 * 30
        self.is_game_clear = False
        pyxel.run(self.update,self.draw)
    def reset_play_scene(self):
        self.senpai_x=SCREEN_WIDTH//2-5
        self.senpai_y=SCREEN_HEIGHT*4//5
        self.Gendais=[]
        self.is_collision=False
        self.game_over_dislay_timer=GAME_OVER_DISPLAY_TIME
        self.countdown_timer = 30 * 30
        self.is_game_clear = False
        
    def update_start_scene(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.reset_play_scene()
            self.current_scene=PLAY_SCENE

    def update_play_scene(self):
        #ゲームオーバー時
        if self.is_collision:
            if self.game_over_dislay_timer>0:
                self.game_over_dislay_timer-=1
            else:
                self.current_scene=START_SCENE

            return
        # カウントダウンの更新
        if self.countdown_timer > 0:
            self.countdown_timer -= 1
        else:
            self.is_game_clear = True
            #game overじゃないけど（名前は間違えてるけど）操作はあってる
            if self.game_over_dislay_timer > 0:
                self.game_over_dislay_timer -= 1
            else:
                self.current_scene = START_SCENE
            return

        #先輩の移動
        if pyxel.btn(pyxel.KEY_RIGHT)and self.senpai_x<SCREEN_WIDTH-18:
            self.senpai_x+=3
        elif pyxel.btn(pyxel.KEY_RIGHT)and SCREEN_WIDTH-18<=self.senpai_x<=SCREEN_WIDTH-16:
            self.senpai_x=144
        if pyxel.btn(pyxel.KEY_LEFT)and self.senpai_x>2:
            self.senpai_x-=3
        elif pyxel.btn(pyxel.KEY_LEFT)and 0<=self.senpai_x<=2:
            self.senpai_x=0
        if pyxel.btn(pyxel.KEY_UP)and self.senpai_x<SCREEN_WIDTH-21:
            self.senpai_x+=6
        elif pyxel.btn(pyxel.KEY_UP)and SCREEN_WIDTH-21<=self.senpai_x<=SCREEN_WIDTH-16:
            self.senpai_x=144
        if pyxel.btn(pyxel.KEY_DOWN)and self.senpai_x>5:
            self.senpai_x-=6
        elif pyxel.btn(pyxel.KEY_DOWN)and 0<=self.senpai_x<=5:
            self.senpai_x=0
        
        #現代の追加
        if pyxel.frame_count%Gendai_INTERVAL==0:
            self.Gendais.append(Gendai(pyxel.rndi(0,SCREEN_WIDTH-8),0))
        #現代アートの落下
        for gendai in self.Gendais.copy():
            gendai.update()
            #衝突
            if (self.senpai_x<=gendai.x<=self.senpai_x+8 and
                self.senpai_y<=gendai.y<=self.senpai_y+8):
                self.is_collision=True
            #画面外に出た現代を削除
            if gendai.y>=SCREEN_HEIGHT:
                self.Gendais.remove(gendai)

    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if self.current_scene==START_SCENE:
            self.update_start_scene()
        elif self.current_scene==PLAY_SCENE:
            self.update_play_scene()
    def draw_start_scene(self):
        pyxel.blt(0,0,0,32,0,160,120)
        pyxel.text(10,10,
                   "「30秒よけ続けろ！」",pyxel.COLOR_RED,self.jp_font)
        pyxel.text(SCREEN_WIDTH//10,SCREEN_HEIGHT-20,
                   "★space:スタート",pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(SCREEN_WIDTH//10,SCREEN_HEIGHT-40,
                   "★escキー：終了",pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(SCREEN_WIDTH//10,SCREEN_HEIGHT-60,
                   "☆上下矢印キー:高速移動",pyxel.COLOR_BLACK,self.jp_font)
        pyxel.text(SCREEN_WIDTH//10,SCREEN_HEIGHT-80,
                   "☆左右矢印キー:移動",pyxel.COLOR_BLACK,self.jp_font)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        #現代アート
        for gendai in self.Gendais:
            gendai.draw()
        #先輩
        pyxel.blt(self.senpai_x,self.senpai_y,0,16,0,16,16,pyxel.COLOR_YELLOW)
         # カウントダウンの描画
        pyxel.text(SCREEN_WIDTH-20, 5, f"{self.countdown_timer // 30}", pyxel.COLOR_WHITE, self.jp_font)
        # ゲームオーバー時の描画
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH//2-30,SCREEN_HEIGHT//2-10,
                       "ゲイ夢 Over",pyxel.COLOR_BLACK,self.jp_font)

        # ゲームクリア時の描画
        if self.is_game_clear:
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 10,
                       "ゲイ夢 clear!", pyxel.COLOR_YELLOW, self.jp_font)
            
    def draw(self):
        if self.current_scene==START_SCENE:
            self.draw_start_scene()
        elif self.current_scene==PLAY_SCENE:
            self.draw_play_scene()
        

App()  