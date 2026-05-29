import pandas as pd
from langchain_core.documents import Document


def load_excel(excel_path: str) -> list[Document]:
    workbook = pd.read_excel(excel_path, sheet_name=None)
    documents: list[Document] = []

    for sheet_name, dataframe in workbook.items():
        normalized_df = dataframe.fillna("")
        columns = [str(column) for column in normalized_df.columns]

        for row_index, row in normalized_df.iterrows():
            row_pairs = [
                f"{column}: {value}"
                for column, value in zip(columns, row.tolist())
                if str(value).strip()
            ]
            if not row_pairs:
                continue

            documents.append(
                Document(
                    page_content="\n".join(row_pairs),
                    metadata={
                        "source": excel_path,
                        "sheet_name": sheet_name,
                        "row_number": int(row_index) + 2,
                    },
                )
            )

    return documents
