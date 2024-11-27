import logging
from manim import *
import itertools
import math
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class TSPAnimation(Scene):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        
        self.cities = [(2, 3), (3, 7), (6, 8), (8, 5), (7, 2)]

    def euclidean_distance(self, city1, city2):
        """Calcula a distância euclidiana entre duas cidades."""
        distance = math.sqrt((city1[0] - city2[0]) * 2 + (city1[1] - city2[1]) * 2)
        logger.debug(f"Distância entre {city1} e {city2}: {distance}")
        return distance

    def calculate_total_distance(self, route):
        """Calcula a distância total de uma rota."""
        distance = sum(self.euclidean_distance(route[i], route[(i + 1) % len(route)]) for i in range(len(route)))
        logger.debug(f"Distância total para a rota {route}: {distance}")
        return distance

    def brute_force_tsp_parallel(self):
        """Calcula a melhor rota em paralelo, mostrando as distâncias em tempo real."""
        best_route, min_distance = None, float('inf')
        all_results = []

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.calculate_total_distance, perm): perm for perm in itertools.permutations(self.cities)}
            for future in as_completed(futures):
                perm = futures[future]
                current_distance = future.result()
                all_results.append((perm, current_distance))

                if current_distance < min_distance:
                    min_distance = current_distance
                    best_route = perm
                    logger.debug(f"Nova melhor rota: {best_route} com distância {min_distance:.2f}")

        return best_route, min_distance, all_results

    def display_city_points(self):
        """Desenha as cidades na tela com labels."""
        points = [Dot(np.array([x - 5, y - 5, 0]), color=BLUE) for x, y in self.cities]
        city_labels = []

        for i, point in enumerate(points):
            self.play(Create(point), run_time=0.5)
            label = Text(f"Cidade {i+1}", font_size=24).next_to(point, DOWN)
            city_labels.append(label)
            self.play(Write(label), run_time=0.5)

        return points, city_labels

    def display_route(self, perm, distance, color=BLUE, show_distance=True):
        """Desenha a rota entre as cidades com setas e mostra as distâncias."""
        route_points = [Dot(np.array([x - 5, y - 5, 0])) for x, y in perm]
        lines = []
        distance_texts = []
        order_labels = []

        for i in range(len(route_points)):
            start = route_points[i].get_center()
            end = route_points[(i + 1) % len(route_points)].get_center()
            line = Line(start, end, color=color, stroke_width=2).add_tip(tip_length=0.2)
            lines.append(line)
            
            if show_distance:
                dist = self.euclidean_distance(perm[i], perm[(i + 1) % len(route_points)])
                distance_text = Text(f"{dist:.2f}", font_size=24).move_to(line.get_center())
                distance_texts.append(distance_text)

            order_label = Text(f"{i+1}", font_size=24, color=WHITE).move_to(route_points[i].get_center() + UP * 0.3)
            order_labels.append(order_label)

        self.play(*[Create(line) for line in lines], *[Write(text) for text in distance_texts], *[Write(label) for label in order_labels], run_time=1)
        route_info = Text(f"Rota: {perm}, Distância Total: {distance:.2f}", font_size=24, color=WHITE).to_edge(DOWN)
        self.play(Write(route_info))
        self.wait(1)
        self.remove(route_info, *lines, *distance_texts, *order_labels)

    def display_best_route(self, best_route, min_distance):
        """Desenha a melhor rota encontrada."""
        best_points = [Dot(np.array([x - 5, y - 5, 0]), color=YELLOW) for x, y in best_route]
        lines = []
        distance_texts = []
        order_labels = []

        for i in range(len(best_points)):
            start = best_points[i].get_center()
            end = best_points[(i + 1) % len(best_points)].get_center()
            line = Line(start, end, color=YELLOW, stroke_width=2).add_tip(tip_length=0.2)
            lines.append(line)
            
            # Exibir a distância (peso) entre as cidades
            dist = self.euclidean_distance(best_route[i], best_route[(i + 1) % len(best_points)])
            distance_text = Text(f"{dist:.2f}", font_size=24).move_to(line.get_center())
            distance_texts.append(distance_text)

            # Adicionar label de ordem de visitação
            order_label = Text(f"{i+1}", font_size=24, color=WHITE).move_to(best_points[i].get_center() + UP * 0.3)
            order_labels.append(order_label)

        self.play(*[Create(line) for line in lines], *[Write(text) for text in distance_texts], *[Write(label) for label in order_labels])
        final_distance_text = Text(f"Distância total ótima: {min_distance:.2f}", font_size=28, color=WHITE).to_edge(UP)
        self.play(Write(final_distance_text))
        self.wait(1)

    def construct(self):
        """Constrói a cena de animação."""
        logger.debug("Iniciando animação das cidades e rotas...")
        city_points, city_labels = self.display_city_points()
        best_route, min_distance, all_results = self.brute_force_tsp_parallel()

        # Animação de cada rota calculada
        for perm, distance in all_results:
            self.display_route(perm, distance, color=BLUE, show_distance=True)

        # Animação da melhor rota encontrada
        logger.debug("Desenhando a melhor rota encontrada...")
        self.display_best_route(best_route, min_distance)

        # Texto final sobre a melhor rota encontrada
        final_text = Text("Esta é a melhor rota encontrada!", font_size=24, color=WHITE)
        self.play(Write(final_text))
        self.wait(2)
