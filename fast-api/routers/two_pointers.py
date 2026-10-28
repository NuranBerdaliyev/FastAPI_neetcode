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
