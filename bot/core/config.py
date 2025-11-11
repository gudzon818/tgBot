from dataclasses import dataclass

@dataclass
class Config:
    env: str = "dev"

config = Config()
