
from collections.abc import Sequence

def check_fibonacci(data: Sequence[int]) -> bool:

    if len(data) < 2:
        return print(True)  

    if data[0] != 0 or data[1] != 1:
        return print(False)

    for i in range(2, len(data)):
        if data[i] != data[i - 1] + data[i - 2]:
            return print(False)

    return print(True)

check_fibonacci([0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89])