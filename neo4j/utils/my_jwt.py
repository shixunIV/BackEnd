import yaml
import jwt


class MyJwt:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        PATH = "../users/config.yml"
        with open(PATH, "r") as f:
            self.CFG = yaml.safe_load(f)
        print(self.CFG)

    # 解码token
    def parse_token(self, token_string: str):
        try:
            payload = jwt.decode(
                token_string,
                algorithms=["HS256"],
            )
        except jwt.ExpiredSignatureError:
            return "Token has expired"
        except jwt.InvalidTokenError:
            return "Invalid token"
        return True


if __name__ == "__main__":
    jwt_instance = MyJwt()
    token = jwt_instance.parse_token(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJJRCI6Inh5aCIsImV4cCI6MTcxNTQxOTg0NH0.n9K3tTwJuwAMFzlL-Weu3r7JWHsUmnAL1k00YXlpY9Y"
    )
    print(token)
