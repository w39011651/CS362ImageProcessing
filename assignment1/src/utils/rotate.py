import cv2
import numpy as np

from cv2.typing import MatLike
from abc import ABC, abstractmethod
from pathlib import Path

class RotateStrategy(ABC):
        @abstractmethod
        def rotate(self, image:MatLike, angle)->MatLike:...

class RotateAngle(RotateStrategy):
        def rotate(self, image: MatLike, angle:int) -> MatLike:
                center = (image.shape[1] // 2, image.shape[0] // 2)

                matrix = cv2.getRotationMatrix2D(center, angle, 1)
                r_img = cv2.warpAffine(image, matrix, (image.shape[1], image.shape[0]))
                cv2.imshow("win", r_img)
                if cv2.waitKey(0) & 0xFF == ord('q'):
                        cv2.destroyAllWindows()
                        return r_img
                
                return r_img
                

if __name__ == '__main__':
        mat = cv2.imread(Path("./assignment1/assignment1/test.jpg"))
        R = RotateAngle()
        assert mat is not None
        
        
        