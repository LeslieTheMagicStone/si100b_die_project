class Math:
    @classmethod
    def norm(cls, vector):
        norm = 0
        for x in vector:
            norm += x**2
        norm **= 0.5
        return norm

    @classmethod
    def normalize(cls, vector):
        norm = Math.norm(vector)
        if norm == 0:
            return vector
        return [x / norm for x in vector]

    @classmethod
    def round(cls, vector):
        return [round(x) for x in vector]

    @classmethod
    def dot(cls, vector, scalar):
        return [x * scalar for x in vector]
