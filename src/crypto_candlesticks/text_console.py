# -*- coding: utf-8 -*-
"""Display data in the CLI using Rich."""
from typing import List, Union

import pandas as pd
from rich import box
from rich.live import Live
from rich.table import Table

Candles = List[List[List[Union[int, float]]]]


def setup_table() -> Table:
    """Create Rich table layout.

    Returns:
        Table: Include desired description and columns.
    """
    table: Table = Table(
        show_header=True,
        caption=caption(),
        box=box.MINIMAL_HEAVY_HEAD,
        header_style='bold #ffff00',
        title='CRYPTO CANDLESTICKS',
        title_style='bold #54ff00 underline',
        show_lines=True,
        safe_box=True,
        expand=True,
    )
    table_columns = [
        'OPEN',
        'CLOSE',
        'HIGH',
        'LOW',
        'VOLUME',
        'TICKER',
        'INTERVAL',
        'TIME',
    ]
    list(
        map(
            lambda table_columns: table.add_column(
                table_columns,
                justify='center',
                no_wrap=True,
            ),
            table_columns,
        ),
    )

    return table


def write_to_console(
    ticker: str,
    interval: str,
    data_downloaded: Candles,
    live: Live,
    table: Table,
) -> Table:
    """Write data to console.

    Args:
        ticker (str): Quote + base currency.
        interval (str): Candlestick interval.
        data_downloaded (Candles): Response from the exchange.
        live (Live): Context manager.
        table (Table): Rich table.

    Returns:
        Table: Updated table to be rendered.
    """
    for row_limit, single_candle in enumerate(data_downloaded[::-1]):
        table.add_row(
            f'[bold white]{single_candle[2]}[/bold white]',  # Open
            f'[bold white]{single_candle[1]}[/bold white]',  # Close
            f'[bold white]{single_candle[3]}[/bold white]',  # High
            f'[bold white]{single_candle[4]}[/bold white]',  # Low
            f'[bold white]{single_candle[5]}[/bold white]',  # Volume
            f'[bold white]{ticker}[/bold white]',
            f'[bold white]{interval}[/bold white]',
            f"[bold white]{pd.to_datetime(single_candle[0], unit='ms')}[/bold white]",
        )
        if row_limit == 15:
            live.update(table)
            break
    live.update(table)
    return table


def caption() -> str:
    """Caption to be displayed at the end.

    Returns:
        str: Message for the users.
    """
    return 'Thank you for using crypto-candlesticks\
            Consider supporting your developers\
            ETH: 0x06Acb31587a96808158BdEd07e53668d8ce94cFE\
            '
