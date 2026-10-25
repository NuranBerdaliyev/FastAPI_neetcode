from fastapi import APIRouter, Query, HTTPException, status
from collections import defaultdict
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/arrays-hashing",
    tags = ["Arrays & Hashing"]
)

class ContainsDuplicateInput(BaseModel):
    nums: list[int] = Field(..., description="Array of integers", examples=[[1, 2, 3, 3]])

class TwoSumInput(BaseModel):
    nums: list[int] = Field(..., description="Array of integers", examples=[[2, 7, 11, 15]])
    target: int = Field(..., description="Required target", examples=[9])

class ValidAnagramInput(BaseModel):
    s: str = Field(..., description="First string", examples=["anagram"])
    t: str = Field(..., description="Second string", examples=["nagarma"])

class GroupAnagramsInput(BaseModel):
    strs: list[str] = Field(..., description="Array of strings", examples=[["act", "pots", "tops", "cat", "stop", "hat"]])

class GroupAnagramsOutput(BaseModel):
    result: list[list[str]] = Field(..., description="Anagram's groups")



@router.post("/contains-duplicate")
def contains_duplicate(data: ContainsDuplicateInput):
    seen = set()
    for num in data.nums:
        if num in seen:
            return {"result": True}
        seen.add(num)
    return {"result": False}

@router.post("/valid-anagram")
def valid_anagram(data: ValidAnagramInput):
    if len(data.s) != len(data.t):
        return {"result": False}
        
    dictionary_sex = defaultdict(int)
    for c in data.s:
        dictionary_sex[c] += 1
    for c in data.t:
        dictionary_sex[c] -= 1
        
    return {"result": not any(dictionary_sex.values())}

@router.post("/two-sum")
def two_sum(data: TwoSumInput):
    prefix_dict = {}
    for i in range(len(data.nums)):
        difference = data.target - data.nums[i]
        if difference in prefix_dict:
            return {"indices": [prefix_dict[difference], i]}
        prefix_dict[data.nums[i]] = i
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"No two numbers sum up to target {data.target}"
    )


@router.post("/group-anagrams", response_model=GroupAnagramsOutput)
def group_anagrams(data: GroupAnagramsInput):
    anagram_map = defaultdict(list)
    
    for string in data.strs:
        count = [0] * 26
        for char in string:
            count[ord(char) - ord('a')] += 1
            
        count_key = tuple(count)
        anagram_map[count_key].append(string)
        
    return {"result": list(anagram_map.values())}
