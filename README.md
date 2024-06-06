# Artificial Intelligence Based Patent Search System

## Introduction
The Artificial Intelligence Based Patent Search System is a cutting-edge solution designed to revolutionize the way researchers and innovators navigate the ever-expanding landscape of patents. With record-breaking numbers of patent applications filed worldwide each year, efficiently searching through this vast resource has become a critical challenge. Our system leverages state-of-the-art natural language processing and information retrieval techniques, specifically tailored for the complex language used in patents.

## Features
- Domain-specific language model, PatentSBERTa, trained on patent data
- High-dimensional vector representations capturing semantic meaning and relationships
- Efficient vector-based search using ElasticSearch
- KNN (k-Nearest Neighbors) algorithm with cosine similarity for retrieving relevant patents
- Excels at handling real-world queries, synthetic queries created by language models, and patent research reports prepared by experts

## Dataset
Our system utilizes a custom dataset of patent documents, focusing on the top 100 companies in the aerospace industry. The text data undergoes rigorous pre-processing, including:
- Translation to English
- Removal of incomplete patents
- Cleaning of irrelevant characters and figures

## Technical Details
1. Data pre-processing:
   - Translation, cleaning, and removal of incomplete patents
2. Vector representation:
   - PatentSBERTa transformer model converts text into high-dimensional vectors
   - Captures semantic meaning and relationships using attention mechanisms
3. Database:
   - ElasticSearch used as a vector database for efficient search
4. Search algorithm:
   - KNN (k-Nearest Neighbors) with cosine similarity retrieves relevant patents

## Results
Our system, powered by the domain-specific PatentSBERTa model, outperforms traditional methods and general-purpose language models in terms of precision, recall, and MRR. It excels at handling various types of queries, including:
- Real-world queries (precision: 67.4%, recall: 46.6%)
- Synthetic queries created by language models (precision: 61.7%, recall: 63.5%)
- Patent research reports prepared by experts (precision: 41.6%, recall: 40.2%)

## Future Improvements
- Expanding to more technical domains beyond aerospace
- Integrating the search system with a patent classification model
- Adding multimodal capabilities
- Investigating user-driven query reformulation

## Contributors
- Buğra Şimşek
- Onur Demirel
- Ali Kemal Tamkoç
- Behiç Kılınçkaya
