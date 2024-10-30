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
        text1 = Text("1. Soruyu Anlama", font_size=36).scale(0.8)
        text2 = Text("İki sayının toplamı isteniyor.", font_size=24).scale(0.8)
        text2.next_to(text1, DOWN)

        with self.voiceover(text="İlk adımda, soruyu anlamaya çalışıyoruz.  Soruda bize iki sayının toplamını bulmamız isteniyor. Bu adımda, ne yapmamız gerektiğini tam olarak belirliyoruz.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(2.5)
            self.play(FadeOut(text1), FadeOut(text2))

    def step_2(self):
        text1 = Text("2. Verileri Belirleme", font_size=36).scale(0.8)
        text2 = Text("Sayılar 2 ve 2'dir.", font_size=24).scale(0.8)
        text2.next_to(text1, DOWN)

        with self.voiceover(text="İkinci adımda, verileri belirliyoruz. Soruda bize verilen sayılar 2 ve 2'dir. Bu sayıları kullanarak toplama işlemini gerçekleştireceğiz.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(2.5)
            self.play(FadeOut(text1), FadeOut(text2))

    def step_3(self):
        text1 = Text("3. Formül Seçimi", font_size=36).scale(0.8)
        formula = MathTex("a + b = c").scale(0.8)
        text2 = Text("Toplama işlemi kullanılacak.", font_size=24).scale(0.8)
        text2.next_to(formula, DOWN)
        formula.next_to(text1, DOWN)


        with self.voiceover(text="Üçüncü adımda, kullanacağımız formülü seçiyoruz. Bu problemde, toplama işlemini kullanacağız. Formülümüz 'a + b = c' şeklindedir.  'a' ve 'b' toplanacak sayıları, 'c' ise toplamın sonucunu temsil eder.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(formula))
            self.play(Write(text2))
            self.wait(2.5)
            self.play(FadeOut(text1), FadeOut(formula), FadeOut(text2))

    def step_4(self):
        text1 = Text("4. Adım Adım Çözüm", font_size=36).scale(0.8)
        formula = MathTex("2 + 2 = 4").scale(0.8)
        formula.next_to(text1, DOWN)
        box = SurroundingRectangle(formula, color=YELLOW)

        with self.voiceover(text="Dördüncü adımda, adım adım çözüme geçiyoruz. 2 ve 2 sayılarını formülümüzde yerine koyuyoruz. 2 + 2 = 4.  Sonuç 4 olarak bulunur.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(formula))
            self.play(Create(box))
            self.wait(2.5)
            self.play(FadeOut(text1), FadeOut(formula), FadeOut(box))


    def step_5(self):
        text1 = Text("5. Sonuç", font_size=36).scale(0.8)
        text2 = Text("Sonuç 4'tür.", font_size=36, color=GREEN).scale(0.8)
        text2.next_to(text1, DOWN)

        with self.voiceover(text="Beşinci ve son adımda, sonucu yazıyoruz. 2 ile 2'nin toplamı 4'tür. İşlemimiz tamamlanmıştır.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(2.5)


