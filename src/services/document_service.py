import io
import uuid
from pathlib import Path
from typing import Tuple

from pandas import DataFrame
from sqlalchemy import text
from streamlit.connections import SQLConnection


class DocumentService:
    DOCUMENTS_FOLDER = "./uploaded_docs"
    DOCUMENTS_TABLE  = "uploaded_document"

    def __init__(self, db: SQLConnection):
        self._db = db
        self._files_directory = Path(self.DOCUMENTS_FOLDER)
        self._files_directory.mkdir(parents=True, exist_ok=True)


    def upload_document(self, file_name: str, file: io.BytesIO) -> Tuple[int, str]:
        new_file_path = f"{uuid.uuid4()}_{file_name}"
        new_path = self._files_directory / new_file_path
        new_path.write_bytes(file)

        with self._db.session as s:
            created_id = s.execute(
                text(f"INSERT INTO {self.DOCUMENTS_TABLE} (name, path) VALUES (:name, :path) RETURNING id;"),
                params=dict(
                    name=file_name,
                    path=new_file_path
                )
            ).scalar()
            s.commit()

        return created_id, str(new_path)

    def get_uploaded_files(self) -> DataFrame:
        return self._db.query(
            f"select id, name, created_timestamp from {self.DOCUMENTS_TABLE}",
            ttl=0,
        )
