from typing import Dict, List


SUBJECT_VARIATIONS: Dict[str, List[str]] = {
    "science": ["Science", "SCIENCE", "Science-Standard"],
    "maths": [
        "Mathematics", "MATHEMATICS", "Maths", "MATHS", 
        "MathsStandard", "Maths-Standard", "Mathematics-Standard",
        "MathsBasic", "Maths-Basic", "Mathematics-Basic"
    ],
    "english": ["English", "ENGLISH", "English-Language-and-Literature", "EnglishL"],
    "sst": [
        "Social-Science", "SOCIAL_SCIENCE", "Social_Science", "SS", "Social Science",
        "SocialScience"  
    ],
    "hindi-b": [
        "Hindi-B", "HINDI-B", "Hindi B", "HINDI B", 
        "HindiCourseB", "Hindi-Course-B", "Hindi_Course_B"
    ]
}


BASE_URL_PATTERNS: List[str] = [
    "ClassX_{year}/{subject}-SQP.pdf",
    "CLASS_X_{year}/X_{subject}_SQP_{year}.pdf",
    "ClassX_{year}/{subject}_SQP.pdf",
    "Class_X_{year}/{subject}-SQP.pdf",
    "Class_X_{year}/{subject}_SQP_{year}.pdf",
    "CLASS_X_{year}/{subject}_SQP.pdf",
    "CLASS%20X_{year}/{subject}%20SQP%20({year}).pdf",
    "CLASS%20X_{year}/SQP%20of%20{subject}%20({year}).pdf",
    "CLASS%20X_{year}/{subject}%20Class%20X%20QP.pdf",
    "CLASS%20X_{year}/SQP%20{subject}%20set%20-I%20class%20X.pdf",
    "CLASS%20X_{year}/SQP%20{subject}%20set%20-II%20class%20X.pdf",
]


SUBJECT_SPECIFIC_PATTERNS: Dict[str, List[str]] = {
    "sst": [

        "CLASS_X_{year}/X-SS_SQP_{year}.pdf",
        "CLASS%20X_{year}/SQP%20of%20Social%20Science%20SQP%20({year}).pdf",
        "CLASS_X_{year}/Social_Science_SQP_{year}.pdf",
        "CLASS_X_{year}/SST_SQP_{year}.pdf",
        "ClassX_{year}/Social-Science-SQP.pdf",

        "ClassX_{year}/SocialScience-SQP.pdf",
        "CLASS%20X_{year}/Social%20Science/Social%20Science%20SQP%20_{year}_%20Set%201.pdf",
        "CLASS%20X_{year}/Social%20Science/Social%20Science%20SQP%20_{year}_%20Set%202.pdf",
        "CLASS_X_{year}/X-SS_SQP_{year}-{year}.pdf",  # Format for 2018-19 style

        "CLASS%20X_{year}/Social%20Science/Social%20Science%20SQP%20_{year}.pdf",
        "CLASS%20X_{year}/Social%20Science/SST%20SQP%20_{year}.pdf",
    ],
    "hindi-b": [
        "CLASS_X_{year}/X-Hindi-B_SQP_{year}.pdf",
        "CLASS%20X_{year}/Hindi-B%20Class%20X%20QP.pdf",
        "ClassX_{year}/Hindi-B-SQP.pdf",
        "CLASS_X_{year}/Hindi_B_SQP_{year}.pdf",
        "Class_X_{year}/Hindi-B_SQP.pdf",
        "ClassX_{year}/HindiCourseB-SQP.pdf"
    ],
    "maths": [
        "ClassX_{year}/MathsStandard-SQP.pdf",
        "ClassX_{year}/MathsBasic-SQP.pdf",
        "CLASS%20X_{year}/Maths/SQP%20Maths%20set%20-I%20class%20X.pdf",
        "CLASS%20X_{year}/Maths/SQP%20Maths%20set%20-II%20class%20X.pdf"
    ]
}