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
        title = Text("Problem", font_size=0.5).to_edge(UL).set_color(BLUE)
        problem_statement_1 = Tex(r"Bir basketbol topu 2.40 m'lik bir yükseklikten, yatayla 35°'lik bir açıyla ve 12 m/s'lik bir ilk hızla atılıyor.", font_size=30).next_to(title, DOWN, buff=0.2).scale(0.8)
        problem_statement_2 = Tex(r"(a) Basketbol potasının yüksekliği 3.05 m ise, oyuncunun potadan ne kadar uzakta olduğunu bulun.", font_size=30).next_to(problem_statement_1, DOWN, buff=0.1).scale(0.8)
        problem_statement_3 = Tex(r"(b) Topun potaya giriş açısı nedir?", font_size=30).next_to(problem_statement_2, DOWN, buff=0.1).scale(0.8)

        with self.voiceover(text="Bu problemde, yatay olarak atılan bir basketbol topunun hareketini inceleyerek oyuncunun potadan ne kadar uzakta olduğunu ve topun potaya giriş açısını bulacağız.") as tracker:
            self.play(Write(title))
            self.wait(1)
            self.play(Write(problem_statement_1))
            self.wait(3)
            self.play(Write(problem_statement_2))
            self.wait(3)
            self.play(Write(problem_statement_3))
            self.wait(3)
            self.play(FadeOut(title, problem_statement_1, problem_statement_2, problem_statement_3))
            self.wait(1)

    def step_2(self):
        title = Text("1. Adım: Verileri Belirleme", font_size=0.5).to_edge(UL).set_color(BLUE)
        
        verilenler = VGroup(
            Tex(r"İlk hız ($v_0$): 12 m/s"),
            Tex(r"Atış açısı ($\theta$): 35°"),
            Tex(r"İlk yükseklik ($y_0$): 2.40 m"),
            Tex(r"Pota yüksekliği ($y$): 3.05 m")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.8)

        with self.voiceover(text="Öncelikle, problemde verilenleri belirleyelim. Topun ilk hızı 12 metre/saniye, atış açısı yatayla 35 derece ve ilk yüksekliği 2.40 metredir. Pota yüksekliği ise 3.05 metre olarak verilmiştir.") as tracker:
            self.play(Write(title))
            self.wait(1)
            for veri in verilenler:
                self.play(Write(veri))
                self.wait(1)
            self.wait(2)
            self.play(FadeOut(title, *verilenler))
            self.wait(1)

    def step_3(self):
        title = Text("2. Adım: Yatay ve Düşey Hız Bileşenlerini Bulma", font_size=0.5).to_edge(UL).set_color(BLUE)
        explanation = Text("İlk hızı yatay ve düşey bileşenlerine ayırmamız gerekiyor:", font_size=30).next_to(title, DOWN, buff=0.2).scale(0.8)
        horizontal_velocity = MathTex(r"v_{0x} = v_0 \cos(\theta) = 12 \cos(35°) \approx 9.83 \ m/s").next_to(explanation, DOWN, buff=0.2).scale(0.8)
        vertical_velocity = MathTex(r"v_{0y} = v_0 \sin(\theta) = 12 \sin(35°) \approx 6.88 \ m/s").next_to(horizontal_velocity, DOWN, buff=0.2).scale(0.8)

        with self.voiceover(text="Topun hareketi iki boyutta gerçekleştiği için, ilk hızı yatay ve düşey bileşenlerine ayırmamız gerekiyor. Yatay hız bileşeni, ilk hızın kosinüs 35 derece ile çarpımına eşittir ve yaklaşık olarak 9.83 metre/saniyedir. Düşey hız bileşeni ise, ilk hızın sinüs 35 derece ile çarpımına eşittir ve yaklaşık olarak 6.88 metre/saniyedir.") as tracker:
            self.play(Write(title))
            self.wait(1)
            self.play(Write(explanation))
            self.wait(3)
            self.play(Write(horizontal_velocity))
            self.wait(3)
            self.play(Write(vertical_velocity))
            self.wait(3)
            self.play(FadeOut(title, explanation, horizontal_velocity, vertical_velocity))
            self.wait(1)

    def step_4(self):
        title = Text("3. Adım: Topun Havada Kalma Süresini Bulma", font_size=0.5).to_edge(UL).set_color(BLUE)
        explanation_1 = Text("Topun potaya ulaşması için geçen süreyi bulmak için düşey hareketi kullanacağız.", font_size=30).next_to(title, DOWN, buff=0.2).scale(0.8)
        formula = MathTex(r"y = y_0 + v_{0y}t + \frac{1}{2}gt^2").next_to(explanation_1, DOWN, buff=0.2).scale(0.8)
        explanation_2 = Text("Bu formülde:", font_size=30).next_to(formula, DOWN, buff=0.2).scale(0.8)
        variables = VGroup(
            Tex(r"$y$, topun son yüksekliği (3.05 m)"),
            Tex(r"$y_0$, topun ilk yüksekliği (2.40 m)"),
            Tex(r"$v_{0y}$, topun ilk düşey hızı (6.88 m/s)"),
            Tex(r"$t$, geçen süre (bulunacak)"),
            Tex(r"$g$, yerçekimi ivmesi (-9.8 m/s²)")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(explanation_2, DOWN, buff=0.2).scale(0.8)

        with self.voiceover(text="Topun potaya ulaşması için geçen süreyi bulmak için düşey hareketi kullanacağız. Bunun için, serbest düşme hareketinin denklemini kullanabiliriz. Denklemimiz y eşittir y sıfır artı v sıfır y çarpı t artı 1/2 çarpı g çarpı t kare. Bu formülde, y topun son yüksekliği yani 3.05 metre, y sıfır topun ilk yüksekliği yani 2.40 metre, v sıfır y topun ilk düşey hızı yani 6.88 metre/saniye, t geçen süre yani bizim bulmak istediğimiz değer ve g yerçekimi ivmesi yani -9.8 metre/saniye karedir.") as tracker:
            self.play(Write(title))
            self.wait(1)
            self.play(Write(explanation_1))
            self.wait(3)
            self.play(Write(formula))
            self.wait(3)
            self.play(Write(explanation_2))
            self.wait(3)
            for variable in variables:
                self.play(Write(variable))
                self.wait(2)
            self.wait(2)
            self.play(FadeOut(title, explanation_1, formula, explanation_2, *variables))
            self.wait(1)

    def step_5(self):
        title = Text("4. Adım: Yatay Mesafeyi Bulma", font_size=0.5).to_edge(UL).set_color(BLUE)
        explanation = Text("Yatay mesafeyi (x) bulmak için:", font_size=30).next_to(title, DOWN, buff=0.2).scale(0.8)
        formula = MathTex(r"x = v_{0x}t").next_to(explanation, DOWN, buff=0.2).scale(0.8)
        reminder = Text("Burada 't' 3. adımda bulduğumuz süredir.", font_size=30).next_to(formula, DOWN, buff=0.2).scale(0.8)

        with self.voiceover(text="Son adımda ise, topun havada kalma süresini kullanarak yatay mesafeyi bulabiliriz. Yatay mesafe, yatay hız çarpı zaman formülü ile hesaplanır. Formülümüz x eşittir v sıfır x çarpı t. Burada t, bir önceki adımda bulduğumuz havada kalma süresidir. Hesalamayı tamamladığımızda, oyuncunun potadan olan uzaklığını yani x'i bulmuş olacağız.") as tracker:
            self.play(Write(title))
            self.wait(1)
            self.play(Write(explanation))
            self.wait(3)
            self.play(Write(formula))
            self.wait(3)
            self.play(Write(reminder))
            self.wait(3)
            self.play(FadeOut(title, explanation, formula, reminder))
            self.wait(1)
