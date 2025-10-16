# Restaurant Retention Analysis

Data-driven insights into restaurant staff retention, engagement, and performance.

## Overview

This project was developed in collaboration with a local company seeking to understand and address staff retention challenges in local restaurants. The goal was to identify key factors driving employee turnover and engagement using real workforce and operational data.

As part of this work, I built an analytical framework in Python to:
* Model frequency, recency, and monetary (FRM) behavior of staff
* Correlate these metrics with retention and performance outcomes
* Provide actionable insights for management to improve staff satisfaction and retention

This project ultimately led to my hiring by the company to help expand their internal analytics capabilities and data-driven decision-making.

## Objectives

* Identify patterns in staff attendance, performance, and engagement
* Highlight predictive indicators of employee turnover
* Visualize trends across multiple restaurants and job roles
* Recommend strategies for improving retention through data analysis

## Methods & Tools

### Core Components

* **Frequency–Recency Analysis** (`FreRecAnalysis.py`)  
  Calculates key engagement metrics to measure staff consistency and tenure health.
* **Monetary Value Analysis** (`MVAnalysis.py`)  
  Analyzes individual and group performance from a cost–value standpoint.
* **Customer/Employee Cohort Reports** (`CustAnalysisReport.py`)  
  Generates reports summarizing workforce trends and retention metrics.
* **Testing Scripts**  
  Validate model accuracy and logic for each analytical component.

### Technical Stack

* **Language:** Python 3.12
* **Libraries:** pandas, numpy, matplotlib, seaborn, scikit-learn (see `requirements.txt`)
* **Environment:** Local virtual environment (`venv`), compatible with Jupyter and command-line execution

## Usage

1. Clone the repository:
```bash
git clone https://github.com/RachSchoenberg/Final-Project-CS5001.git
cd Final-Project-CS5001
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run analysis scripts:
```bash
python3 "Project Code Files/FreRecAnalysis.py"
python3 "Project Code Files/MVAnalysis.py"
```

5. Generate retention reports or visualizations:
```bash
python3 "Project Code Files/CustAnalysisReport.py"
```

## Example Insights

* Identified correlations between shift frequency and long-term retention
* Detected significant drop-offs in staff engagement following schedule volatility
* Produced clear, interpretable visualizations for decision-makers

## Future Work

* Integrate with live restaurant management systems (POS & scheduling)
* Add predictive modeling for turnover risk
* Develop a lightweight dashboard for ongoing tracking

## Author

**Rachel Schoenberg**  
Masters Student, Data Science | Go-To-Market Manager  
Focused on applied analytics, workforce optimization, and product strategy

[LinkedIn](https://www.linkedin.com/in/rachellschoenberg-a80a88117/) | [GitHub](https://github.com/RachSchoenberg)
