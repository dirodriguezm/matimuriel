import typer
import pandas as pd
from pathlib import Path

app = typer.Typer()


@app.command()
def main(
    mails_path: str,
    files_path: str,
    out_path: str,
    mail_column="mails",
    delimiters=",XX;",
):
    delimiter_list = delimiters.split("XX")
    mails = try_read_csv(Path(mails_path), delimiter_list)
    mails["repetido"] = False
    for path in Path(files_path).rglob("*.csv"):
        dataframe = try_read_csv(path, delimiter_list)
        mails["mask"] = mails[mail_column].isin(dataframe[mail_column])
        mails.repetido = mails.loc[:, ["repetido", "mask"]].any(axis=1)
    mails = mails.drop(columns="mask")
    mails.to_csv(out_path, index=False)


def try_read_csv(path: Path, delimiters: list) -> pd.DataFrame:
    dataframe = pd.DataFrame()
    err = Exception("Error al leer csv")
    is_err = False
    for delim in delimiters:
        try:
            is_err = False
            dataframe = pd.read_csv(path, delimiter=delim)
        except Exception as exc:
            is_err = True
            err = exc
        if not is_err:
            return dataframe
    if is_err:
        raise err


if __name__ == "__main__":
    app()
