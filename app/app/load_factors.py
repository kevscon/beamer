import pandas as pd

class AASHTOLoadFactors:
    def __init__(self, max_factor_filepath, min_factor_filepath):
        self.max_factor_df = pd.read_csv(max_factor_filepath, index_col=0)
        self.min_factor_df = pd.read_csv(min_factor_filepath, index_col=0)

    def return_factor(self, load_case, load_type, factor_type='max'):
        if factor_type == 'min':
            factor_df = self.min_factor_df
        else:
            factor_df = self.max_factor_df
        self.factor = factor_df.loc[load_case, load_type]
        return '{:.2f}'.format(self.factor)
