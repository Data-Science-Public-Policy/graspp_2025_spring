import os
import re
import json
import spacy
import pandas as pd
from datetime import datetime
from glob import glob
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt

class RawReportsProcessor:

    def __init__(self, input_folder, output_folder=None):
        self.input_folder = input_folder
        self.output_folder = output_folder or os.path.join(input_folder, "parquet_output")
        os.makedirs(self.output_folder, exist_ok=True)
        self.nlp = spacy.load("en_core_web_sm")
        self.skipped_reports = []

    def _normalize_date(self, date_str):
        for fmt in ("%B %Y", "%d %b %Y", "%d %B %Y", "%d %b %Y (%H:%M)", "%d %b %Y (%H:%M:%S)"):
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        return None

    def _extract_country(self, text):
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return ent.text.strip()
        return None

    def _extract_relevant_paragraphs(self, text):
        keywords = ["central bank", "monetary policy", "reserve bank", "national bank"]
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        relevant = []
        for para in paragraphs:
            para_lower = para.lower()
            for keyword in keywords:
                if keyword in para_lower:
                    relevant.append(para)
                    break        
        return "\n---\n".join(relevant) if relevant else None

    def _parse_report_block(self, block, source_file):
        lines = block.strip().splitlines()
        header_line = " ".join(lines[:2]) if len(lines) >= 2 else lines[0] if lines else ""

        country = self._extract_country(header_line)
        if not country:
            return None

        date_match = re.search(r'(\d{1,2} \w+ \d{4})|(\w+ \d{4})', header_line)
        if not date_match:
            return None
        raw_date = date_match.group(0)
        date = self._normalize_date(raw_date)
        if not date:
            return None

        relevant_text = self._extract_relevant_paragraphs(block.strip())

        pressure = self._check_for_pressure(relevant_text)
        threats = self._check_for_threats(relevant_text)
        has_elections = self._check_for_elections(relevant_text)


        if relevant_text is None:
            self.skipped_reports.append({
                'country': country,
                'date': date.isoformat(),
                'reason': 'No relevant keywords found',
                'source_file': source_file
            })

        return {
            'country': country,
            'date': date,
            'relevant_text': relevant_text,
            'pressure': pressure,
            'threats': threats,
            'mentions_elections': has_elections
        }

    def _parse_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        blocks = content.split("____________________________________________________________")
        return [
            report for block in blocks
            if (report := self._parse_report_block(block, os.path.basename(file_path)))
        ]

    def _check_for_pressure(self, text):
        
        if not isinstance(text, str):
            return 0
        t = text.lower()
        if any(k in t for k in [
            "under pressure", "print money", "money printing", "monetize", "succumb",
            "government control", "forced to", "pressure to lower rates"
        ]):
            return 2
        if any(k in t for k in [
            "resist", "reiterated", "independent", "declined", "not considering",
            "maintained independence", "held steady"
        ]):
            return 1
        return 0

    def _check_for_threats(self, text):
        
        if not isinstance(text, str):
            return []

        t = text.lower()
        threats = []
        if any(k in t for k in [
            "legal independence", "revise central bank law", "amend mandate",
            "revoke independence", "constitutional change", "change in mandate"
        ]):
            threats.append("legal_amendment")
        if any(k in t for k in [
            "replace governor", "removed from office", "new central bank head",
            "dismissal", "reshuffle", "appointed", "sacked", "fired"
        ]):
            threats.append("leader_change")
        return threats

    def _check_for_elections(self, text):
        
        if not isinstance(text, str):
            return False
        keywords = ["election", "elections", "vote", "votes", "ballot", "polls", "campaign"]
        return any(k in text.lower() for k in keywords)


    def extract_reports(self):
        all_reports = []
        for file_path in glob(os.path.join(self.input_folder, "*.txt")):
            all_reports.extend(self._parse_file(file_path))
        self.df = pd.DataFrame(all_reports)
        return self.df

    def save_reports_by_country(self):
        
        for country, group in self.df.groupby("country"):
            sorted_group = group.sort_values("date")
            file_name = f"{country.replace(' ', '_').lower()}.parquet"
            output_path = os.path.join(self.output_folder, file_name)
            sorted_group.to_parquet(output_path, index=False)

    def save_skipped_log(self):
        if self.skipped_reports:
            log_path = os.path.join(self.output_folder, "skipped_reports.json")
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(self.skipped_reports, f, ensure_ascii=False, indent=2)

    def generate_wordcloud(self, country_name=None, save_path=None, ax=None):

        if not country_name:
            target_df = self.df
            country_name = "All Countries"
        else:
            target_df = self.df[self.df['country'] == country_name]

        # Drop nulls in relevant_text
        target_df = target_df.dropna(subset=['relevant_text'])

        vectorizer = CountVectorizer(
            analyzer='word',
            stop_words='english',
            lowercase=True,
            ngram_range=(1, 3),
            min_df=0.1  # Exclude rare phrases
        )

        counts = vectorizer.fit_transform(target_df['relevant_text']).toarray().sum(axis=0)
        word_freq = dict(zip(vectorizer.get_feature_names_out(), counts))

        wordcloud = WordCloud(width=800, height=400, background_color='white')
        wordcloud.generate_from_frequencies(word_freq)

        if ax:
            ax.imshow(wordcloud)
            ax.axis('off')
            ax.set_title(f"Word Cloud for {country_name}", size=20)
        else:
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud)
            plt.axis('off')
            plt.title(f"Word Cloud for {country_name}", size=20)

            if save_path:
                plt.savefig(save_path)
            else:
                plt.show()

    def plot_pressure_histogram_by_year(self, country=None):
        
        df = self.df.copy()

        if not country is None:
            df = df[df["country"] == country]

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year

        df_filtered = df[df['pressure'].isin([1, 2])]

        # Count per year per category
        counts = df_filtered.groupby(['year', 'pressure']).size().unstack(fill_value=0)
        counts.columns = ['1', '2']
        counts['total'] = counts.sum(axis=1)

        # Plot all three as side-by-side bars
        counts[['1', '2', 'total']].plot(
            kind='bar',
            figsize=(12, 6),
            color=['#1f77b4', '#ff7f0e', '#2ca02c']
        )
        plt.title("Central Bank Pressure Reports by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Reports")
        plt.legend(title="Category")
        plt.tight_layout()
        plt.show()

    def plot_threats_by_year(self, country=None):
       
        df = self.df.copy()

        if not country is None:
            df = df[df["country"] == country]

        df = self.df.copy()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year

        # Expand threat list into separate rows
        df_threats = df.explode('threats')
        threat_counts = df_threats.dropna(subset=['threats']).groupby(['year', 'threats']).size().unstack(fill_value=0)

        # Plot threats
        threat_counts.plot(kind='bar', figsize=(12, 5), colormap='Set2')
        plt.title("Frequency of Threats to Central Bank Independence by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Reports")
        plt.tight_layout()
        plt.show()

    def plot_elections_by_year(self, country=None):
        
        df = self.df.copy()

        if not country is None:
            df = df[df["country"] == country]

        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['year'] = df['date'].dt.year

        # Count election mentions
        election_counts = df[df['mentions_elections']].groupby('year').size()

        # Plot elections
        election_counts.plot(kind='bar', figsize=(12, 5), color='cornflowerblue')
        plt.title("Reports Mentioning Elections by Year")
        plt.xlabel("Year")
        plt.ylabel("Number of Reports")
        plt.tight_layout()
        plt.show()

    def run(self):
        self.extract_reports()
        self.save_reports_by_country()
        self.save_skipped_log()
        self.generate_wordcloud()
        self.plot_pressure_histogram_by_year()
        self.plot_threats_by_year()
        self.plot_elections_by_year()
        return self.df
