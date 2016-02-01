from django.contrib import admin
from api.models import ImageUpload
from api.models import BannedDomain
from api.models import BannedIP
from api.models import BannedWord
from api.models import SavingsGoal
from api.models import CreditGoal
from api.models import FinalGoal
#from api.models import Badge 
from api.models import XPLevel
#from api.models import Course
#from api.models import Quiz
#from api.models import Question
from api.models import EnrolledCourse
from api.models import QuizSubmission
from api.models import QuestionSubmission
from api.models import Me


admin.site.register(ImageUpload)
admin.site.register(BannedDomain)
admin.site.register(BannedIP)
admin.site.register(BannedWord)
admin.site.register(SavingsGoal)
admin.site.register(CreditGoal)
admin.site.register(FinalGoal)
admin.site.register(XPLevel)
admin.site.register(EnrolledCourse)
admin.site.register(QuizSubmission)
admin.site.register(QuestionSubmission)
admin.site.register(Me)


