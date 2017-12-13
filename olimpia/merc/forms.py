from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from .models import Series, TorrentServers


CHOICES = (( False,'No',), ( True,'Si',))
CHOICES_QUALITY = (( 'NR','NR',),( 'HD','HD',),( 'VO','VO',),)

class SeriesForm(forms.ModelForm):
    
    ep_start = forms.CharField(max_length=8, min_length=8,  initial="NRS00E00",widget=forms.TextInput(attrs={'class' : 'form-control','readonly':'readonly'}))
    ep_end = forms.CharField(max_length=8, min_length=8,  initial="NRS99E99",widget=forms.TextInput(attrs={'class' : 'form-control','readonly':'readonly'}))
    quality = forms.CharField(max_length=2, min_length=2,  initial="NR",widget=forms.Select(attrs={'class' : 'form-control'},choices=CHOICES_QUALITY))
    
    
    
    class Meta:
        model = Series
        fields = ('nombre', 'quality','ep_start','ep_end','paussed', 'skipped', )
        widgets = {
            'nombre': forms.TextInput(attrs={'class' : 'form-control'}),
            'paussed': forms.Select(attrs={'class' : 'form-control'},choices=CHOICES),
            'skipped': forms.Select(attrs={'class' : 'form-control'},choices=CHOICES),
        }
        
    
        
class SeriesFindForm(SeriesForm):
    to_saved = forms.BooleanField(initial=False, required=False)
    class Meta(SeriesForm.Meta):
        fields = SeriesForm.Meta.fields + ('to_saved',)
        
class TorrentServersForm(forms.ModelForm):
    
        '''
        torrent_active = models.NullBooleanField(default=False)  # Field name made lowercase.
        space_disk = models.IntegerField()
        host = models.CharField(blank=True, null=True, max_length=200)
        port = models.IntegerField()
        user = models.CharField(blank=True, null=True, max_length=200)
        password = models.CharField(blank=True, null=True, max_length=200)
        paused = models.NullBooleanField(default=False)  # Field name made lowercase.
        download = models.CharField(blank=True, null=True, max_length=200)
        '''
    
    
        class Meta:
            model = TorrentServers
            fields = ('torrent_active', 'space_disk','host','port','user', 'password', 'paused','download' )
            widgets = {
                'torrent_active': forms.Select(attrs={'class' : 'form-control'},choices=CHOICES),
                'space_disk':forms.NumberInput(attrs={'class' : 'form-control'}),
                'host': forms.TextInput(attrs={'class' : 'form-control'}),
                'port':forms.NumberInput(attrs={'class' : 'form-control'}),
                'user': forms.TextInput(attrs={'class' : 'form-control'}),
                'password':forms.PasswordInput(attrs={'class' : 'form-control'}),
                'paused': forms.Select(attrs={'class' : 'form-control'},choices=CHOICES),
                'download': forms.TextInput(attrs={'class' : 'form-control'}),
            }