import game
import pygame

pygame.init()

pygame.display.set_caption("Pong")

def main():
    pong_game = game.Game()
    pong_game.run()
    pygame.quit()


if __name__ == '__main__':
    main()
