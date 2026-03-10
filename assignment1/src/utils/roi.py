import cv2
import numpy as np

from pathlib import Path
from abc import ABC, abstractmethod
from cv2.typing import MatLike, Rect
from typing import Tuple

class RoiSelector(ABC):
        def select(self, img: MatLike)->Rect:
                rect = cv2.selectROI("ROI", img, showCrosshair=False, fromCenter=False)
                cv2.destroyAllWindows()
                return rect
        @abstractmethod
        def cut(self, img:MatLike, area:Rect)->MatLike:...

        def run(self, img:MatLike)->MatLike:
                rect = self.select(img)
                roi = self.cut(img, rect)
                return roi

                

class RoiRectSelector(RoiSelector):
        def cut(self, img:MatLike, area:Rect)->MatLike:
                x,y,w,h = area
                roi = img[y:y+h, x:x+w]
                return roi
        
        
class RoiEllipseSelector(RoiSelector):
        def find_incircle(self, rect:Rect)->Tuple[Tuple[int, int], Tuple[int, int]]:
                x,y,w,h = rect
                center = (w // 2, h // 2)
                axes = (w // 2, h // 2)
                return center, axes
        
        def cut(self, img:MatLike, area:Rect)->MatLike:
                x,y,w,h = area
                center, axes = self.find_incircle(area)
                roi_rect = img[y:y+h, x:x+w]

                mask = np.zeros((roi_rect.shape[0], roi_rect.shape[1]), dtype=np.uint8)
                cv2.ellipse(
                        img=mask,
                        center=center,
                        axes=axes,
                        angle=0, startAngle=0,endAngle=360,color=255,thickness=-1,
                )

                result = cv2.bitwise_and(roi_rect, roi_rect, mask=mask)
                return result

                

if __name__ == '__main__':
        img_data = np.fromfile(Path("C:/Users/lovem/Desktop/repository/影像處理概論/assignment1/assignment1/assignment1/test.jpg"), dtype=np.uint8)
        img = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
        r = RoiEllipseSelector()
        assert img is not None

        nimg = r.run(img)
        cv2.imshow("ROI", nimg)
        if cv2.waitKey(0) & 0xFF00 == ord('q'):
                exit()
        