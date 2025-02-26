# 📝 AI-Powered Resume Matcher  

🚀 **An AI-powered tool that analyzes resumes against job descriptions, provides match scores, identifies missing skills, and suggests improvements.**  

## 📌 Overview  

Finding a job is tough, especially when your resume doesn't pass Applicant Tracking Systems (ATS) or doesn't highlight the right skills.  
This project uses **LLMs (GPT-4-turbo), embeddings, and cosine similarity** to analyze resumes and provide **actionable feedback**.  

## ✅ Features  

- 📝 **Upload Resume (PDF/DOCX)**  
- 🏢 **Paste Job Description**  
- 🔎 **Get Match Score (%)**  
- 💡 **Identify Missing Skills**  
- 📈 **Receive Resume Improvement Suggestions**  
- ✍️ **Generate a Tailored Cover Letter**  

## ⚙️ How It Works  

1. **Extracts text from resumes** (PDF or DOCX).  
2. **Embeds both resume & JD using OpenAI embeddings**.  
3. **Calculates similarity score** via cosine similarity.  
4. **Uses GPT-4-turbo** to provide **feedback on strengths, missing skills, and improvements**.  
5. **Outputs a sample cover letter** based on the resume & JD.  

## 📾 Installation & Setup  

1️⃣ **Clone the repository**  
```bash
git clone https://github.com/your-username/resume-matcher.git
cd resume-matcher
```

2️⃣ **Create a virtual environment & install dependencies**  
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

3️⃣ **Set up OpenAI API key**  
```bash
export OPENAI_API_KEY="your-api-key-here"
```

4️⃣ **Run the Streamlit app**  
```bash
streamlit run app.py
```

## 🎯 Usage  

- **Upload your resume** (PDF or DOCX).  
- **Paste a job description** in the text box.  
- Click **"Analyze Resume"** and get results:  
  - **Match Score** (% similarity).  
  - **Key strengths** in your resume.  
  - **Missing skills** that can improve your match.  
  - **Actionable recommendations** to optimize your resume.  
  - **A tailored cover letter** to use in your application.  

## 🛠️ Technologies Used  

- **Python** 🐍  
- **Streamlit** 🎨 (UI)  
- **OpenAI GPT-4-turbo** 🤖 (LLM for feedback & cover letter)  
- **LangChain** 🔗 (Embeddings)  
- **scikit-learn** 📊 (Cosine similarity)  
- **pdfplumber & docx2txt** 📝 (Resume text extraction)  

## 🤝 Contributing  

Feel free to fork this repo and contribute! 🚀  

## 🐝 License  

This project is licensed under the **MIT License**.  

---  

🚀 **Optimizing resumes with AI – helping job seekers land their dream jobs!**

