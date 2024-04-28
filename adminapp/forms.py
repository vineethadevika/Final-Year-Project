from django import forms
from django.core.validators import MinValueValidator
from .models import AddTimeTable
from django.utils import timezone
from .models import AddStudent
from django.core.exceptions import ValidationError
from .models import Room

class AdminlogForm(forms.Form):
    adminemail = forms.EmailField(
        label='Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    adminpassword = forms.CharField(
        label='Password', required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class AddTimeTableForm(forms.ModelForm):
    class Meta:
        model = AddTimeTable
        fields = ['subject', 'iv_cse_a_faculty', 'iv_cse_b_faculty', 'iv_cse_c_faculty']


def all_emails():
    try:
        from .models import AddFaculty
        all_emails = [(i.email, i.email) for i in AddFaculty.objects.all()]
        return all_emails

    except:
        all_emails = ""
        return all_emails


branches = [
    ("cse", "Cse"),
    ("it", "It"),
    ("ece", "Ece")

]

semesters = [
    ("first", "First"),
    ("second", "Second")
]

year = [
    ("first", "First"),
    ("second", "Second"),
    ("third", "Third"),
    ("fourth", "Fourth")
]


subjects = [
    ('Select Subject', 'selects subject'),
    ('Mathematics and Discrete Structures', 'mathematics and discrete structures'),

    ('Computer Networks', 'computer networks'),

    ('Databases', 'databases'),

    ('Web Technologies', 'web technologies'),

    ('Data Structures', 'data structures'),

    ('Operating Systems', 'operating systems'),

    ('Discrete Mathematics ', 'discrete mathematics '),

    ('Introduction to Probability and Statistics ',
        'introduction to probability and statistics '),

    ('Computer Organization and Architecture ',
        'computer organization and architecture '),

    ('Object Oriented Programming', 'object oriented programming'),

]


class AddStudentForm(forms.Form):
    rollnumber = forms.CharField(
        label='Roll Number', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    name = forms.CharField(
        label='Student Name', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        label='Department', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email', max_length=100, required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label='Contact', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    year = forms.IntegerField(
        label='Year', required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    semester = forms.IntegerField(
        label='Semester', required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    profile_url = forms.URLField(
        label='Profile URL', max_length=200, required=True,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )


    
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel File', 
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    


class AddexamhallForm(forms.Form):
    Date = forms.DateField(label='Date', required=True,
                           widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    starttime = forms.TimeField(label='Exam start time', 
                                widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    endtime = forms.TimeField(label='Exam End Time', 
                              widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    noofrooms = forms.IntegerField(label="Rooms", required=True, 
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}), 
                                   validators=[MinValueValidator(0)])
    noofbenches = forms.IntegerField(label="Benches", required=True, 
                                     widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 0}), 
                                     validators=[MinValueValidator(0)])
    rooms_list = forms.CharField(widget=forms.HiddenInput(), required=False)
    students_per_bench = forms.ChoiceField(label="Students per bench", choices=[(2, 'Two students per bench'), (3, 'Three students per bench')],
                                           widget=forms.RadioSelect(), required=True)

    def clean_Date(self):
        date = self.cleaned_data.get('Date')
        if date < timezone.now().date():
            raise forms.ValidationError("Date cannot be in the past.")
        return date

    def clean_starttime(self):
        starttime = self.cleaned_data.get('starttime')
        if self.cleaned_data.get('Date') == timezone.now().date() and starttime < timezone.now().time():
            raise forms.ValidationError("Start time cannot be in the past for today's date.")
        return starttime

    def clean_endtime(self):
        endtime = self.cleaned_data.get('endtime')
        if endtime is None:
            raise forms.ValidationError("End time is required.")
        
        if self.cleaned_data.get('Date') == timezone.now().date() and endtime < timezone.now().time():
            raise forms.ValidationError("End time cannot be in the past for today's date.")
        
        starttime = self.cleaned_data.get('starttime')
        if starttime and endtime <= starttime:
            raise forms.ValidationError("End time should be after start time.")
    
        return endtime

    def clean_noofrooms(self):
        noofrooms = self.cleaned_data.get('noofrooms')
        if noofrooms is not None and noofrooms <= 0:
            raise forms.ValidationError("Number of rooms must be a positive integer.")
        return noofrooms

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rooms'] = forms.ModelMultipleChoiceField(
            queryset=Room.objects.all(),
            required=True,
            widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            label="Select Rooms"
        )
    
    def clean_rooms(self):
        selected_rooms = self.cleaned_data.get('rooms', [])
        no_of_rooms_entered = self.cleaned_data.get('noofrooms', 0)
        
        if len(selected_rooms) != no_of_rooms_entered:
            raise forms.ValidationError("Please select exactly {} rooms.".format(no_of_rooms_entered))
        
        return selected_rooms

    def clean_noofbenches(self):
        noofbenches = self.cleaned_data.get('noofbenches')
        if noofbenches is not None and noofbenches <= 0:
            raise forms.ValidationError("Number of benches must be a positive integer.")
        return noofbenches


    def clean(self):
        cleaned_data = super().clean()
        noofrooms = cleaned_data.get('noofrooms')
        noofbenches = cleaned_data.get('noofbenches')
        students_per_bench = int(cleaned_data.get('students_per_bench', 2))

        if noofrooms is not None and noofbenches is not None:
            total_students = AddStudent.objects.count()
            total_seats_available = noofrooms * noofbenches * students_per_bench
            if total_seats_available < total_students:
                raise forms.ValidationError(
                    "Not enough seats available in the exam hall for the total number of students.",
                    code='seats_unavailable'  # Assign a custom error code
                )

        return cleaned_data



class AddFacultyForm(forms.Form):

    name = forms.CharField(
        label='Faculty Name', max_length=50, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Faculty Email', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label='Faculty Contact', max_length=10, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    branch = forms.ChoiceField(
        label='Branch', choices=branches, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    subject = forms.ChoiceField(
        label='Subject', choices=subjects, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    semester = forms.ChoiceField(
        label='Semester', choices=semesters, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    year = forms.ChoiceField(
        label='Year', choices=year, required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label='Faculty Profile', required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )


class AdminAnnouncement(forms.Form):
    announcement = forms.CharField(
        label='Enter Announcement', max_length=150, required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your announcement here'})
    )
