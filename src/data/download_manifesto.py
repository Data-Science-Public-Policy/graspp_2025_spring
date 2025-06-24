import requests
import pandas as pd

class DownloadManifesto:
    def __init__(self, dataset_key, version, api_key):
        self.dataset_key = dataset_key
        self.version = version
        self.api_key = api_key
        self.base_url = "https://manifesto-project.wzb.eu/api/v1/"

    def _api_call(self, endpoint, params=None):
        """Make API call and return JSON response or None if failed"""
        params = params or {}
        params["api_key"] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)
        return response.json() if response.status_code == 200 else None
    
    def get_country_data(self, country):
        """Get core data filtered by country with party keys"""
        data = self._api_call("get_core", {"key": self.dataset_key})
        if not data:
            return None
            
        df = pd.DataFrame(data[1:], columns=data[0])
        df = df[df['countryname'] == country][['countryname', 'party', 'partyname', 'date']].copy()
        df['keys'] = df['party'] + '_' + df['date']
        return df
    
    def get_metadata(self, df):
        """Get metadata and add manifesto IDs to dataframe"""
        metadata = self._api_call("metadata", {"keys[]": df['keys'].tolist(), "version": self.version})
        if not metadata:
            return df, None
            
        # Create ID mapping and add to dataframe
        id_map = {item['manifesto_id']: item['manifesto_id'] 
                 for item in metadata.get('items', []) if item.get('manifesto_id')}
        df['manifesto_id'] = df['keys'].map(id_map)
        
        return df, metadata
    
    def get_texts(self, df):
        """Get texts and merge with dataframe (requires manifesto_id column)"""
        if 'manifesto_id' not in df.columns:
            raise ValueError("DataFrame must have 'manifesto_id' column. Call get_metadata() first.")
            
        valid_ids = [mid for mid in df['manifesto_id'].dropna().unique()]
        if not valid_ids:
            return df
            
        texts_data = self._api_call("texts_and_annotations", 
                                   {"keys[]": valid_ids, "version": self.version})
        
        # Extract and map texts
        texts = {}
        if texts_data:
            for item in texts_data.get('items', []):
                key = item.get('key')
                text_items = item.get('items', [])
                texts[key] = ' '.join(text_item.get('text', '') for text_item in text_items)
        
        df['text'] = df['manifesto_id'].map(texts)
        return df.dropna().set_index(['countryname', 'date'])

# Usage example:
# downloader = ManifestoDownloader(dataset_key, version, api_key)
# result = downloader.get_country_data("Germany")
# final_data = downloader.get_texts(result)
