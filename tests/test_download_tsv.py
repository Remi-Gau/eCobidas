from ecobidas.download_tsv import download_spreadsheet


def test_download_spreadsheet(tmp_path):
    download_spreadsheet(schema="neurovault", output_dir=tmp_path)
