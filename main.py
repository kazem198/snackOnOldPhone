import cv2
import numpy as np
import random
import math


class Snack:
    def __init__(self):
        self.wFood = 20
        self.hFood = 20
        self.posFood = random.randint(100, 1100), random.randint(100, 700)
        self.moveKey = -1  # 0move up,1 move right,2move down,3move left
        self.points = [[500, 480], [500, 490], [500, 500]]
        self.allowLength = 5  # maximum length
        self.currentLength = 3
        self.score = 0
        self.allowGame = True
        self.collosion = False

    def update(self, img):

        if self.currentLength < len(self.points):
            self.points.pop(0)

        #     draw snack
        for i, point in enumerate(self.points):

            if i > 0:
                distance = math.hypot(
                    self.points[i][0]-self.points[i-1][0], self.points[i][1]-self.points[i-1][1])
                if distance < 500:
                    cv2.line(
                        img, self.points[i], self.points[i-1], (255, 0, 0), 3)

            #     draw Head
        headPoint = self.points[-1]
        cv2.circle(img, headPoint, 5, (0, 0, 255), cv2.FILLED)

        # check for eat food

        x, y = headPoint
        if self.posFood[0] - (self.wFood//2) < x < self.posFood[0] + (self.wFood//2) and self.posFood[1] - (self.hFood//2) < y < self.posFood[1] + (self.hFood//2):
            self.currentLength += 1
            self.positionFood()
            self.score += 1

        # check for collosion
        distance = []
        for i, point in enumerate(self.points):

            if i < len(self.points)-3:
                cx, cy = self.points[-2]
                px, py = self.points[i]
                distance.append(int(math.hypot(cx - px, cy - py)))

        if len(distance) > 2:
            if min(distance) < 5:
                self.allowGame = False
                self.collosion = True
                print("GAME OVER:collosin")

        return img

    def move(self):
        lastPoint = self.points[-1]

        if self.moveKey == 0:
            up = lastPoint[1]-10

            if up <= 0:
                addPoint = [lastPoint[0],  720]
            else:
                addPoint = [lastPoint[0],  up]

            self.points.append(addPoint)

        elif self.moveKey == 1:
            right = lastPoint[0]+10
            if right > 1280:
                addPoint = [0,  lastPoint[1]]
            else:
                addPoint = [right,  lastPoint[1]]

            self.points.append(addPoint)

        elif self.moveKey == 2:
            down = lastPoint[1]+10
            addPoint = [lastPoint[0],  down]
            if down > 720:
                addPoint = [lastPoint[0],  0]

            else:
                addPoint = [lastPoint[0],  down]

            self.points.append(addPoint)

        elif self.moveKey == 3:
            left = lastPoint[0]-10

            if left <= 0:
                addPoint = [1280,  lastPoint[1]]
            else:
                addPoint = [left,  lastPoint[1]]

            self.points.append(addPoint)

    def positionFood(self):
        self.posFood = random.randint(100, 1100), random.randint(100, 700)


game = Snack()
while True:
    img = np.zeros((720, 1280, 3), np.uint8)
    if game.allowGame:
        cv2.rectangle(img, (game.posFood[0]-game.wFood//2, game.posFood[1]-game.hFood//2),
                      (game.posFood[0]+game.wFood//2, game.posFood[1]+game.hFood//2), (255, 255, 255), cv2.FILLED)
        game.move()
        img = game.update(img)
    else:
        if game.collosion:
            cv2.putText(img, "collosin!!!! to start again please press r button", (5, 550),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        else:
            cv2.putText(img, "to start again please press r button", (5, 550),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    if game.allowLength+3 <= len(game.points):
        cv2.putText(img, "YOU WIN ", (350, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 5)
        game.allowGame = False
    key = cv2.waitKey(100)

    cv2.putText(img, f'YOUR SCORE IS : {
                str(game.score)}', (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    cv2.imshow("Image", img)

    if key == ord("q"):
        cv2.destroyAllWindows()
        break
    elif key == ord("w") and game.moveKey != 2:
        game.moveKey = 0
    elif key == ord("d") and game.moveKey != 3:
        game.moveKey = 1
    elif key == ord("s") and game.moveKey != 0:
        game.moveKey = 2
    elif key == ord("a") and game.moveKey != 1:
        game.moveKey = 3
    elif key == ord("r"):
        game.allowGame = True

        game.posFood = random.randint(100, 1100), random.randint(100, 700)
        game.moveKey = -1  # 0move up,1 move right,2move down,3move left
        game.points = [[500, 480], [500, 490], [500, 500]]

        game.currentLength = 3
        game.score = 0
