import os
import sys

__package__ = 'genai'
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'py'))

if __name__ == "__main__" and __package__ is None:
    __package__ = "genai"

del os
del sys