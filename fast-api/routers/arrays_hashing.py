from fastapi import APIRouter, HTTPException, status
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
    result: list[list[str]] = Field(..., description="Anagram's groups", examples=[[["act", "cat"], ["pots", "tops", "stop"], ["hat"]]])

class EncodeDecodeInput(BaseModel):
    strs: list[str] = Field(..., description="Array of string for encoding and decoding", examples=[["Hello,World", "4#", "   ", "neet#code"]])

class EncodeDecodeOutput(BaseModel):
    strs: list[str] = Field(..., description="Input", examples=[["Hello,World", "4#", "   ", "neet#code"]])
    encoded_str: str = Field(..., description="Result of encoding input", examples=["11#Hello,World2#4#3#   9#neet#code"])
    decoded_str: list[str] = Field(..., description="Result of decoding the encoded string. It has to be the same input", examples=[["Hello,World", "4#", "   ", "neet#code"]])

class ProductExceptSelfInput(BaseModel):
    nums: list[int] = Field(..., description = "Array of integers", examples = [[-1,0,1,2,3]])

class ProductExceptSelfOutput(BaseModel):
    nums: list[int] = Field(..., description="Array of integers demonstrating the product of elements except the index where integer is", examples=[[0,-6,0,0,0]])

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

@router.post("/encode-decode", response_model=EncodeDecodeOutput)
def encode_decode_strings(data: EncodeDecodeInput):
    chunks = []
    for s in data.strs:
        chunks.append(str(len(s)) + "#" + s)
    encoded_res = "".join(chunks)
    
    decoded_res = []
    i = 0
    while i < len(encoded_res):
        length = 0
        j = i
        while encoded_res[j].isdigit():
            length = length * 10 + int(encoded_res[j])
            j += 1
            
        word = encoded_res[j + 1 : j + 1 + length]
        decoded_res.append(word)
        i = j + 1 + length

    return EncodeDecodeOutput(
        strs=data.strs,
        encoded_str=encoded_res,
        decoded_str=decoded_res
    )

@router.post("/product-except-self", response_model=ProductExceptSelfOutput)
def product_of_array_except_self(data: ProductExceptSelfInput):
    number=1
    prefix_list=[]
    for num in data.nums:
        prefix_list.append(number)
        number*=num
            
    number=1
    suffix_list=[]
    for num in reversed(data.nums):
        suffix_list.append(number)
        number*=num

    suffix_list.reverse()
    nums=[]
    for left, right in zip(prefix_list, suffix_list):
        nums.append(left*right)
        
    return ProductExceptSelfOutput(
        nums = nums
    )