# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/02_dataset.ipynb (unless otherwise specified).

__all__ = ['Dataset', 'create_dataset']

# Cell
import uuid
import numpy as np
import pandas as pd
from copy import deepcopy
import json
from pathlib import Path
from typing import Union, Tuple
import datetime as dt
from functools import wraps
from rich import print as rich_print
from typeguard import typechecked

# Cell
class Dataset:
    def __init__(self, dataf: pd.DataFrame, *args, **kwargs):
        self.dataf = dataf
        self.__dict__.update(*args, **kwargs)
        self.all_cols = list(self.dataf.columns)
        self.feature_cols = [col for col in self.all_cols if col.startswith("feature")]
        self.target_cols = [col for col in self.all_cols if col.startswith("target")]
        self.prediction_cols = [
            col for col in self.all_cols if col.startswith("prediction")
        ]
        self.not_aux_cols = self.feature_cols + self.target_cols + self.prediction_cols
        self.aux_cols = [
            col for col in self.all_cols if col not in self.not_aux_cols
        ]

    def copy_dataset(self):
        """Copy Dataset object"""
        return deepcopy(self)

    def copy_dataframe(self) -> pd.DataFrame:
        """Copy DataFrame part of Dataset"""
        return deepcopy(self.dataf)

    def export_json_metadata(self, file="config.json", verbose=False, **kwargs):
        """Export all attributes in Dataset that can be serialized to json file."""
        rich_print(f":file_folder: Exporting metadata to {file} :file_folder:")
        json_txt = json.dumps(
            self.__dict__, default=lambda o: "<not serializable>", **kwargs
        )
        if verbose:
            rich_print(json_txt)
        Path(file).write_text(json_txt)

    def import_json_metadata(self, file="config.json", verbose=False, **kwargs):
        """Load arbitrary data into Dataset object from json file."""
        rich_print(f":file_folder: Importing metadata from {file} :file_folder:")
        with open(file) as json_file:
            json_data = json.load(json_file, **kwargs)
        if verbose:
            rich_print(json_data)
        # Make sure there is no overwrite on DataFrame
        json_data.pop("dataf", None)
        self.__dict__.update(json_data)

    def get_column_selection(self, cols: Union[str, list]) -> pd.DataFrame:
        """Return DataFrame given selection of columns."""
        return self.dataf.loc[:, cols if isinstance(cols, list) else [cols]]

    @property
    def get_feature_data(self) -> pd.DataFrame:
        return self.get_column_selection(cols=self.feature_cols)

    @property
    def get_target_data(self) -> pd.DataFrame:
        return self.get_column_selection(cols=self.target_cols)

    @property
    def get_single_target_data(self) -> pd.DataFrame:
        return self.get_column_selection(cols=['target'])

    @property
    def get_prediction_data(self) -> pd.DataFrame:
        return self.get_column_selection(cols=self.prediction_cols)

    @property
    def get_aux_data(self) -> pd.DataFrame:
        """All columns that are not features, targets nor predictions."""
        return self.get_column_selection(cols=self.aux_cols)

    def get_feature_target_pair(self, multi_target=False) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get split of feature and target columns.
        :param multi_target: Returns only 'target' column by default.
        Returns all target columns when set to True.
        """
        X = self.get_feature_data
        y = self.get_target_data if multi_target else self.get_single_target_data
        return X, y

    def merge_datasets(self, other, *args, **kwargs):
        """
        Merge Dataset with other Dataset.
        :param other: Another Dataset.
        WARNING: Metadata of original Dataset will be kept in case of duplicates.
        *args, **kwargs will be passed to DataFrame merge operation.
        :return: Dataset with dataf and metadata merged.
        Metadata of original has priority in case of duplicate keys
        """
        # Merge DataFrames
        new_dataset, other_copy = self.copy_dataset(), other.copy_dataset()
        new_dataset.dataf = self.dataf.merge(other.dataf, *args, **kwargs)
        # Merge metadata
        other_copy.__dict__.pop('dataf', None)
        new_dataset.__dict__.update(**other_copy.__dict__)
        return Dataset(**new_dataset.__dict__)

    def __repr__(self) -> str:
        return f"Dataset of shape {self.dataf.shape}. Columns: {self.all_cols}"

    def __str__(self):
        return self.__repr__()

# Cell
def create_dataset(file_path: str, *args, **kwargs):
    """
    Convenience function to initialize Dataset object with arbitrary metadata.
    Supports file formats for which Pandas has a 'read_' function.
    For example, .csv, .parquet, .json, .pickle, .html and .xml.
    For more details check https://pandas.pydata.org/docs/reference/io.html
    """
    assert Path(file_path).is_file(), f"{file_path} does not point to file."
    suffix = Path(file_path).suffix[1:]
    # Suffix without dot
    dataf = getattr(pd, f"read_{suffix}")(file_path)
    return Dataset(dataf, *args, **kwargs)