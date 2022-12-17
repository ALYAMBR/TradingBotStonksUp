import pickle
import datetime
    
class Pipeline:
    """
    Serializable pipeline for classifying the 
    direction of the closing price movement
    """
    def __init__(self, clf, window):
        """
        Parameters
        ----------
        clf
            Classifier that predicts the direction of the 
            closing price movement for the next timeframe
        window: int
            Window length in timeframes used for prediction
        """
        self.__clf = clf
        self.__window_size = window
        
    def save(self, path):
        """
        Saves the pipeline in binary form to the file specified in the path
        
        ...
        Parameters
        ----------
        path
            Pipeline save path
        """
        with open(path, "wb") as fout:
            pickle.dump(self, fout)
            
    @staticmethod
    def load(path):
        """
        Loads a pipeline from a file specified in the path
        
        ...
        Parameters
        ----------
        path
            Pipeline load path
            
        Returns
        -------
        Pipeline
            Ready to use pipeline object
        """
        with open(path, "rb") as fin:
            pipeline = pickle.load(fin)
        return pipeline
    
    def predict(self, df):
        """
        Predicts the direction of the closing 
        price movement for the next timeframe
        
        ...
        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with following columns: 
                <TICKER>
                <PER>
                <DATE>
                <TIME>
                <OPEN>
                <HIGH>
                <LOW>
                <CLOSE>
                <VOL>
            
            Must contain at least `window` rows
            
        Returns
        -------
        int
            1 if next closing price greater or equal to current
            0 otherwise
        """
        X = self.__preprocess(df)
        prediction = int(self.__clf.predict([X])[0])
        return prediction
    
    def __preprocess(self, df):
        """
        Preprocess the dataframe for submission to the classifier
        
        ...
        Parameters
        ----------
        df: pd.DataFrame
            Dataframe with following columns: 
                <TICKER>
                <PER>
                <DATE>
                <TIME>
                <OPEN>
                <HIGH>
                <LOW>
                <CLOSE>
                <VOL>
            
            Must contain at least `window` rows
            
        Returns
        -------
        np.ndarray
            Array of features ready for use by the classifier
        """
        df = df.drop(columns=["<TICKER>", "<PER>", "<DATE>", "<TIME>"])
        window = df[-self.__window_size:]
        X = window.values.reshape(-1)
        return X