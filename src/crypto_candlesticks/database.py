# -*- coding: utf-8 -*-
"""Sqlite database class."""

# built-in
import sqlite3
from typing import Union

# external
import click


Candles = list[list[list[Union[int, float]]]]


class SqlDatabase(object):
    """SqlDatabase main class for storing the candlestick data in SQL."""

    __slots__ = ('_conn', '_cursor', '_pragmas', '_schema')

    def __init__(self, databasefile: str) -> None:
        """Create the database object to which the data will be saved.

        Args:
            databasefile (str): Filename for the database.
        """
        self._conn = sqlite3.connect(databasefile)
        self._cursor = self._conn.cursor()
        self._pragmas = (
            "PRAGMA encoding='UTF-8';",
            'PRAGMA synchronous=0;',
            'PRAGMA journal_mode=WAL;',
        )
        self._schema = """CREATE TABLE IF NOT EXISTS "Candlestick"(
                ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Timestamp REAL NOT NULL,
                Open REAL NOT NULL,
                Close REAL NOT NULL,
                High REAL NOT NULL,
                Low REAL NOT NULL,
                Volume REAL NOT NULL,
                Ticker TEXT NOT NULL,
                Interval TEXT NOT NULL
                )"""
        for pragma in self._pragmas:
            self._cursor.execute(pragma)
        self._cursor.execute(self._schema)

    def __repr__(self) -> str:
        """Database repr dunder.

        Returns:
            str: Object representation.
        """
        return 'Sql database class'

    def insert_candlesticks(
        self,
        candlestick_info: Candles,
        ticker: str,
        interval: str,
    ) -> None:
        """Write the candlestick data into a SQL table.

        Args:
            candlestick_info (Candles): A list of containing OHLC.
            ticker (str): Ticker of the candle.
            interval (Interval): Period downloaded.

        Raises:
            sqlite3.Error: Exception that prevented to write the data.
        """
        try:
            for candle in candlestick_info[::-1]:
                with self._conn:
                    self._cursor.execute(
                        'INSERT INTO Candlestick VALUES \
                        (:ID, :Timestamp, :Open, \
                        :Close, :High, :Low, \
                        :Volume, :Ticker, :Interval)',
                        {
                            'ID': None,
                            'Timestamp': candle[0],
                            'Open': candle[2],
                            'Close': candle[1],
                            'High': candle[3],
                            'Low': candle[4],
                            'Volume': candle[5],
                            'Ticker': ticker,
                            'Interval': interval,
                        },
                    )
        except (sqlite3.Error) as sqlite_error:
            click.secho(
                f'Failed to write data to Database {sqlite_error}',
                fg='red',
            )
            raise
