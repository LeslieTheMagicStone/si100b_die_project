class Math:
    @classmethod
    def normalize(cls, vector: tuple) -> tuple:
        if Math.magnitude(vector) == 0:
            return vector
        return [x / Math.magnitude(vector) for x in vector]

    @classmethod
    def magnitude(slc, vector: tuple) -> tuple:
        val = 0
        for x in vector:
            val += x * x
        return pow(val, 0.5)
