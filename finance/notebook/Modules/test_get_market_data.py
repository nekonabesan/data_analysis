from pathlib import Path
import sys

import numpy as np
import pandas as pd
import pytest

# Ensure this test can import sibling module when run from workspace root.
sys.path.append(str(Path(__file__).resolve().parent))
import get_market_data as gmd


def test_get_csv_data_reads_expected_file(tmp_path: Path):
    csv_path = tmp_path / "sample.csv"
    src = pd.DataFrame(
        {"700.HK": [0.01, -0.02], "175.HK": [0.03, 0.04]},
        index=pd.to_datetime(["2025-01-01", "2025-01-02"]),
    )
    src.to_csv(csv_path)

    obj = gmd.GetMarketData(tmp_path)
    out = obj.get_csv_data("sample.csv")

    assert list(out.columns) == ["700.HK", "175.HK"]
    assert len(out) == 2
    assert str(out.index.dtype).startswith("datetime64")


def test_get_data_from_yfinance_uses_download(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    expected = pd.DataFrame(
        {
            ("Close", "9434.T"): [100.0, 101.0],
            ("Open", "9434.T"): [99.0, 100.0],
        },
        index=pd.to_datetime(["2025-01-06", "2025-01-07"]),
    )

    def fake_download(tickers, start=None, end=None):
        assert tickers == ["9434.T"]
        assert start == "2025-01-01"
        assert end == "2025-01-31"
        return expected

    monkeypatch.setattr(gmd.yf, "download", fake_download)

    obj = gmd.GetMarketData(tmp_path)
    out = obj.get_data_from_yfinance(["9434.T"], start="2025-01-01", end="2025-01-31")

    pd.testing.assert_frame_equal(out, expected)


def test_convert_prices_to_returns_simple(tmp_path: Path):
    obj = gmd.GetMarketData(tmp_path)
    price_df = pd.DataFrame(
        {"A": [100.0, 110.0, 121.0], "B": [200.0, 210.0, 220.5]}
    )

    out = obj.convert_prices_to_returns(price_df, method="simple")

    expected = pd.DataFrame(
        {
            "A": [0.10, 0.10],
            "B": [0.05, 0.05],
        },
        index=[1, 2],
    )
    pd.testing.assert_frame_equal(out, expected, rtol=1e-10, atol=1e-10)


def test_convert_prices_to_returns_log(tmp_path: Path):
    obj = gmd.GetMarketData(tmp_path)
    price_df = pd.DataFrame({"A": [100.0, 110.0, 121.0]})

    out = obj.convert_prices_to_returns(price_df, method="log")

    expected_values = np.log(np.array([110.0 / 100.0, 121.0 / 110.0]))
    assert np.allclose(out["A"].to_numpy(), expected_values)


def test_convert_prices_to_returns_invalid_method_raises(tmp_path: Path):
    obj = gmd.GetMarketData(tmp_path)
    price_df = pd.DataFrame({"A": [100.0, 110.0]})

    with pytest.raises(ValueError, match="method must be 'simple' or 'log'"):
        obj.convert_prices_to_returns(price_df, method="invalid")
