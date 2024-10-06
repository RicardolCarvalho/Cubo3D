import numpy as np
import pygame

class Cubo:
    def __init__(self):
        self.vertices = np.array([
            [-1, -1, -1], [-1, -1,  1], [-1,  1, -1], [-1,  1,  1],
            [ 1, -1, -1], [ 1, -1,  1], [ 1,  1, -1], [ 1,  1,  1]
        ])
        
        self.arestas = [(0, 1), (1, 3), (3, 2), (2, 0), (4, 5), (5, 7), (7, 6), (6, 4), 
                        (0, 4), (1, 5), (2, 6), (3, 7)]
        
        self.angulo_x = self.angulo_y = self.angulo_z = 0
        self.velocidade_x = self.velocidade_y = self.velocidade_z = 0.01
        self.translacao = np.array([0, 0, -8])

    def rotation_matrix_x(self, theta):
        return np.array([
            [1, 0, 0], [0, np.cos(theta), -np.sin(theta)], [0, np.sin(theta), np.cos(theta)]
        ])

    def rotation_matrix_y(self, theta):
        return np.array([
            [np.cos(theta), 0, np.sin(theta)], [0, 1, 0], [-np.sin(theta), 0, np.cos(theta)]
        ])

    def rotation_matrix_z(self, theta):
        return np.array([
            [np.cos(theta), -np.sin(theta), 0], [np.sin(theta), np.cos(theta), 0], [0, 0, 1]
        ])

    def projection(self, ponto):
        d = 2
        z = ponto[2] if ponto[2] != 0 else 0.001
        fator_escala = d / (d + z)
        return np.array([ponto[0] * fator_escala, ponto[1] * fator_escala])

    def apply_transformations(self, ponto):
        rotacionado = np.dot(self.rotation_matrix_x(self.angulo_x), ponto)
        rotacionado = np.dot(self.rotation_matrix_y(self.angulo_y), rotacionado)
        rotacionado = np.dot(self.rotation_matrix_z(self.angulo_z), rotacionado)
        return rotacionado + self.translacao

    def run(self):
        pygame.init()
        tela = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Cubo e Pirâmide 3D")
        relogio = pygame.time.Clock()
        forma_atual = "cubo"

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    return

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_RIGHT]:
                self.velocidade_x += 0.001
                self.velocidade_y += 0.001
                self.velocidade_z += 0.001
            if teclas[pygame.K_LEFT]:
                self.velocidade_x -= 0.001
                self.velocidade_y -= 0.001
                self.velocidade_z -= 0.001
            if teclas[pygame.K_p]:
                forma_atual = "piramide"
            if teclas[pygame.K_c]:
                forma_atual = "cubo"

            self.angulo_x += self.velocidade_x
            self.angulo_y += self.velocidade_y
            self.angulo_z += self.velocidade_z

            tela.fill((0, 0, 0))
            if forma_atual == "cubo":
                self.draw_cubo(tela)
            elif forma_atual == "piramide":
                self.draw_piramide(tela)

            pygame.display.flip()
            relogio.tick(60)

    def draw_cubo(self, tela):
        vertices_projetados = []
        for vertice in self.vertices:
            transformado = self.apply_transformations(vertice)
            projetado = self.projection(transformado)
            ajustado = projetado * 200 + np.array([300, 300])
            vertices_projetados.append(ajustado)
        for aresta in self.arestas:
            pygame.draw.line(tela, (255, 0, 0), vertices_projetados[aresta[0]], vertices_projetados[aresta[1]], 2)
        for vertice in vertices_projetados:
            pygame.draw.rect(tela, (255, 0, 0), (vertice[0] - 3, vertice[1] - 3, 6, 6))

    def draw_piramide(self, tela):
        vertices_piramide = np.array([[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [0, 0, 1]])
        arestas_piramide = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)]
        vertices_projetados = []
        for vertice in vertices_piramide:
            transformado = self.apply_transformations(vertice)
            projetado = self.projection(transformado)
            ajustado = projetado * 200 + np.array([300, 300])
            vertices_projetados.append(ajustado)
        for aresta in arestas_piramide:
            pygame.draw.line(tela, (0, 255, 0), vertices_projetados[aresta[0]], vertices_projetados[aresta[1]], 2)
        for vertice in vertices_projetados:
            pygame.draw.rect(tela, (0, 255, 0), (vertice[0] - 3, vertice[1] - 3, 6, 6))

def run():
    cubo = Cubo()
    cubo.run()

if __name__ == "__main__":
    run()
