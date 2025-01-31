from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class timeRangeEnum(Enum):
    Days = 'Days'
    Months = 'Months'
    Years = 'Years'
    Weeks = 'Weeks'
    Hours = 'Hours'

class EducationLevel(Enum):
    School = 'School'
    UnderGraduate = "UG"
    PostGraduate = "PG"
    PHD = "PHD"
    CompetitiveExam = 'CompetitiveExam'
    SelfStudy = 'SelfStudy'

class StudyTime(Enum):
    Morning = "Morning"
    Afternoon = "Afternoon"
    Evening = "Evening"
    Night = "Night"

class PriorKnowledge(Enum):
    Beginner = "Beginner"
    Intermediate = "Intermediate"
    Advanced = "Advanced"

class PreferredStudyMethods(Enum):
    VideoLectures = "VideoLectures"
    Reading = "Reading"
    PracticeTests = "PracticeTests"
    FlashCards = "FlashCards"

class RevisionFrequency(Enum):
    Daily = "Daily"
    Weekly = "Weekly"
    BeforeExam = "BeforeExam"


class BreakPreferences(Enum):
    Pomodoro = "POMODORO"
    Fifiy_two_seventeen = "FIFTY_TWO_SEVENTEEN"
    Ninetry_Minute_Lifecycle = "NINETY_MINUTE_CYCLE"
    Sixty_Ten = "SIXTY_TEN"
    Flowtime = "FLOWTIME"
    Two_Day_Rule = "TWO_DAY_RULE"
    Reverse_Pomodoro = "REVERSE_POMODORO"

@dataclass
class PromptTypes:
    # basic personalization inputs
    timelimit : timeRangeEnum
    education : EducationLevel
    age : int
    studyHours : int
    studytime : StudyTime

    # study goals and subjects
    prior : PriorKnowledge
    examdate : str
    exam : str

    # study preferences
    method : PreferredStudyMethods
    revision : RevisionFrequency
    breaks : BreakPreferences

    # external constraints
    availablehoursinWeekend : str

@dataclass
class Break:
    after_minutes: int
    break_duration_minutes: int

@dataclass
class BreakSchedule:
    method: str
    breaks: List[Break]

@dataclass
class Topic:
    subject: str
    topic: str
    resources: List[str]
    duration_minutes: int
    difficulty_level: str

@dataclass
class StudyDay:
    date: str  # Format: YYYY-MM-DD
    day_of_week: str
    topics: List[Topic]
    revision_topics: List[str]
    practice_tests: List[str]
    break_schedule: BreakSchedule
    notes: Optional[str] = None

@dataclass
class WeeklySummary:
    total_study_hours: int
    key_focus_areas: List[str]
    recommended_improvements: List[str]

@dataclass
class ExamReadiness:
    current_score: int
    confidence_level: str
    areas_to_improve: List[str]

@dataclass
class StudyPlan:
    timeline: List[StudyDay]
    weekly_summary: WeeklySummary
    exam_readiness_score: ExamReadiness
