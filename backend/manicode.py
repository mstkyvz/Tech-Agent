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
        text1 = Text("1. Adım: Soruyu Anlama", color=RED, font_size=36).scale(0.8)
        text2 = Text("İki sayının toplamı isteniyor.", color=BLUE, font_size=30).scale(0.8).next_to(text1, DOWN)

        with self.voiceover(text="İlk adımda, soruyu anlamaya çalışıyoruz. Bize verilen problemde iki sayının toplamını bulmamız isteniyor.") as tracker:
            self.play(Create(text1))
            self.wait(0.5)
            self.play(Create(text2))
            self.wait(2.5)
        self.play(FadeOut(text1), FadeOut(text2))


    def step_2(self):
        text1 = Text("2. Adım: Verileri Belirleme", color=GREEN, font_size=36).scale(0.8)
        text2 = Text("Sayılar 2 ve 2'dir.", color=PURPLE, font_size=30).scale(0.8).next_to(text1, DOWN)

        with self.voiceover(text="İkinci adımda, problemde verilen sayıları belirliyoruz. Bu problemde, toplamamız gereken sayılar 2 ve 2'dir.") as tracker:
            self.play(Create(text1))
            self.wait(0.5)
            self.play(Create(text2))
            self.wait(2.5)
        self.play(FadeOut(text1), FadeOut(text2))


    def step_3(self):
        text1 = Text("3. Adım: Formül Seçimi", color=BLUE, font_size=36).scale(0.8)
        formula = MathTex("a + b = c", color=PINK).scale(0.8).next_to(text1, DOWN)
        text2 = Text("Toplama işlemi kullanılacaktır.", color=BLACK, font_size=30).scale(0.8).next_to(formula, DOWN)

        with self.voiceover(text="Üçüncü adımda, problemi çözmek için kullanacağımız formülü seçiyoruz. Bu problem için toplama formülü 'a + b = c' kullanılacaktır.") as tracker:
            self.play(Create(text1))
            self.wait(0.5)
            self.play(Write(formula))
            self.wait(0.5)
            self.play(Create(text2))
            self.wait(1.5)
        self.play(FadeOut(text1), FadeOut(formula), FadeOut(text2))


    def step_4(self):
        text1 = Text("4. Adım: Adım Adım Çözüm", color=PINK, font_size=36).scale(0.8)
        solution = MathTex("2 + 2 = 4", color=RED).scale(0.8).next_to(text1, DOWN)


        with self.voiceover(text="Dördüncü adımda, belirlediğimiz formülü kullanarak adım adım çözüme ulaşıyoruz. 2 + 2 = 4 işlemi ile sonuca ulaşıyoruz.") as tracker:
            self.play(Create(text1))
            self.wait(0.5)
            self.play(Write(solution))
            self.wait(2.5)
        self.play(FadeOut(text1), FadeOut(solution))



    def step_5(self):
        text1 = Text("5. Adım: Sonuç", color=PURPLE, font_size=36).scale(0.8)
        result = MathTex(r"\underline{2 + 2 = 4}", color=GREEN).scale(0.8).next_to(text1, DOWN)

        with self.voiceover(text="Son adımda, bulduğumuz sonucu değerlendiriyoruz. 2 ile 2'nin toplamı 4'tür. İşlem tamamlanmıştır.") as tracker:
            self.play(Create(text1))
            self.wait(0.5)
            self.play(Write(result))
            self.wait(2.5)

