def validateNumberInput(minValue: int, maxValue: int):
    def validate(_, value):
        try:
            intValue = int(value)
            if intValue >= minValue and intValue <= maxValue:
                return True
            return False
        except:
            return False

    return validate
