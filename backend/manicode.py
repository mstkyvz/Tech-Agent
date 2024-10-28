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
        text1 = MathTex(r"f(x) = 3\ln(x^2 - 1) + 2\ln(x^3 - 1) - 5\ln(x - 1)").scale(0.8)
        text2 = MathTex(r"\lim_{x \to 1^+} e^{f(x)}").scale(0.8)
        text1.shift(2*UP)
        text2.shift(UP)

        with self.voiceover(text="Soruda bize bir f(x) fonksiyonu verilmiş ve x, 1'e sağdan yaklaşırken e üzeri f(x) ifadesinin limitinin ne olduğu soruluyor. ") as tracker:
            self.play(Write(text1))
            self.play(Write(text2))
            self.wait(3)
        self.play(FadeOut(text1, text2))

    def step_2(self):
        text = MathTex(r"f(x) = \ln(x^2 - 1)^3 + \ln(x^3 - 1)^2 - \ln(x - 1)^5").scale(0.8)
        
        with self.voiceover(text="İlk adımda logaritma özelliklerinden faydalanarak ifadeyi sadeleştirelim. Logaritma özelliğine göre, bir logaritmanın önündeki katsayı logaritmanın içine kuvvet olarak girebilir.") as tracker:
            self.play(Write(text))
            self.wait(3)
        self.play(FadeOut(text))

    def step_3(self):
        text1 = MathTex(r"f(x) = \ln[(x^2 - 1)^3 * (x^3 - 1)^2] - \ln(x - 1)^5").scale(0.7)
        text2 = MathTex(r"f(x) = \ln\frac{(x^2 - 1)^3 * (x^3 - 1)^2}{(x - 1)^5}").scale(0.7)

        with self.voiceover(text="Logaritma özelliğine göre, toplama durumunda olan logaritmalar çarpım durumunda logaritma içine, çıkarma durumunda olan logaritmalar ise bölüm durumunda logaritma içine alınabilir.") as tracker:
            self.play(Write(text1))
            self.wait(3)
            self.play(Transform(text1, text2))
            self.wait(3)
        self.play(FadeOut(text1))
        
    def step_4(self):
        text1 = MathTex(r"f(x) = \ln\frac{((x+1)(x-1))^3 * ((x-1)(x^2+x+1))^2}{(x - 1)^5}").scale(0.6)
        text2 = MathTex(r"f(x) = \ln\frac{(x+1)^3(x-1)^3 * (x-1)^2(x^2+x+1)^2}{(x - 1)^5}").scale(0.6)
        text3 = MathTex(r"f(x) = \ln[(x+1)^3 (x^2+x+1)^2]").scale(0.6)

        with self.voiceover(text="Logaritma içindeki ifadeyi çarpanlarına ayıralım. (x kare - 1) ifadesi (x+1) çarpı (x-1) olarak; (x küp - 1) ifadesi ise (x-1) çarpı (x kare + x + 1) olarak çarpanlarına ayrılabilir.") as tracker:
            self.play(Write(text1))
            self.wait(3)
            self.play(Transform(text1, text2))
            self.wait(3)
            self.play(Transform(text1, text3))
            self.wait(3)
        self.play(FadeOut(text1))

    def step_5(self):
        text1 = MathTex(r"\lim_{x \to 1^+} e^{f(x)} =  e^{\ln[(1+1)^3 (1^2+1+1)^2]}").scale(0.6)
        text2 = MathTex(r"\lim_{x \to 1^+} e^{f(x)} =  e^{\ln(8 * 9)}").scale(0.6)
        text3 = MathTex(r"\lim_{x \to 1^+} e^{f(x)} =  e^{\ln(72)}").scale(0.6)
        text4 = MathTex(r"\lim_{x \to 1^+} e^{f(x)} = 72").scale(0.6)


        with self.voiceover(text="Son olarak, sadeleştirilmiş ifadede x yerine 1 yazarak limiti hesaplayabiliriz. Sonuç olarak limitimiz 72 olarak bulunur.") as tracker:
            self.play(Write(text1))
            self.wait(3)
            self.play(Transform(text1, text2))
            self.wait(3)
            self.play(Transform(text1, text3))
            self.wait(3)
            self.play(Transform(text1, text4))
            self.wait(3)
        self.play(FadeOut(text1))

