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
        text1 = MathTex(r"A(3,4)", color=RED).scale(0.8)
        text2 = MathTex(r"m_1 \cdot m_2 = -1", color=GREEN).scale(0.8)
        text3 = MathTex(r"m_1 + m_2 = \frac{3}{2}", color=BLUE).scale(0.8)

        text1.shift(UP*2)
        text2.next_to(text1, DOWN)
        text3.next_to(text2, DOWN)

        with self.voiceover(text="A noktası (3,4) koordinatlarında veriliyor. İki doğru dik kesiştiği için eğimleri çarpımı -1'e eşittir. Ayrıca, eğimleri toplamı 3/2 olarak verilmiştir.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(0.5)
            self.play(Write(text3))
            self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3))
        

    def step_2(self):
        text1 = MathTex(r"\text{Doğru 1: } y - 4 = m_1(x - 3)", color=PINK).scale(0.8)
        text2 = MathTex(r"y = m_1x - 3m_1 + 4", color=PURPLE).scale(0.8)
        text1.shift(UP)
        text2.next_to(text1, DOWN)
        with self.voiceover(text="İlk doğrunun denklemini, verilen A(3,4) noktasını ve m1 eğimini kullanarak yazalım. Nokta eğim formülünden y - 4 = m1 çarpı (x - 3) olur. Düzenlersek, y = m1x - 3m1 + 4 elde ederiz.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2))


    def step_3(self):
        text1 = MathTex(r"x-\text{kesişim noktası: } y = 0", color=RED).scale(0.8)
        text2 = MathTex(r"0 = m_1x - 3m_1 + 4", color=GREEN).scale(0.8)
        text3 = MathTex(r"x = \frac{3m_1 - 4}{m_1} = 3 - \frac{4}{m_1}", color=BLUE).scale(0.8)
        text4 = MathTex(r"B(3 - \frac{4}{m_1}, 0)", color=PINK).scale(0.8)
        text1.shift(UP*1.5)
        text2.next_to(text1, DOWN)
        text3.next_to(text2, DOWN)
        text4.next_to(text3, DOWN)

        with self.voiceover(text="x-kesişim noktasını bulmak için y=0 koyarız. 0 = m1x - 3m1 + 4 denklemini çözersek, x = (3m1 - 4) / m1 = 3 - 4/m1 bulunur.  Böylece B noktasının koordinatları (3 - 4/m1, 0) olur.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(0.5)
            self.play(Write(text3))
            self.wait(0.5)
            self.play(Write(text4))
            self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), FadeOut(text4))
    

    def step_4(self):
        text1 = MathTex(r"\text{Benzer şekilde, C noktası için:}", color=RED).scale(0.8).shift(UP)
        text2 = MathTex(r"C(3 - \frac{4}{m_2}, 0)", color=GREEN).scale(0.8)
        text2.next_to(text1, DOWN)
        with self.voiceover(text="Benzer şekilde, ikinci doğru için aynı adımları izleyerek C noktasının koordinatlarını (3 - 4/m2, 0) olarak buluruz.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2))

    def step_5(self):
        text1 = MathTex(r"|BC| = |(3 - \frac{4}{m_1}) - (3 - \frac{4}{m_2})| = |\frac{4}{m_2} - \frac{4}{m_1}|", color=BLUE).scale(0.8)
        text2 = MathTex(r"= |4(\frac{m_1 - m_2}{m_1m_2})| = 4|m_2 - m_1| \text{ (çünkü } m_1m_2 = -1)", color=PURPLE).scale(0.8)
        text3 = MathTex(r"\text{Alan(ABC)} = \frac{1}{2} \cdot |BC| \cdot 4 = 2|BC| = 8|m_2 - m_1|", color=BLACK).scale(0.8)
        text4 = MathTex(r"|m_2 - m_1| = \sqrt{(m_1 + m_2)^2 - 4m_1m_2} = \sqrt{(\frac{3}{2})^2 - 4(-1)} = \frac{5}{2}", color=RED).scale(0.8)
        text5 = MathTex(r"\text{Alan(ABC)} = 8 \cdot \frac{5}{2} = 20", color=GREEN).scale(0.8)

        text1.shift(UP*2)
        text2.next_to(text1, DOWN)
        text3.next_to(text2, DOWN)
        text4.next_to(text3, DOWN)
        text5.next_to(text4, DOWN)


        with self.voiceover(text="BC uzunluğunu, B ve C noktalarının x koordinatlarının farkının mutlak değeri olarak buluruz.  Bu da |4/m2 - 4/m1| olur.  m1m2 = -1 olduğundan, bu ifade 4|m2 - m1|'e eşittir.  ABC üçgeninin alanı, taban çarpı yükseklik bölü 2'dir. Taban |BC| ve yükseklik 4 olduğundan, alan 2|BC| = 8|m2 - m1|'dir.  |m2 - m1|'i bulmak için (m2 - m1)² = (m1 + m2)² - 4m1m2 özdeşliğini kullanırız.  Buradan |m2 - m1| = 5/2 bulunur.  Sonuç olarak, alan 8 * 5/2 = 20'dir.") as tracker:
            self.play(Write(text1))
            self.wait(0.5)
            self.play(Write(text2))
            self.wait(0.5)
            self.play(Write(text3))
            self.wait(0.5)
            self.play(Write(text4))
            self.wait(0.5)
            self.play(Write(text5))
            self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), FadeOut(text4), FadeOut(text5))


