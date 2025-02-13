## Web Scraping Project for the English Live Platform

This project is a web scraping solution developed to extract information from English Live (englishlive.com), specifically focused on lessons and feedbacks. The scraped data is structured with the following columns:

- **Date**: The date when the lesson or feedback was recorded.
- **Title**: The title of the lesson or feedback.
- **Type**: The type of lesson or feedback (e.g., course, student review, etc.).
- **Score**: The feedback rating or score.
- **Teacher**: The name of the teacher associated with the lesson.

The extracted data is structured and can be consumed by any Business Intelligence (BI) tool for further analysis and visualization. You can also use the provided Power BI template file (`EF Projeto.pbix`) available in the repository to easily consume and visualize the data.

### Project Overview
The goal of this project was to automate the extraction of lessons and feedback data from the platform in order to process and analyze it more efficiently. The extracted data includes:

- Course lessons
- Student feedbacks
- Lesson details and feedback ratings

### Data Consumption
You can consume the output of this project with any BI tool, such as:

- **Power BI** (you can use the provided **Power BI template file** `EF Projeto.pbix` in the repository to easily consume and visualize the data)
- **Tableau**
- **Excel**
- **Knime Analytics**

Simply import the resulting file into your BI tool of choice to start analyzing the data and uncover insights.

### Features
- **Automated Data Extraction:** Web scraping script to retrieve course and feedback data from English Live.
- **Data Structuring:** Clean, structured data with Date, Title, Type, Score, and Teacher columns ready to be loaded into BI tools.
- **Customizable:** Modify the script to adjust to any changes on the platform or to extract different data.
- **Power BI Integration:** Use the provided **Power BI template file** (`EF Projeto.pbix`) for easy consumption and visualization of the data.

### Requirements
- Python 3.x
- Libraries:
  - **PyQt5**
  - **Selenium**
  - **Pandas**

### How to Run
1. Clone the repository.
2. Install the required libraries by running:
   ```bash
   pip install -r requirements.txt
