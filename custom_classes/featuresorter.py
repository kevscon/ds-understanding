import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class FeatureSort:
    '''
    Sort (in descending order) feature importances for machine learning models

    Parameters
    ----------
    weights : array of feature weights from model
    labels : list of feature labels
    '''

    def __init__(self, weights, labels):
        self.weights = weights
        self.labels = labels

    def wgts(self, num_ret='all', ret_0=False):
        '''
        Create dataframe of features x weights

        Parameters
        ----------
        num_ret : number of top features to return
        ret_0 : return weights with value of zero
        '''
        # create feature weight dataframe
        self.df =  pd.DataFrame(self.weights, index=self.labels, columns=['feat_wgt']).copy()

        # 0 values
        if ret_0 == False:
            # drop weights == 0
            self.df = self.df[self.df.iloc[:, 0] != 0]

        # top number of features to return
        if num_ret != 'all':
            # slice number of rows in dataframe
            self.df = self.df.iloc[:num_ret, :]

        # return unsorted weight dataframe
        return(self.df)

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
        # create column identifying positive weights
        self.df['positive'] = self.df['feat_wgt'] > 0

        # 0 values
        if ret_0 == False:
            # drop weights == 0
            self.df = self.df[self.df.iloc[:, 0] != 0]

        # top number of features to return
        if num_ret != 'all':
            # slice number of rows in dataframe
            self.df = self.df.iloc[:num_ret, :]

        # return sorted weight dataframe
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

        # return sorted and absolute value weight dataframe
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

        # return sorted percentage dataframe
        return(self.df)

    def imp_plot(self, feat_lab='df_idx',  title='Feature Importance',
        xlab='Feature', ylab='Model Influence'):
        '''
        Return bar plot of model importances. No account of direction.
        Input is based on last class method run

        Parameters
        ----------
        feat_lab : labels for features, default is dataframe index
        title : title for bar plot
        xlab : title for x-axis labels
        ylab : title for y-axis labels
        '''
        # initialize plot
        ax = plt.gca()

        # bar plot feature importances
        self.df.iloc[:, 0].plot(kind='bar', color='darkgoldenrod')

        # set labels
        ax.set_title(title)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        # set feature labels
        if feat_lab != 'df_idx':
            ax.set_xticklabels(feat_lab)

    def wgt_plot(self, feat_lab='df_idx',  title='Feature Weights',
        xlab='Feature', ylab='Model Influence', rev_col=False):
        '''
        Return bar plot of model feature weights. Takes into account direction.
        Input is based on last class method run

        Parameters
        ----------
        feat_lab : labels for features, default is dataframe index
        title : title for bar plot
        xlab : title for x-axis labels
        ylab : title for y-axis labels
        rev_col : option to reverse positive/negative plot coloring
        '''

        # define pos/neg plot coloring
        if rev_col:
            pos_col = 'darkred'
            neg_col = 'darkgreen'
        else:
            pos_col = 'darkgreen'
            neg_col = 'darkred'

        # initialize plot
        ax = plt.gca()

        # bar plot feature weights with positive and negative differentiation
        self.df.iloc[:, 0].plot(kind='bar', ax=ax, color=self.df.iloc[:, 1]
                                .map({True: pos_col, False: neg_col}))

        # set labels
        ax.set_title(title)
        ax.set_xlabel(xlab)
        ax.set_ylabel(ylab)
        # set feature labels
        if feat_lab != 'df_idx':
            ax.set_xticklabels(feat_lab)

        # positive label for legend
        pos_patch = mpatches.Patch(color='green', label='Positive')
        # negative label for legend
        neg_patch = mpatches.Patch(color='red', label='Negative')
        # display legend
        legend = plt.legend(title='Correlation', handles=[pos_patch, neg_patch])
