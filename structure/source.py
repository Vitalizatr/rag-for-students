from dataclasses import dataclass
import os
import hashlib
@dataclass(frozen=True)
class Source:
    name: str
    full_path : str
    sha256_hash : str
    updated_at_sec : int
    pages : int

    @classmethod
    def create_from_pdf(cls,full_path : str,text : list[str]):
        name = os.path.basename(full_path)
        encode_text = "".join(text).encode("utf-8")
        sha256_hash = hashlib.sha256(encode_text).hexdigest()
        updated_at_sec = int(os.path.getmtime(full_path))
        pages = len(text)

        return cls(
            name = name,
            full_path = full_path,
            sha256_hash = sha256_hash,
            updated_at_sec = updated_at_sec,
            pages = pages
        )
