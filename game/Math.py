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

    @classmethod
    def add(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise ValueError(
                f"addition of different len vectors: {len(vector1)} and {len(vector2)}"
            )
        return [vector1[i] + vector2[i] for i in range(len(vector1))]

    @classmethod
    def minus(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise ValueError(
                f"minus of different len vectors: {len(vector1)} and {len(vector2)}"
            )
        return [vector1[i] - vector2[i] for i in range(len(vector1))]

    @classmethod
    def distance(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise ValueError(
                f"distance of different len vectors: {len(vector1)} and {len(vector2)}"
            )
        return cls.norm(cls.minus(vector1, vector2))
