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


class NLProcess:

    def __init__(self, doc_tops, top_labels, doc_labels):
        self.doc_tops = doc_tops
        self.top_labels = top_labels
        self.doc_labels = doc_labels

    def top_wgts(self):
        '''
        create dataframe of documents x weights

        Parameters
        ----------
        doc_tops : array of topic weights for each document
        top_labels : dictionary of topic #: topic label
        doc_labels : list of document labels
        '''
        # create dataframe of topic weights
        self.top_df = pd.DataFrame(self.doc_tops).copy()
        # map topic # to topic labels and set as columns
        self.top_df.columns = self.top_df.columns.map(self.top_labels)
        # set index to document labels
        self.top_df.set_index(self.doc_labels, inplace=True)
        # return weight dataframe
        return(self.top_df)

    def prcntg(self):
        '''
        convert weights to percentage of topic
        '''
        # convert weights to percentage
        self.prcntg_df = self.doc_top_df.div(self.doc_top_df.sum(axis=1), axis=0).copy()
        # drop any NaN values from dataframe
        self.prcntg_df.dropna(inplace=True)
        # return percentage dataframe
        return(self.prcntg_df)
