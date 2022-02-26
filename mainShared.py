def collectTime(startTime, endTime, hz, invisible=None, debug=False, queue=None):
    timeCalculate = (1 / hz) - (endTime - startTime)
    if invisible is not None and debug:
        if queue is not None:
            if timeCalculate < 0:
                queue[0].put("print")
                queue[0].put(f"{endTime - startTime} -> {timeCalculate}: {invisible} of {1/hz}")
        else:
            print(f"{endTime - startTime} -> {timeCalculate}: {invisible} of {1/hz}")

    return timeCalculate if timeCalculate > 0 else 0


if __name__ == '__main__':
    pass
