import numpy as np
import pandas as pd

# print top words of topic model
def print_top_words(word_matrix, feature_names, n_top_words):
    for index, topic in enumerate(word_matrix):
        message = "\nTopic #{}:".format(index)
        message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1 :-1]])
        print(message)
        print("="*70)


def top_wgts(doc_tops, top_labels, doc_labels):
    '''
    create dataframe of documents x weights

    Parameters
    ----------
    doc_tops : array of topic weights for each document
    top_labels : dictionary of topic #: topic label
    doc_labels : list of document labels
    '''

    top_df = pd.DataFrame(doc_tops)
    top_df.columns = top_df.columns.map(top_labels)
    top_df.set_index(doc_labels, inplace=True)
    return(top_df)


def prcntg(doc_top_df):
    '''
    convert weights to percentage of topic

    Parameters
    ----------
    doc_top_df : documents x weights dataframe
    '''

    prcntg_df = doc_top_df.div(doc_top_df.sum(axis=1), axis=0)
    prcntg_df.dropna(inplace=True)
    return(prcntg_df)


class TopClass:

    def __init__(self, doc_tops):
        # array of topic weights for each document
        self.doc_tops = doc_tops

    def top_wgts(self, top_labels='', doc_labels=''):
        '''
        return dataframe of documents x weights

        Parameters
        ----------
        top_labels : list of topic description labels
        doc_labels : list of document labels
        '''
        # create dataframe object of documents x weights
        self.top_df = pd.DataFrame(self.doc_tops).copy()
        if top_labels:
            # set columns as topic labels
            self.top_df.columns = top_labels
        if doc_labels:
            # set index to document labels
            self.top_df.set_index([doc_labels], inplace=True)
        # return weight dataframe
        return(self.top_df)

    def top_pct(self, top_labels='', doc_labels=''):
        '''
        convert topic weights to percentage of document

        Parameters
        ----------
        top_labels : list of topic description labels
        doc_labels : list of document labels
        '''
        # create dataframe object of documents x weights
        self.top_df = pd.DataFrame(self.doc_tops).copy()
        # convert weights to proportion
        self.top_df = self.top_df.div(self.top_df.sum(axis=1), axis=0).copy()
        # round to percentage
        self.top_df = self.top_df.apply(lambda x: round(x * 100, 1))
        if top_labels:
            # set columns as topic labels
            self.top_df.columns = top_labels
        if doc_labels:
            # set index to document labels
            self.top_df.set_index([doc_labels], inplace=True)
        # return percentage dataframe
        return(self.top_df)

    def sort_tops(self, doc_labels=''):
        '''
        sort topics by weight per document in descending order

        Parameters
        ----------
        doc_labels : list of document labels
        '''
        # dataframe of weight values
        sort_val = self.top_df.values.copy()
        # sort rows by value (ascending order)
        sort_val.sort(axis=1)
        # reverse values in rows (descending order)
        sort_val = np.flip(sort_val, axis=1)
        # create dataframe
        sort_val = pd.DataFrame(sort_val)
        # sort labels by weight
        sort_lab = pd.DataFrame(self.top_df.columns[np.argsort(-self.top_df.values,
            axis=1)])
        # concatenate dataframes and interweave columns
        sort_df = pd.concat([sort_lab, sort_val], axis=1)[np.arange(len(self.top_df.columns))]
        # create hierarchical column names
        multi_idx = pd.MultiIndex.from_product([np.arange(len(self.top_df.columns)),
            ['Label', 'Weight']])
        # set column labels
        sort_df = pd.DataFrame(sort_df.values, columns=multi_idx)
        if doc_labels:
            # set index to document labels
            sort_df.set_index([doc_labels], inplace=True)
        # return dataframe
        return(sort_df)
