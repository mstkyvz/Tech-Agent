from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
from manim import *

class Solution(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang="tr"))
        self.step_1()
        self.step_2()
        self.step_3()
        self.step_4()
        self.step_5()


    def step_1(self):
        text1 = Tex(r"A(a, b) noktasının B(3, 0) noktasına göre simetriği C noktası olsun.").scale(0.8)
        with self.voiceover(text="A(a, b) noktasının B(3, 0) noktasına göre simetriği C noktası olsun.  Simetri noktası bulma formülünü kullanarak C noktasının koordinatlarını bulacağız.") as tracker:
            self.play(Create(text1))
            self.wait(3)
        self.play(FadeOut(text1))

    def step_2(self):
        text2 = MathTex(r"x = 2 \cdot 3 - a = 6 - a").scale(0.8).set_color(RED)
        text3 = MathTex(r"y = 2 \cdot 0 - b = -b").scale(0.8).set_color(GREEN)
        text4 = MathTex(r"C(6 - a, -b)").scale(0.8).set_color(BLUE)

        with self.voiceover(text="C noktasının koordinatları (x, y) ise, x eşittir 2 çarpı 3 eksi a, yani 6 eksi a. y eşittir 2 çarpı 0 eksi b, yani eksi b. Böylece C noktasının koordinatları (6 eksi a, eksi b) olur.") as tracker:
            self.play(Create(text2))
            self.wait(1)
            self.play(text2.animate.shift(UP))
            self.play(Create(text3))
            self.wait(1)
            self.play(text3.animate.shift(UP))
            self.play(Create(text4))
            self.wait(3)

        self.play(FadeOut(text2),FadeOut(text3),FadeOut(text4))


    def step_3(self):

        text5 = Tex(r"C noktasının y-eksenine göre simetriği D noktasıdır.").scale(0.8)
        text6 = MathTex(r"D(-(6 - a), -b) = (a - 6, -b)").scale(0.8).set_color(PINK)
        with self.voiceover(text="C noktasının y-eksenine göre simetriği D noktasıdır. D noktasının koordinatlarını bulmak için x koordinatının işaretini değiştiririz. Bu durumda D noktasının koordinatları (a eksi 6, eksi b) olur.") as tracker:
            self.play(Create(text5))
            self.wait(3)
            self.play(FadeOut(text5))
            self.play(Create(text6))
            self.wait(3)
        self.play(FadeOut(text6))



    def step_4(self):
        text7 = Tex(r"C ve D noktalarından geçen doğrunun denklemi y = -x - 1'dir.").scale(0.8)
        text8 = Tex(r"C ve D noktalarını denklemde yerine koyalım.").scale(0.8).set_color(PURPLE)
        with self.voiceover(text="C ve D noktalarından geçen doğrunun denklemi y eşittir eksi x eksi 1'dir. Şimdi C ve D noktalarının koordinatlarını bu denklemde yerine koyarak a ve b arasındaki ilişkiyi bulacağız.") as tracker:
             self.play(Create(text7))
             self.wait(1)
             self.play(text7.animate.shift(UP))
             self.play(Create(text8))
             self.wait(3)
        self.play(FadeOut(text7),FadeOut(text8))

    def step_5(self):
        text9 = MathTex(r"b = 7 - a").scale(0.8).set_color(RED)
        text10 = MathTex(r"b = a - 5").scale(0.8).set_color(GREEN)
        text11 = MathTex(r"a = 6").scale(0.8).set_color(BLUE)
        text12 = MathTex(r"b = 1").scale(0.8).set_color(PINK)
        text13 = MathTex(r"a + b = 7").scale(0.8).set_color(BLACK).set_color(YELLOW)


        with self.voiceover(text="C noktasını denklemde yerine koyarsak, b eşittir 7 eksi a bulunur. D noktasını denklemde yerine koyarsak, b eşittir a eksi 5 bulunur. Bu iki denklemi çözerek a eşittir 6 ve b eşittir 1 buluruz. Sonuç olarak a artı b eşittir 7 olur.  Cevap A şıkkıdır.") as tracker:
            self.play(Create(text9))
            self.wait(1)
            self.play(text9.animate.shift(UP))
            self.play(Create(text10))
            self.wait(1)
            self.play(text10.animate.shift(UP))
            self.play(Create(text11))
            self.wait(1)
            self.play(text11.animate.shift(UP))
            self.play(Create(text12))
            self.wait(1)
            self.play(text12.animate.shift(UP))
            self.play(Create(text13))

            self.wait(3)

