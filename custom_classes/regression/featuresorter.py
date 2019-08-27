import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class FeatureSort:
    '''
    Sort (in descending order) feature weights for Linear Regression or Logistic Regression models

    Parameters
    ----------
    weights : array of feature weights from model
    labels : list of feature labels
    '''

    def __init__(self, weights, labels):
        self.weights = weights
        self.labels = labels

    def sort_wgts(self, num_ret='all', ret_0=False):
        '''
        Sort feature weights (greatest to least)

        Parameters
        ----------
        num_ret : number of top features to return
        ret_0 : return weights with value of zero
        '''
        # create feature weight dataframe
        self.df = pd.DataFrame(self.weights, index=self.labels, columns=['feat_wgt']).copy()

        # sort feature weight dataframe
        self.df.sort_values(by='feat_wgt', ascending=False, inplace=True)

        # 0 values
        if ret_0 == False:
            # drop weights == 0
            self.df = self.df[self.df.iloc[:, 0] != 0]

        # top number of features to return
        if num_ret != 'all':
            # slice number of rows in dataframe
            self.df = self.df.iloc[:num_ret, :]

        # return dataframe
        return(self.df)

    def sort_abs(self, num_ret='all', ret_0=False):
        '''
        Sort feature weights (greatest to least) based on absolute values

        Parameters
        ----------
        num_ret : number of top features to return
        ret_0 : return weights with value of zero
        '''
        # create feature weight dataframe
        self.df = pd.DataFrame(self.weights, index=self.labels, columns=['feat_wgt']).copy()

        # create column identifying positive weights
        self.df['positive'] = self.df['feat_wgt'] > 0
        # transform weights to absolute value
        self.df['feat_wgt'] = self.df['feat_wgt'].apply(abs)
        # sort feature weight dataframe
        self.df.sort_values(by='feat_wgt', ascending=False, inplace=True)

        # 0 values
        if ret_0 == False:
            # drop weights == 0
            self.df = self.df[self.df.iloc[:, 0] != 0]

        # top number of features to return
        if num_ret != 'all':
            # slice number of rows in dataframe
            self.df = self.df.iloc[:num_ret, :]

        # return dataframe
        return(self.df)

    def sort_pct(self, num_ret='all', ret_0=False, rnd=1):
        '''
        Sort feature weights (greatest to least) and return as percentage values

        Parameters
        ----------
        num_ret : number of top features to return
        ret_0 : return weights with value of zero
        rnd : decimal precision for rounding
        '''
        # create feature weight dataframe
        self.df = pd.DataFrame(self.weights, index=self.labels, columns=['feat_wgt']).copy()
        # create column identifying positive weights
        self.df['positive'] = self.df['feat_wgt'] > 0
        # transform weights to absolute value
        self.df['feat_wgt'] = self.df['feat_wgt'].apply(abs)
        # sort weights
        self.df.sort_values(by='feat_wgt', ascending=False, inplace=True)
        # transform weights to percentages
        self.df['feat_wgt'] = round(self.df['feat_wgt'] / self.df['feat_wgt'].sum() * 100, rnd)
        # rename column
        col_rename = self.df.columns.values
        col_rename[0] = 'feat_%'
        self.df.columns = col_rename

        # 0 values
        if ret_0 == False:
            # drop weights == 0
            self.df = self.df[self.df.iloc[:, 0] != 0]

        # top number of features to return
        if num_ret != 'all':
            # slice number of rows in dataframe
            self.df = self.df.iloc[:num_ret, :]

        # return dataframe
        return(self.df)

    @staticmethod
    def feat_plot(df_feats, feat_lab='df_idx'):
        '''
        Return plot of positive and negative feature weights for a given model

        Parameters
        ----------
        df_feats : dataframe of a model's feature wieght values and if positive
        feat_lab : labels for features, default is dataframe index
        '''
        # define feature labels
        if feat_lab == 'df_idx':
            feat_lab = df_feats.index

        # initialize plot
        ax = plt.gca()
        # plot feature weights with positive and negative differentiation
        df_feats.iloc[:, 0].plot(kind='bar', ax=ax, color=df_feats.iloc[:, 1]
                                .map({True: 'g', False: 'r'}))
        ax.set_title('Feature Weights')
        ax.set_xlabel('Feature')
        ax.set_ylabel('Model Influence')
        # set x-tick labels to feature labels
        ax.set_xticklabels(feat_lab)

        # positive label for legend
        pos_patch = mpatches.Patch(color='green', label='Positive')
        # negative label for legend
        neg_patch = mpatches.Patch(color='red', label='Negative')
        # display legend
        legend = plt.legend(title='Correlation', handles=[pos_patch, neg_patch])
        legend.get_title().set_fontsize('18')
