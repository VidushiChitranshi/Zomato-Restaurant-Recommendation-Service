import pandas as pd
from datasets import load_dataset
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ZomatoLoader:
    """
    Phase 1: Data Acquisition
    Loads and cleans the Zomato restaurant dataset from Hugging Face.
    """
    
    DATASET_NAME = "ManikaSaini/zomato-restaurant-recommendation"
    REQUIRED_COLUMNS = [
        "name", 
        "location", 
        "rate", 
        "approx_cost(for two people)", 
        "cuisines"
    ]

    def load_data(self) -> pd.DataFrame:
        """
        Loads the dataset from Hugging Face and returns it as a DataFrame.
        """
        try:
            logger.info(f"Loading dataset: {self.DATASET_NAME}")
            dataset = load_dataset(self.DATASET_NAME, split='train')
            df = dataset.to_pandas()
            return df
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            raise RuntimeError(f"Could not load dataset from Hugging Face: {e}")

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Performs preprocessing and cleaning on the dataset.
        """
        logger.info("Starting data cleaning...")
        
        # 1. Drop duplicate rows
        df = df.drop_duplicates()
        
        # 1b. Drop duplicate restaurant names to ensure variety
        df = df.drop_duplicates(subset=['name'])

        # 2. Schema Validation: Check if required columns exist
        missing_cols = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in dataset: {missing_cols}")

        # 3. Clean 'rate' column (format is 'x/5' or 'NEW' or '-')
        def parse_rate(val):
            if pd.isna(val) or val == "NEW" or val == "-":
                return None
            try:
                # Extract the numeric part before '/5'
                return float(str(val).split('/')[0])
            except (ValueError, IndexError):
                return None

        df['rate'] = df['rate'].apply(parse_rate)

        # 4. Clean 'approx_cost(for two people)' column (format is '1,200')
        def parse_cost(val):
            if pd.isna(val):
                return None
            try:
                # Remove commas and convert to float
                return float(str(val).replace(',', ''))
            except ValueError:
                return None

        df['approx_cost(for two people)'] = df['approx_cost(for two people)'].apply(parse_cost)

        # 5. Handle null values for essential columns
        # Drop rows where name or location is null
        df = df.dropna(subset=['name', 'location'])
        
        # Fill missing numeric values with 0 or a median (here we keep them as None/NaN for search logic)
        
        logger.info(f"Cleaned data. Final row count: {len(df)}")
        return df

    def get_structured_data(self, export_csv: bool = False, output_path: str = "cleaned_zomato.csv") -> pd.DataFrame:
        """
        Orchestration method for Phase 1.
        Favors local CSV if it exists to speed up deployment/loading.
        """
        # Check if local cleaned data exists
        if os.path.exists(output_path):
            logger.info(f"Loading data from local cache: {output_path}")
            return pd.read_csv(output_path)

        # Fallback to Hugging Face if local file not found
        logger.info("Local data not found. Downloading from Hugging Face...")
        raw_df = self.load_data()
        clean_df = self.clean_data(raw_df)
        structured_df = clean_df[self.REQUIRED_COLUMNS]

        if export_csv:
            structured_df.to_csv(output_path, index=False)
            logger.info(f"CSV exported successfully to {output_path}")

        return structured_df


if __name__ == "__main__":
    # Quick sanity check
    loader = ZomatoLoader()
    try:
        data = loader.get_structured_data(export_csv=True)

        print(data.head())
    except Exception as err:
        print(f"Error during manual run: {err}")
