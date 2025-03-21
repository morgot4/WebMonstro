from pydantic import BaseModel



class Test(BaseModel):
    a: int
    b: str
    c: list



test = Test(a=1, b="2", c=[3])


def test_f(a: int, b: str, c: list):
    print(a, b, c)



test_f(**test.model_dump())