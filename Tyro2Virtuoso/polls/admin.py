from django.contrib import admin

from .models import Question, Choice

# admin.StackedInline for stacked choices
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    
    # You can even add methods to display
    list_display = ["question_text", "pub_date", "was_published_recently"]
    
    # Filtering in admin
    list_filter = ["pub_date"]
    
    # Inlines of choice model which has a fk to Questions Model
    inlines = [ChoiceInline]
    
    # When somebody enters search terms, Django will search the question_text field.
    # You can use as many fields as you’d like – although because it uses a LIKE query behind the scenes,
    # limiting the number of search fields to a reasonable number will make it easier for your database to do the search.
    search_fields = ["question_text"]


'''
# Another way
class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
'''

admin.site.register(Question, QuestionAdmin)

# admin.site.register(Choice)
