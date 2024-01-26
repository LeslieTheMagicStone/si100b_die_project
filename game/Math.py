import math


class Math:
    @classmethod
    def same_type_with_input(cls, value, input):
        if isinstance(input, list):
            return list(value)
        elif isinstance(input, tuple):
            return tuple(value)

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
        ans = [x / norm for x in vector]
        return Math.same_type_with_input(ans, vector)

    @classmethod
    def round(cls, vector):
        ans = [round(x) for x in vector]
        return Math.same_type_with_input(ans, vector)

    @classmethod
    def scale(cls, vector, scalar):
        ans = [x * scalar for x in vector]
        return Math.same_type_with_input(ans, vector)

    @classmethod
    def add(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise ValueError(
                f"addition of different len vectors: {len(vector1)} and {len(vector2)}"
            )
        ans = [vector1[i] + vector2[i] for i in range(len(vector1))]
        return Math.same_type_with_input(ans, vector1)

    @classmethod
    def minus(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise ValueError(
                f"minus of different len vectors: {len(vector1)} and {len(vector2)}"
            )
        ans = [vector1[i] - vector2[i] for i in range(len(vector1))]
        return Math.same_type_with_input(ans, vector1)

    @classmethod
    def distance(cls, vector1, vector2):
        if len(vector1) != len(vector2):
            raise ValueError(
                f"distance of different len vectors: {len(vector1)} and {len(vector2)}"
            )
        return cls.norm(cls.minus(vector1, vector2))

    @classmethod
    def orthogonal(cls, vector):
        if len(vector) != 2:
            raise ValueError(f"only support 2d orthogonal")

        ans = [vector[1], -vector[0]]
        return Math.same_type_with_input(ans, vector)

    @classmethod
    def ortho_normal(cls, vector):
        ans = Math.normalize(Math.orthogonal(vector))
        return Math.same_type_with_input(ans, vector)

    @classmethod
    def angle_degrees(cls, vector):
        if len(vector) != 2:
            raise ValueError(f"only support 2d angle")

        return math.degrees(math.atan2(vector[0], vector[1]))
