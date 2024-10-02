import numpy as np
import pygame
import math

class Cubo:
    def __init__(self):
        # Vértices do cubo
        self.vertices = np.array([
            [-1, -1, -1],
            [-1, -1,  1],
            [-1,  1, -1],
            [-1,  1,  1],
            [ 1, -1, -1],
            [ 1, -1,  1],
            [ 1,  1, -1],
            [ 1,  1,  1]
        ])

        # Definir as arestas do cubo
        self.arestas = [(0, 1), (1, 3), (3, 2), (2, 0),
                        (4, 5), (5, 7), (7, 6), (6, 4),
                        (0, 4), (1, 5), (2, 6), (3, 7)]

        # Ângulos de rotação para cada eixo
        self.angulo_x = 0
        self.angulo_y = 0
        self.angulo_z = 0

        # Velocidades de rotação para cada eixo
        self.velocidade_x = 0.01
        self.velocidade_y = 0.01
        self.velocidade_z = 0.01

        # Translação inicial: move o cubo para longe da tela no eixo Z
        self.translacao = np.array([0, 0, -8])  # Afastar o cubo no eixo Z

    def rotation_matrix_x(self, theta):
        return np.array([
            [1, 0, 0],
            [0, np.cos(theta), -np.sin(theta)],
            [0, np.sin(theta), np.cos(theta)]
        ])

    def rotation_matrix_y(self, theta):
        return np.array([
            [np.cos(theta), 0, np.sin(theta)],
            [0, 1, 0],
            [-np.sin(theta), 0, np.cos(theta)]
        ])

    def rotation_matrix_z(self, theta):
        return np.array([
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])

    def projection(self, ponto):
        # Projeção em perspectiva
        d = 2  # Distância da câmera
        z = ponto[2] if ponto[2] != 0 else 0.001  # Evitar divisão por zero

        fator_escala = d / (d + z)  # Fator de escala de acordo com a profundidade
        x_proj = ponto[0] * fator_escala
        y_proj = ponto[1] * fator_escala
        return np.array([x_proj, y_proj])

    def apply_transformations(self, ponto):
        # Aplicar rotações em cada eixo
        rotacionado = np.dot(self.rotation_matrix_x(self.angulo_x), ponto)
        rotacionado = np.dot(self.rotation_matrix_y(self.angulo_y), rotacionado)
        rotacionado = np.dot(self.rotation_matrix_z(self.angulo_z), rotacionado)

        # Aplicar translação (mover o cubo para longe no eixo Z)
        transladado = rotacionado + self.translacao
        return transladado

    def run(self):
        # Iniciar Pygame
        pygame.init()
        tela = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Cubo 3D com Controle de Velocidade")

        relogio = pygame.time.Clock()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Controle de teclas para ajustar a velocidade da rotação
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_RIGHT]:
                self.velocidade_x += 0.001  # Aumentar rotação em todos os eixos
                self.velocidade_y += 0.001
                self.velocidade_z += 0.001
            if teclas[pygame.K_LEFT]:
                self.velocidade_x -= 0.001  # Diminuir rotação em todos os eixos
                self.velocidade_y -= 0.001
                self.velocidade_z -= 0.001

            # Aplicar as velocidades para atualizar os ângulos de rotação
            self.angulo_x += self.velocidade_x
            self.angulo_y += self.velocidade_y
            self.angulo_z += self.velocidade_z

            # Limpar tela
            tela.fill((0, 0, 0))

            # Calcular projeção dos vértices
            vertices_projetados = []
            for vertice in self.vertices:
                vertice_transformado = self.apply_transformations(vertice)
                vertice_projetado = self.projection(vertice_transformado)
                # Ajustar para o centro da tela
                vertice_projetado = vertice_projetado * 200 + np.array([300, 300])
                vertices_projetados.append(vertice_projetado)

            # Desenhar o cubo
            self.draw(tela, vertices_projetados)

            # Atualizar a tela
            pygame.display.flip()
            relogio.tick(60)

    def draw(self, tela, vertices_2d):
        # Desenhar as arestas do cubo
        for aresta in self.arestas:
            pygame.draw.line(tela, (255, 0, 0), 
                             vertices_2d[aresta[0]], vertices_2d[aresta[1]], 2)

        # Desenhar os vértices como pequenos quadrados
        for vertice in vertices_2d:
            pygame.draw.rect(tela, (255, 0, 0), (vertice[0] - 3, vertice[1] - 3, 6, 6))

def run():
    cubo = Cubo()
    cubo.run()

if __name__ == "__main__":
    run()
