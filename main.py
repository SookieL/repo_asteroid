from if3_game.engine import init, Layer
from asteroid import RESOLUTION, AsteroidGame , Spaceship, Asteroid
from random import randint

init(RESOLUTION,(" "*100)+ "Asteroid")


game = AsteroidGame() 

game.run()