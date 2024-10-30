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
        text = "Problemimiz, A(3,4) noktasında dik kesişen iki doğrunun eğimleri toplamı 3/2 olarak verilmiş. Bu doğruların x eksenini kestiği noktalar B ve C. ABC üçgeninin alanını bulmamız gerekiyor."
        with self.voiceover(text=text) as tracker:
            problem = Tex(r"A(3,4) noktasında dik kesişen iki doğru \\ $m_1 + m_2 = \frac{3}{2}$, x-kesen noktaları B ve C. \\ ABC üçgeninin alanı nedir?").scale(0.8)
            self.play(Create(problem))
            self.wait(3)
        self.play(FadeOut(problem))


    def step_2(self):
        text = "İki doğrumuz l1 ve l2 olsun. Eğimleri m1 ve m2. Doğrular dik kesiştikleri için m1 * m2 = -1. Ayrıca m1 + m2 = 3/2 verilmiş."
        with self.voiceover(text=text) as tracker:
            eq1 = MathTex(r"m_1 \cdot m_2 = -1").scale(0.8)
            eq2 = MathTex(r"m_1 + m_2 = \frac{3}{2}").scale(0.8)
            self.play(Create(eq1))
            self.wait(3)
            self.play(eq1.animate.shift(UP))
            self.play(Create(eq2))
            self.wait(3)
        self.play(FadeOut(eq1), FadeOut(eq2))


    def step_3(self):
        text = "l1 doğrusunun denklemi y-4 = m1(x-3). x eksenini kestiği nokta B'yi bulmak için y=0 koyalım. Buradan x = 3 - 4/m1. Yani B noktası (3 - 4/m1, 0). Benzer şekilde l2 için C noktası (3 - 4/m2, 0)."

        with self.voiceover(text=text) as tracker:
            l1_eq = MathTex(r"l_1: y - 4 = m_1(x - 3)").scale(0.8)
            b_point = MathTex(r"B = (3 - \frac{4}{m_1}, 0)").scale(0.8)
            c_point = MathTex(r"C = (3 - \frac{4}{m_2}, 0)").scale(0.8)

            self.play(Create(l1_eq))
            self.wait(3)
            self.play(l1_eq.animate.shift(UP))
            self.play(Create(b_point))
            self.wait(3)
            self.play(b_point.animate.shift(UP))
            self.play(Create(c_point))
            self.wait(3)
        self.play(FadeOut(l1_eq), FadeOut(b_point), FadeOut(c_point))



    def step_4(self):
        text = "Üçgenin tabanı BC'nin uzunluğu |(3 - 4/m1) - (3 - 4/m2)| = 4|m1 - m2|/|m1*m2|. m1*m2 = -1 olduğundan BC = 4|m1 - m2|. Üçgenin yüksekliği A noktasının y koordinatı olan 4. ABC üçgeninin alanı 1/2 * BC * 4 = 8|m1 - m2|."

        with self.voiceover(text=text) as tracker:
            bc_length = MathTex(r"BC = 4|m_1 - m_2|").scale(0.8)
            area = MathTex(r"Alan = 8|m_1 - m_2|").scale(0.8)

            self.play(Create(bc_length))
            self.wait(3)
            self.play(bc_length.animate.shift(UP))
            self.play(Create(area))
            self.wait(3)
        self.play(FadeOut(bc_length), FadeOut(area))




    def step_5(self):
        text = "(m1-m2)^2 = (m1+m2)^2 - 4m1m2 = (3/2)^2 - 4(-1) = 25/4. Buradan |m1-m2| = 5/2. ABC üçgeninin alanı 8 * (5/2) = 20."

        with self.voiceover(text=text) as tracker:
            m_diff_sq = MathTex(r"(m_1 - m_2)^2 = \frac{25}{4}").scale(0.8)
            m_diff = MathTex(r"|m_1 - m_2| = \frac{5}{2}").scale(0.8)
            final_area = MathTex(r"Alan = 20").scale(0.8).set_color(YELLOW)
            
            self.play(Create(m_diff_sq))
            self.wait(3)
            self.play(m_diff_sq.animate.shift(UP))
            self.play(Create(m_diff))
            self.wait(3)
            self.play(m_diff.animate.shift(UP))
            self.play(Create(final_area))
            self.wait(3)

            rect = SurroundingRectangle(final_area, color=YELLOW)
            self.play(Create(rect))
            self.wait(3)

        self.play(FadeOut(m_diff_sq), FadeOut(m_diff), FadeOut(final_area), FadeOut(rect))

