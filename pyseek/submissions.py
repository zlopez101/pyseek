import typer
import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag
from pyseek import edgar, _read, utils, models

app = typer.Typer()


def extractText(report: str) -> str:
    blocks = ["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th"]

    def to_plaintext(html_text: str) -> str:
        soup = BeautifulSoup(html_text, features="lxml")
        extracted_blocks = _extract_blocks(soup.body)
        extracted_blocks_texts = [
            block.get_text().strip() for block in extracted_blocks
        ]
        return "\n".join(extracted_blocks_texts)

    def _extract_blocks(parent_tag) -> list:
        extracted_blocks = []
        for tag in parent_tag:
            if tag.name in blocks:
                extracted_blocks.append(tag)
                continue
            if isinstance(tag, Tag):
                if len(tag.contents) > 0:
                    inner_blocks = _extract_blocks(tag)
                    if len(inner_blocks) > 0:
                        extracted_blocks.extend(inner_blocks)

        return extracted_blocks

    return to_plaintext(report)


@app.command()
def get(
    company: str = typer.Argument(..., help="CIK number or ticker of the company"),
    record: str = typer.Option(None, "--record", "-f", help="record to save the data"),
) -> dict:
    """Get all the company submissions for a given CIK, returns a csv"""
    company = utils.validate_ticker_or_cik(company)
    results = edgar.get_all_company_submissions(company.cik_str)
    df = _read.read_submissions(results)

    record = utils.validate_submission_record(company=company, record=record)

    df.to_csv(record, index=False)


@app.command()
def filter(
    company: str = typer.Option(
        None, "--company", "-c", help="CIK number or ticker of the company"
    ),
    record: str = typer.Option(
        None, "--record", "-r", help="Filename to save the data"
    ),
    form: models.Form = typer.Option(
        models.Form.tenk, "--form", "-f", help="Filing type to filter by"
    ),
):
    """Given a submissions file, filter by form type"""
    if not company and not record:
        raise typer.BadParameter("You must provide either a company or a record")
    record = utils.validate_submission_record(company=company, record=record)
    df = pd.read_csv(record)
    print(df[df["form"] == form.value])


@app.command()
def download(
    company: str = typer.Option(
        ..., "--company", "-c", help="CIK number or ticker of the company"
    ),
    record: str = typer.Option(
        None, "--record", "-r", help="Filename to save the data"
    ),
    form: models.Form = typer.Option(
        models.Form.tenk, "--form", "-f", help="Filing type to filter by"
    ),
    latest: bool = typer.Option(
        True, " /--latest", " /-l", help="Download the latest flag"
    ),
    number: int = typer.Option(1, "--number", "-n", help="The number to download"),
):
    """Download a sec company submission"""
    record = utils.validate_submission_record(company=company, record=record)
    df = pd.read_csv(record)
    company = utils.validate_ticker_or_cik(company)
    # items are sorted by filingDate, with most recent on top
    forms = df[df["form"] == form.value]

    if latest:
        most_recent_form = forms.iloc[0]
        accn = most_recent_form["accessionNumber"]
        primaryDoc = most_recent_form["primaryDocument"]
    report = edgar.download_company_submission(company.cik_str, accn, primaryDoc)
    soup = BeautifulSoup(report, "html.parser")
    # report = soup.get_text()
    with open(f"{company.ticker}_{form.value}.txt", "w") as f:
        f.write(soup.get_text(separator="\n", strip=True))
