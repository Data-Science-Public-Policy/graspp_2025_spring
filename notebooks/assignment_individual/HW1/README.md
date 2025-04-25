# GRASSP2025_AgriEcon
# Food Expenditure and Income Analysis — Based on Japanese Household Survey Data

This project analyzes food expenditure patterns using data from the Japanese Household Survey. The focus is on two main food categories: **staple foods** (e.g., rice, wheat) and **meat products** (e.g., fresh and processed meat), across **five income levels**.

## 🎯 Objective

The goal of this project is to examine how income levels affect the consumption of staple foods and meat. In particular, the analysis aims to test **Bennett’s Law** in economics:

> *As income rises, the proportion of calories consumed from starchy staple foods decreases, while the consumption of more nutritious, higher-value foods (like meat) increases.*

## 📊 Data Processing Workflow

- **Source**: Official Japanese Household Survey data (Excel format)
- **Selection**: Extracted staple food and meat expenditure data for five income groups
- **Cleaning**: Removed irrelevant columns and missing data
- **Merging**: Combined the staple and meat datasets into a single DataFrame for analysis
- **Reshaping**: Converted wide-format tables into long-format to facilitate regression analysis

## 🧪 Usage

To reproduce the data processing steps and generate the merged dataset:

