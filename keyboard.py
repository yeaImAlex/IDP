
import pygame

class Keyboard1:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((100,100))

    def getKey(self, keyName):
        ans = False
        for eve in pygame.event.get(): pass
        keyInput = pygame.key.get_pressed()
        myKey = getattr(pygame, 'K_{}'.format(keyName))
        if keyInput[myKey]:
            ans = True
        pygame.display.update()

        return ans

    def main(self):
        if self.getKey('a'):
            print('Left')
        if self.getKey('d'):
            print('Right')
        if self.getKey('w'):
            print('Forward')
        if self.getKey('s'):
            print('Backward')
        if self.getKey('e'):
            print('Right forward')
        if self.getKey('q'):
            print('Left forward')

if __name__ == '__main__':
        keyboard = Keyboard1()

        while True:
           keyboard.main()
