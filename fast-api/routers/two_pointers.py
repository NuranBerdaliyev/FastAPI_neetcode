from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/two-pointers",
    tags = ["Two Pointers"]
)

class IsPalindromeInput(BaseModel):
    s: str = Field(..., description="String which has to be checked if it is palindrome", examples=["Was it a car or a cat I saw?"])

class IsPalindromeOutput(BaseModel):
    is_palindrome: bool = Field(..., description="Result. Is it palindrome?", examples=[True])

class TwoSumIIInput(BaseModel):
    numbers: list[int] = Field(..., description="Array of integers", examples = [[1,2,3,4]])
    target: int = Field(..., description="Integer which should be sum of two integers from array", examples=[3])

class TwoSumIIOutput(BaseModel):
    indices: list[int] = Field(..., description="Indices of untegers which sum is target", examples=[[1, 2]])

@router.post("/is-palindrome", response_model=IsPalindromeOutput)
def is_palindrome(data: IsPalindromeInput):
    i=0; j=len(data.s)-1
    while i<j:
        while i<j and not data.s[i].isalnum():
            i+=1
        while i<j and not data.s[j].isalnum():
            j-=1
            
        if data.s[i].lower() != data.s[j].lower():
            return IsPalindromeOutput(is_palindrome=False)
        i+=1
        j-=1
    return IsPalindromeOutput(is_palindrome=True)

@router.post("/two-sum-ii", response_model=TwoSumIIOutput)
def two_sum_ii(data: TwoSumIIInput):
    i=0; j=len(data.numbers)-1
    while i<j:
        current_sum=data.numbers[i]+data.numbers[j]
        if current_sum==data.target:
            return TwoSumIIOutput(indices=[1, 2])
        if current_sum<data.target:
            i+=1
        else:
            j-=1
