n = int(input())
arr = list(map(int, input().split()))


def func(n, arr):
    global swaps
    swaps = 0
    for i in range(n-1, 1, -1):
        if arr[i] == i + 1:
            continue
        elif arr[i - 1] == i + 1:
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            swaps += 1
        elif arr[i - 2] == i + 1:
            arr[i - 1], arr[i - 2] = arr[i - 2], arr[i - 1]
            arr[i], arr[i - 1] = arr[i - 1], arr[i]
            swaps += 2
        else:
            return False

    if arr[1] == 2:
        return True
    elif arr[0] == 2 and arr[1] == 1:
        swaps += 1
        arr[0], arr[1] = arr[0], arr[1]
        return True
    else:
        return False

if func(n, arr):
    print("YES")
    print(swaps)
else:
    print("NO")

