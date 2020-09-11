from pydantic import Field, BaseModel


class SongRequest(BaseModel):
    title: str
    artist: str
    year: int
    album: str


class Shards(BaseModel):
    total: int
    successful: int
    failed: int


class SongResponse(BaseModel):
    index: str = Field(alias="_index")
    type: str = Field(alias="_type")
    id: str = Field(alias="_id")
    version: int = Field(alias="_version")
    result: str = Field(alias="result")
    seq_no: int = Field(alias="_seq_no")
    primary_term: int = Field(alias="_primary_term")
    shards: Shards = Field(alias="_shards")
