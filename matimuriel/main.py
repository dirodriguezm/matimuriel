import typer
import pandas as pd
from pathlib import Path

app = typer.Typer()


@app.command()
def main(mails_path: str, files_path: str, out_path: str, mail_column="mails"):
    mails = pd.read_csv(mails_path)
    mails["repetido"] = False
    files_dir = Path(files_path)
    for path in files_dir.iterdir():
        dataframe = pd.read_csv(path)
        mails["mask"] = mails[mail_column].isin(dataframe[mail_column])
        mails.repetido = mails.loc[:, ["repetido", "mask"]].any(axis=1)
    mails = mails.drop(columns="mask")
    mails.to_csv(out_path, index=False)


if __name__ == "__main__":
    app()
