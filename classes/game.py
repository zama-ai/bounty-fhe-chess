import pygame
from base import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger() 

    def display_chessboard(self, surface):
        for row in range(cb_rows):
            for col in range(cb_cols):
                if(row + col) %2 == 0:
                    color = (251,203,4) #(255,203,0,255)
                else:
                    color = (29,24,9) #(0,0,0,255)

                rect = (col * sqsize, row * sqsize, sqsize, sqsize)

                pygame.draw.rect(surface, color, rect)

    def display_pieces(self, surface):
        for row in range(cb_rows):
            for col in range(cb_cols):
                #presence of a piece
                if self.board.squares[row][col].piece_presence():
                    piece = self.board.squares[row][col].piece

                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        # pygame specification
                        img = pygame.image.load(piece.img_uri)
                        img_center = col * sqsize + sqsize // 2, row * sqsize + sqsize // 2
                        piece.rectangle = img.get_rect(center=img_center)
                        surface.blit(img, piece.rectangle)