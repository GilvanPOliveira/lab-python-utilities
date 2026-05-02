import hashlib

from src.modules.hash_tools.schemas import HashRequest


def generate_hash(payload: HashRequest) -> dict[str, str]:
    encoded = payload.value.encode("utf-8")
    result = hashlib.new(payload.algorithm)
    result.update(encoded)

    return {
        "algorithm": payload.algorithm,
        "hash": result.hexdigest(),
    }
