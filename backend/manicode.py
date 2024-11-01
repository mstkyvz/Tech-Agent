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
        baslik = Text("Aktivasyon Fonksiyonları: Sigmoid vs. ReLU", font_size=36, color=BLUE).scale(0.8)
        with self.voiceover(text="Merhaba! Bu videoda, yapay sinir ağlarında kullanılan iki önemli aktivasyon fonksiyonu olan Sigmoid ve ReLU arasındaki farkları inceleyeceğiz. Aktivasyon fonksiyonları, bir nöronun girdisini alıp bir çıktı üretmek için kullanılır. Bu çıktı, ağın bir sonraki katmanına iletilir.") as tracker:
            self.play(Write(baslik))
            self.wait(3)
        self.play(FadeOut(baslik))


    def step_2(self):
        sigmoid_formul = MathTex(r"f(x) = \frac{1}{1 + e^{-x}}", color=RED).scale(0.8)
        relu_formul = MathTex(r"f(x) = max(0, x)", color=GREEN).scale(0.8)

        with self.voiceover(text="İlk olarak, Sigmoid fonksiyonunu ele alalım. Sigmoid fonksiyonu, girdiyi 0 ile 1 arasında bir değere sıkıştırır. Formülü şu şekildedir:  1 bölü 1 artı e üzeri eksi x.  ReLU fonksiyonu ise negatif girdileri 0'a, pozitif girdileri ise kendilerine eşitler. Formülü, maksimum 0 ve x'dir.") as tracker:
            self.play(Write(sigmoid_formul))
            self.wait(3)
            self.play(sigmoid_formul.animate.shift(UP*2))
            self.play(Write(relu_formul))
            self.wait(3)
        self.play(FadeOut(sigmoid_formul), FadeOut(relu_formul))

    def step_3(self):
        sigmoid_grafik = FunctionGraph(lambda x: 1 / (1 + np.exp(-x)), x_range=[-5, 5], color=RED).scale(0.8)
        relu_grafik = FunctionGraph(lambda x: max(0, x), x_range=[-5, 5], color=GREEN).scale(0.8)
        
        with self.voiceover(text="Sigmoid fonksiyonunun grafiği, S şeklinde bir eğridir ve girdiler arttıkça 1'e, azaldıkça 0'a yaklaşır. ReLU fonksiyonunun grafiği ise, x ekseni boyunca 0'da sabittir ve pozitif x değerleri için doğrusal olarak artar.") as tracker:
            self.play(Create(sigmoid_grafik))
            self.wait(3)
            self.play(sigmoid_grafik.animate.shift(UP*2))
            self.play(Create(relu_grafik))
            self.wait(3)
        self.play(FadeOut(sigmoid_grafik), FadeOut(relu_grafik))


    def step_4(self):
        ornek1 = MathTex(r"\text{Sigmoid: } f(2) \approx 0.88, \ f(-1) \approx 0.27", color=PINK).scale(0.8)
        ornek2 = MathTex(r"\text{ReLU: } f(2) = 2, \ f(-1) = 0", color=PURPLE).scale(0.8)

        with self.voiceover(text="Örneklerle açıklayalım. Sigmoid fonksiyonunda, girdi 2 olduğunda çıktı yaklaşık 0.88, girdi -1 olduğunda ise yaklaşık 0.27'dir. ReLU fonksiyonunda ise, girdi 2 olduğunda çıktı 2, girdi -1 olduğunda ise çıktı 0'dır.") as tracker:
            self.play(Write(ornek1))
            self.wait(3)
            self.play(ornek1.animate.shift(UP*2))
            self.play(Write(ornek2))
            self.wait(3)
        self.play(FadeOut(ornek1), FadeOut(ornek2))


    def step_5(self):
        sonuc = Text("Sonuç:", font_size=36, color=BLACK).scale(0.8)
        aciklama = Text("ReLU, genellikle daha hızlı öğrenme sağlar.", font_size=24, color=BLUE).scale(0.8)


        with self.voiceover(text="Sonuç olarak, Sigmoid fonksiyonu olasılık tahmini için uygunken, ReLU genellikle daha hızlı öğrenme sağlar ve derin ağlarda kaybolan gradyan problemini azaltmada etkilidir.  Seçim, spesifik uygulamaya ve ağ mimarisine bağlıdır.") as tracker:
            self.play(Write(sonuc))
            self.wait(3)
            self.play(sonuc.animate.shift(UP*2))
            self.play(Write(aciklama))
            self.wait(3)


