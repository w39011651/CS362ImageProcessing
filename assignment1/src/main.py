from assignment1.src.utils import imageIO
from utils import resize

def main(strategy: resize.ResizeStrategy):
        IO = imageIO.photoRW("assignment1/assignment1/yzu1.jpg")
        
        img = IO.read(IO.path)
        assert img is not None
        R.resize(img, 2048, 1080)

if __name__ == "__main__":
        R = resize.ResizeBilinear()
        main(R)