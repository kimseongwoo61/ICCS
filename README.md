# **Illegal Content Monitoring System**
## **Introduction**

> The Illegal Content Monitoring Support System is a support system that identifies and takes proactive measures against suicide-related harmful and provocative information in real-time. It complements the ongoing government initiative of 'Public Participation in Suicide Harmful Information Monitoring' and efficiently performs the task of monitoring illegal content using machine learning and artificial intelligence technologies.
> 

## **Key Features**

1. **Google Vision Image Verification**
    - Evaluates the harmfulness of input images using the Google Vision API.
    - The API classifies content as harmful if it scores above a certain threshold based on five elements: adult, medical, spoofed, violence, and racy.
2. **Blacklist Keyword Verification and Keyword Extraction**
    - Examines Korean text extracted from web pages for blacklist keywords to determine harmfulness.
3. **Suicide-related Content Analysis Report Generation**
    - Provides a report of content harmfulness test results and efficiently manages harmful web pages with search result reports.
4. **GUI Service for Enforcement Officers**
    - Enhances user convenience by providing login, registration, enforcement support pages, and an administrator-only page.

## Installation and Run

To start the Illegal Content Monitoring System, follow these steps:

1. **Clone the repository:**
    
    ```bash
    git clone https://github.com/kimseongwoo61/ICCS.git
    ```
    
2. **Install external dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Run the Django server:**
    
    ```bash
    cd ./main
    python manage.py runserver 8080
    ```
    
4. **Access browser** 
    
    ```bash
    http://127.0.0.1:8080
    ```
    

## **Secure Coding and Vulnerability Management**

- Development is based on the Ministry of Public Administration and Security's secure coding guide for secure coding and vulnerability management.
- The STRIDE model was used to identify attack surfaces, and the Microsoft Threat modeling tool was used to measure risks.
- Bandit, a static code analysis tool, was used to inspect vulnerability patterns, and web inspection support tools such as ZAP and BurpSuite were utilized to identify and address vulnerabilities.

## **References**

- **Online Suicide Information Analysis Cases**
    - [Korea Press Foundation, 2021 Social Media User Survey](https://www.kpf.or.kr/front/board/boardContentsView.do?board_id=246&contents_id=62666fac70c2463c879c3a34fc12b364)
    - [Today's Best, Real-time Community Rankings](https://todaybeststory.com/ranking_current.html)
- **Legal Information**
    - [Korea Foundation for Suicide Prevention, Monitoring Team Protects Life](https://sims.kfsp.or.kr/)
    - [OpenNet, Guidelines for Managing Information Mediators' Posts](https://www.opennet.or.kr/21200)
