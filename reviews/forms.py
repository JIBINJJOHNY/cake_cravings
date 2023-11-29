from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=Review.STAR_CHOICES),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].label = 'Rating'
        self.fields['comment'].label = 'Comment'


class UpdateReviewForm(forms.Form):
    rating = forms.IntegerField()
    comment = forms.CharField()
