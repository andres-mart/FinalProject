import numpy as np
import pandas as pd

from src.data_utils import get_feature_target, get_train_val_sets
from src import outliers_detection


def test_detect_outliers(data: pd.DataFrame):
    """Test the preprocess_data function."""

    assert filtered_df.shape[0] == 8741
    assert filtered_df.shape[1] == 20 
    assert isinstance(train_data, np.ndarray)
    